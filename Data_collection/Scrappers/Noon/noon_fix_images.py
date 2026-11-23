"""
تصليح الصور بس (أسرع من الـ backfill الكامل).

  python noon_fix_images.py            # شغّال لوحده
  python noon_fix_images.py 1 2        # نافذة 1 من 2 (شغّل التانية: python noon_fix_images.py 2 2)
  python noon_fix_images.py merge      # يدمج النتيجة في noon_all.parquet و noon_all.csv
  python noon_fix_images.py only       # يعيد بس الفروع المكتوبة في retry_leaves.txt (سطر لكل فرع: Category / Subcategory)

- بيزور بس الفروع اللي فيها منتجات صورتها فاضية أو placeholder.
- بيجمع الصفحة كلها بأمر JavaScript واحد (بدل مئات أوامر Selenium).
- بيكتب في ملفات صغيرة images_partN.csv ومش بيلمس noon_all لحد ما تعمل merge.
- لو وقف، شغّله تاني وبيكمل (بيتخطى اللي اتصلّح).
"""
import ast
import csv
import glob
import os
import random
import shutil
import sys
import time

import pandas as pd

OUT_DIR = os.environ.get("NOON_DIR", os.path.join(os.path.expanduser("~"), "noon_data"))
PARQUET = os.path.join(OUT_DIR, "noon_all.parquet")
CSV_OUT = os.path.join(OUT_DIR, "noon_all.csv")
HERE = os.path.dirname(os.path.abspath(__file__))
PARAMS = "limit=50&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc"
MAX_PAGES = 12

JS_EXTRACT = """
return Array.from(document.querySelectorAll('[data-qa="plp-product-box-name"]')).map(n => {
  const a = n.closest('a[href*="/p/"]');
  if (!a) return null;
  const src = Array.from(a.querySelectorAll('img')).map(i => i.src || '')
                   .find(s => s.includes('nooncdn.com/p/')) || '';
  return [a.href, src];
}).filter(Boolean);
"""


def clean_link(link):
    return link.split("?")[0] if link else link


def is_missing(series):
    return (series == "") | series.str.contains("placeholder", na=False)


def load_categories():
    files = sorted(glob.glob(os.path.join(HERE, "noon_scraper*.py")))
    if not files:
        sys.exit("مش لاقي noon_scraper.py جنب السكريبت ده (لازم يبقوا في نفس الفولدر).")
    tree = ast.parse(open(files[0], encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "CATEGORIES":
            return ast.literal_eval(node.value)
    sys.exit("مش لاقي CATEGORIES في " + files[0])


def load_found():
    found = {}
    for f in glob.glob(os.path.join(OUT_DIR, "images_part*.csv")):
        with open(f, encoding="utf-8", newline="") as fh:
            for row in csv.reader(fh):
                # نتجاهل أي سطر مقطوع (مثلاً من امتلاء القرص): لازم لينك نون وصورة من نون
                if (len(row) == 2 and row[0].startswith("https://www.noon.com")
                        and row[1].startswith("https://f.nooncdn.com/p/")):
                    found[row[0]] = row[1]
    return found


def check_space(min_mb=500):
    free = shutil.disk_usage(OUT_DIR).free / 1024 / 1024
    if free < min_mb:
        sys.exit(f"المساحة الفاضية على القرص {free:.0f} MB بس. فضّي مساحة (أقل حاجة {min_mb} MB) وشغّله تاني.")


def merge():
    check_space(500)
    df = pd.read_parquet(PARQUET).astype(str)
    found = load_found()
    mask = is_missing(df["Image"])
    before = int(mask.sum())
    mapped = df.loc[mask, "Link"].map(found)
    df.loc[mask, "Image"] = mapped.fillna(df.loc[mask, "Image"])
    after = int(is_missing(df["Image"]).sum())
    # نكتب في ملف مؤقت وبعدين نبدّل، عشان لو القرص اتملا الملف الأصلي مايتبوّظش
    tmp_pq, tmp_csv = PARQUET + ".tmp", CSV_OUT + ".tmp"
    df.to_parquet(tmp_pq, index=False)
    df.to_csv(tmp_csv, index=False, encoding="utf-8-sig")
    os.replace(tmp_pq, PARQUET)
    os.replace(tmp_csv, CSV_OUT)
    print(f"images missing: {before} -> {after} (of {len(df)} rows)")
    good = df.loc[~is_missing(df["Image"]), "Image"]
    print("image endings (لو فيه نهايات غريبة يبقى فيه روابط مقطوعة):",
          good.str[-4:].value_counts().head(6).to_dict())


def run(part, parts, only=False):
    check_space(300)
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    df = pd.read_parquet(PARQUET, columns=["Link", "Image", "Category", "Subcategory"]).astype(str)
    found = load_found()
    need = df[is_missing(df["Image"]) & ~df["Link"].isin(found)]
    todo = {}
    for cat, sub, link in zip(need["Category"], need["Subcategory"], need["Link"]):
        todo.setdefault((cat, sub), set()).add(link)

    leaves = [(c, s, u) for c, subs in load_categories().items() for s, u in subs.items()]
    mine = [l for i, l in enumerate(leaves) if i % parts == part - 1 and todo.get((l[0], l[1]))]
    if only:
        rf = next((f for f in (os.path.join(HERE, "retry_leaves.txt"), os.path.join(OUT_DIR, "retry_leaves.txt"))
                   if os.path.exists(f)), None)
        if not rf:
            sys.exit("مش لاقي retry_leaves.txt (حطه جنب السكريبت).")
        wanted = {ln.strip() for ln in open(rf, encoding="utf-8") if ln.strip()}
        mine = [l for l in mine if f"{l[0]} / {l[1]}" in wanted]
    total_missing = sum(len(todo[(c, s)]) for c, s, _ in mine)
    print(f"part {part}/{parts}: {len(mine)} leaves, {total_missing} products need images")
    if not mine:
        print("nothing to do")
        return

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=ar-EG")
    # عشان الصور تتحمّل حتى لو النافذة ورا نافذة تانية
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-background-timer-throttling")
    driver = webdriver.Chrome(options=options)

    mapfile = os.path.join(OUT_DIR, f"images_part{part}.csv")
    new_file = not os.path.exists(mapfile)
    failed, fixed_total, started = [], 0, time.time()
    try:
        for i, (cat, sub, url) in enumerate(mine, 1):
            missing = set(todo[(cat, sub)])
            want = len(missing)
            seen = set()
            try:
                for page in range(1, MAX_PAGES + 1):
                    driver.get(f"{url}?{PARAMS}&page={page}")
                    time.sleep(3)
                    for _ in range(8):
                        driver.execute_script("window.scrollBy(0, 1000)")
                        time.sleep(0.7)
                    rows = driver.execute_script(JS_EXTRACT)
                    items = {}
                    for link, src in rows:
                        items.setdefault(clean_link(link), src)
                    if not items:
                        break
                    new = [l for l in items if l not in seen]
                    if page > 1 and len(new) < len(items) * 0.5:
                        break
                    seen.update(new)
                    hits = {l: items[l] for l in missing if items.get(l)}
                    if hits:
                        with open(mapfile, "a", encoding="utf-8", newline="") as fh:
                            w = csv.writer(fh)
                            if new_file:
                                w.writerow(["Link", "Image"])
                                new_file = False
                            for l, src in hits.items():
                                w.writerow([l, src])
                        missing -= set(hits)
                        fixed_total += len(hits)
                    if not missing:
                        break
                    time.sleep(random.uniform(1, 2.5))
            except OSError as e:
                if getattr(e, "errno", None) == 28:     # القرص اتملا: مفيش فايدة نكمّل
                    print("!! القرص اتملا. فضّي مساحة وشغّل السكريبت تاني (بيكمّل من مكانه).")
                    failed.append(f"{cat} / {sub}")
                    break
                print(f"!! {sub} failed: {str(e)[:120]}")
                failed.append(f"{cat} / {sub}")
            except Exception as e:
                print(f"!! {sub} failed: {str(e)[:120]}")
                failed.append(f"{cat} / {sub}")
            mins = (time.time() - started) / 60
            print(f"[{i}/{len(mine)}] {sub}: fixed {want - len(missing)}/{want} "
                  f"| total fixed {fixed_total}/{total_missing} | {mins:.1f} min", flush=True)
    finally:
        driver.quit()
    print("\nDone. Failed:", failed)
    if failed:
        try:
            with open(os.path.join(OUT_DIR, "images_failed.txt"), "w", encoding="utf-8") as fh:
                fh.write("\n".join(failed))
            print("الفروع الفاشلة اتسجلت في images_failed.txt (انسخها في retry_leaves.txt وشغّل: only)")
        except OSError:
            pass
    print("Next: python noon_fix_images.py merge")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "merge":
        merge()
    elif args and args[0] == "only":
        run(1, 1, only=True)
    else:
        p = int(args[0]) if len(args) >= 1 else 1
        n = int(args[1]) if len(args) >= 2 else 1
        run(p, n)
