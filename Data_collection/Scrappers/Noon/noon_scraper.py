from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import random
import re
import os
import time


CATEGORIES = {
    "Mobile Accessories": {
        "Cases & Covers": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/cases-and-covers/",
        "Screen Protectors": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/screen-protectors-24427/",
        "Data Cables": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/data-cables/",
        "Car Mounts": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/car-mounts/",
        "Wall Chargers": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/chargers-17982/wall-chargers/",
        "Wireless Chargers": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/chargers-17982/wireless-chargers/",
        "Phone Grips Stands": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/phone-grips-stands/",
        "Power Banks": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/power-banks/",
        "Mobile Lens Lens Protectors": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/mobile-lens-lens-protectors/",
        "Car Chargers": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/car-chargers-18279/",
        "Mounts": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/mounts-24349/",
        "Selfie Sticks": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/selfie-sticks/",
        "USB OTG Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/usb-otg-adapters/",
        "Universal Travel Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/universal-travel-adapters/",
        "Smartphone Handheld Gimbals Stabilizers": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/smartphone-handled-gimbals-stabilizers/",
        "Bluetooth Trackers": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/bluetooth-trackers/",
        "Headphone Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/headphone-adapters/",
        "Mobile Phone Batteries": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/mobile-phone-batteries/",
        "Mobile Phone Skin Stickers": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/mobile-phone-skin-stickers/",
        "Replacement Screens": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/replacement-screens/",
        "Screen Magnifiers": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/screen-magnifiers/",
        "SIM Card Tools Accessories": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/sim-card-tools-accessories/",
        "Anti Dust Plugs": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/anti-dust-plugs/",
        "Mobile Phone Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/mobile-phone-adapters/",
        "Mobile Body Panels": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/mobile-body-panels/",
        "Headsets": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/headsets-18965/",
        "Speaker Cases": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/speaker-cases/",
        "Selfie Monitor Screen": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/selfie-monitor-screen/",
        "Micro Sd Cards": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/accessories-16176/micro-sd-cards-25125/",
    },
    "Mobiles": {
        "Smartphones": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/mobiles-20905/smartphones/",
        "Feature Phones": "https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/mobiles-20905/feature_phones/",
    },
    "Laptop Accessories": {
        "Screen Protectors": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/laptop-accessories/screen-protectors-26162/",
        "Sleeves & Slipcases": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/laptop-accessories/bags-and-cases-16607/sleeves-and-slipcases-23672/",
        "Laptop Skins": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/laptop-accessories/bags-and-cases-16607/laptop-skins/",
        "Backpacks": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/laptop-accessories/bags-and-cases-16607/backpacks-26174/",
        "Chargers & Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/laptop-accessories/chargers-and-adapters-17988/",
        "Docking Stations": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/laptop-accessories/docking-stations-16141/",
        "Laptop Batteries": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/laptop-accessories/laptop-batteries/",
        "Laptop Replacement Keyboards": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/laptop-accessories/laptop-replacement-keyboards/",
        "Laptop Security Locks": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/laptop-accessories/laptop-security-locks/",
    },
    "PC Peripherals & Cables": {
        "Mousepads": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/mousepads/",
        "Digital Pens": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/input-devices/digital-pens/",
        "Graphics Tablets": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/input-devices/graphics-tablets/",
        "Numeric Keypads": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/input-devices/numeric-keypads/",
        "Presentation Pointers": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/input-devices/presentation-pointers-19084/",
        "Touch Pads": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/input-devices/touch-pads/",
        "Desktop Power Cables": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/cables-and-interconnects-18838/desktop-power-cables/",
        "HDMI Cable": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/cables-and-interconnects-18838/hdmi-cable/",
        "VGA Cable": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/cables-and-interconnects-18838/vga-cable/",
        "SATA Cable": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/cables-and-interconnects-18838/sata-cable/",
        "Keyboards": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/keyboards-21187/",
        "Mouses": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/mouses/",
        "Gaming Headsets": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/gaming-headsets/",
        "Gaming Mouse": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/gaming-mouse-vg/",
        "Keyboard & Mouse Combos": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/keyboard-and-mouse-combos/",
        "Gaming Keyboards": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/gaming-keyboards-vg/",
        "Hard Drive Enclosure": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/hard-drive-enclosure/",
        "Gaming Mousepad": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/gaming-mousepad/",
        "Gaming Keyboard Mouse Set": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/gaming-keyboard-mouse-set-ea/",
        "Computer Speakers": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/computer-speakers/",
        "Memory Card Readers": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/memory-card-readers/",
        "Headsets & Microphones": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/headsets-and-microphones-16755/",
        "USB to Ethernet Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/usb-to-ethernet-adapters/",
        "Uninterrupted Power Supply UPS": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/uninterrupted-power-supply-ups-20866/",
        "USB Lamps": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/usb-lamps/",
        "Wrist Rests": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/wrist-rests/",
        "Memory Card Cases": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/cables-and-accessories/memory-card-cases/",
    },
    "PC Components": {
        "Memory": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/computer-components-15997/memory-25310/",
        "Power Supplies": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/computer-components-15997/power-supplies/",
        "Fans & Cooling": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/computer-components-15997/fans-and-cooling/",
        "Internal Cooling Systems": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/computer-components-15997/internal-cooling-systems-46785/",
        "Graphics Cards": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/computer-components-15997/graphics-cards/",
        "Video Capture Cards": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/computer-components-15997/video-capture-cards/",
        "PC Cases": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/computer-components-15997/pc-cases/",
        "Network Cards": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/computer-components-15997/network-cards/",
        "Motherboards": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/computer-components-15997/motherboards/",
        "Sound Cards": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/computer-components-15997/sound-cards/",
        "Cpu Processors": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/computer-components-15997/cpu-processors/",
    },
    "Networking": {
        "Hubs": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/hubs-22673/",
        "Routers": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/routers/",
        "Ethernet Cable": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/ethernet-cable/",
        "Switches": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/switches-22460/",
        "Wireless USB Adapter": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/wireless-usb-adapter/",
        "Network Hub": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/network-hub/",
        "Repeaters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/repeaters/",
        "Network USB to Ethernet Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/network-usb-to-ethernet-adapters/",
        "Mesh System": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/mesh-system/",
        "Powerlan Adapter": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/powerlan-adapter/",
        "Network Antennas": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/network-antennas/",
        "Network Cable Testers": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/network-cable-testers/",
        "Modem": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/modem/",
        "Data Cards Dongle": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/data-cards-dongle/",
        "Print Server": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/networking-products-16523/print-server/",
    },
    "Monitors": {
        "Monitor Arms & Stands": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/monitor-accessories/monitor-arms-and-stands-25606/",
        "Monitors": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/monitor-accessories/monitors-17248/",
        "Portable Monitors": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/monitor-accessories/portable-monitors/",
    },
    "Data Storage": {
        "Internal Hard Drives": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/data-storage/internal-hard-drives/",
        "Internal Solid State Drives": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/data-storage/internal-solid-state-drives/",
        "External Hard Drives": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/data-storage/external-hard-drives/",
        "Memory Cards": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/data-storage/memory-cards/",
        "USB Flash Drives": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/data-storage/usb-flash-drives/",
        "External Solid State Drives": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/data-storage/external-solid-state-drives/",
        "Network Attached Storage": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/data-storage/network-attached-storage-18079/",
        "Crypto Hardware Wallets": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/data-storage/crypto-hardware-wallets/",
    },
    "Printers & Scanners": {
        "Laser Printers": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/printers/laser-printers/",
        "All in One Printers": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/printers/all-in-one-printers/",
        "3D Printers": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/printers/3d-printers/",
        "Receipt Printers": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/printers/receipt-printers/",
        "Inkjet Printers": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/printers/inkjet-printers/",
        "Toner Cartridges": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/printer-accessories-22725/toner-cartridges/",
        "Ink Cartridges": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/printer-accessories-22725/ink-cartridges/",
        "Printer Cables": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/printer-accessories-22725/printer-cables/",
        "Inks Refill Kit": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/printer-accessories-22725/inks-refill-kit/",
        "Printer Ribbon": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/printer-accessories-22725/printer-ribbon/",
        "Printer Transfer Rollers": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/printer-accessories-22725/printer-transfer-rollers-22727/",
        "Printer Trays": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/printer-accessories-22725/printer-trays-24889/",
        "Documents Photo Scanners": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/scanners/documents-photo-sanners/",
        "Flatbed Scanners": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/scanners/flatbed-scanners/",
        "3D Scanners": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/scanners/3d-scanners/",
    },
    "Adapters, Webcams & Servers": {
        "HDMI Gender Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/hdmi-adapters/hdmi-gender-adapters/",
        "HDMI to Displayport Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/hdmi-adapters/hdmi-to-displayport-adapters/",
        "HDMI to USB Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/hdmi-adapters/hdmi-to-usb-adapters/",
        "HDMI to VGA Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/hdmi-adapters/hdmi-to-vga-adapters/",
        "HDMI to DVI Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/hdmi-adapters/hdmi-to-dvi-adapters/",
        "Webcams": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/webcams/",
        "VGA to HDMI Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/vga-adapters/vga-to-hdmi-adapters/",
        "VGA to USB Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/vga-adapters/vga-to-usb-adapters/",
        "VGA Gender Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/vga-adapters/vga-gender-adapters/",
        "VGA to Displayport Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/vga-adapters/vga-to-displayport-adapters/",
        "VGA to DVI Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/vga-adapters/vga-to-dvi-adapters/",
        "Anti Dust Plugs": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/anti-dust-plugs-ca/",
        "Servers": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computer-accessories/servers-18304/",
    },
    "Laptops": {
        "Laptop Notebooks": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/laptops/laptop-notebooks/",
        "Business Laptops": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/laptops/business-laptops/",
        "2 in 1 Laptops": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/laptops/2-in-1-laptops/",
        "AI Laptops": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/laptops/ai-laptops/",
        "Ultrabooks": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/laptops/ultrabooks/",
        "Macbooks": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/laptops/macbooks/",
        "Laptop Netbooks": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/laptops/laptop-netbooks/",
        "Gaming Laptops": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/laptops/gaming-laptops/",
    },
    "Desktops": {
        "Desktop Tower PCS": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/desktops/desktop-tower-pcs/",
        "All in One PCS": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/desktops/all-in-one-pcs/",
        "Mini PCS": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/desktops/mini-pcs/",
        "Business Desktops": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/desktops/business-desktops/",
        "AI Desktops": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/desktops/ai-desktops/",
        "Gaming Desktop": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/desktops/gaming-desktop/",
        "Stick PCS": "https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/computers-new/desktops/stick-pcs/",
    },
    "Wearables": {
        "Smartwatch Band": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/smart-watches-and-accessories/smartwatch-accessories/smartwatch-band/",
        "Smartwatch Cases": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/smart-watches-and-accessories/smartwatch-accessories/smartwatch-cases/",
        "Smartwatch Screen Protectors": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/smart-watches-and-accessories/smartwatch-accessories/smartwatch-screen-protectors/",
        "Smartwatch Charger": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/smart-watches-and-accessories/smartwatch-accessories/smartwatch-charger/",
        "Smartwatch Case with Band": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/smart-watches-and-accessories/smartwatch-accessories/smartwatch-case-with-band/",
        "Smartwatches": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/smart-watches-and-accessories/smartwatches/",
        "Fitness Trackers": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/fitness-trackers-and-accessories/fitness-trackers/",
        "Fitness Tracker Bands": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/fitness-trackers-and-accessories/fitness-tracker-accessories/fitness-tracker-bands/",
        "Fitness Tracker Cases": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/fitness-trackers-and-accessories/fitness-tracker-accessories/fitness-tracker-cases/",
        "Fitness Tracker Chargers": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/fitness-trackers-and-accessories/fitness-tracker-accessories/fitness-tracker-chargers/",
        "Fitness Tracker Screen Protectors": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/fitness-trackers-and-accessories/fitness-tracker-accessories/fitness-tracker-screen-protectors/",
        "Smart Rings": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/smart-rings/",
        "Smart Glasses": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/smart-glasses/",
        "Virtual Reality Headsets": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/virtual-reality-headsets/",
        "AR Glasses": "https://www.noon.com/egypt-en/electronics-and-mobiles/wearable-technology/ar-glasses/",
    },
    "Video Games": {
        "Console Sticker": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/console-sticker/",
        "Gaming Mouse Video Games": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/gaming-keyboard-and-mice/gaming-mouse-video-games/",
        "Gaming Keyboard": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/gaming-keyboard-and-mice/gaming-keyboard/",
        "Gaming Mousepads": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/gaming-keyboard-and-mice/gaming-mousepads/",
        "Gaming Keyboard Mouse Sets": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/gaming-keyboard-and-mice/gaming-keyboard-mouse-sets/",
        "Microphone & Headsets": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/microphone-and-headsets/",
        "Console Accessories": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/console-accessories/",
        "Gaming Chairs": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/gaming-chairs/",
        "Controller Cover": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/controller-cover/",
        "Stands": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/stands/",
        "Chargers Cables": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/chargers-cables/",
        "Finger Gloves & Sleeves": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/finger-gloves-and-sleeves/",
        "Gaming Replacement Accessories": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/gaming-replacement-accessories/",
        "Thumb Grips": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/thumb-grips/",
        "Game Cases": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/game-cases/",
        "VR Headsets": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/vr-headsets/",
        "Digital Cards": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/digital-cards/",
        "Console Cameras": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/console-cameras/",
        "Gaming Triggers": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/gaming-triggers/",
        "Display Stand": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/display-stand/",
        "Audio Controller": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/audio-controller/",
        "Gaming Motherboards": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-accessories/gaming-motherboards/",
        "Games": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/games-34004/",
        "Controllers & Joysticks": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-controllers/controllers-and-joysticks/",
        "Gaming Pedals": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-controllers/gaming-pedals/",
        "Gaming Steering Wheels": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-controllers/gaming-steering-wheels/",
        "Gaming Pistols Guns": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-controllers/gaming-pistols-guns/",
        "Electronic Dancing Mat": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-controllers/electronic-dancing-mat/",
        "Gaming Guitars": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-controllers/gaming-guitars/",
        "Gaming Skateboards": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-controllers/gaming-skateboards/",
        "Gaming Console": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/gaming-console/",
        "Game Tables Video": "https://www.noon.com/egypt-en/electronics-and-mobiles/video-games-10181/game-tables-video/",
    },
    "Cameras & Photo": {
        "Photography Lights": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/lighting-and-studio/photography-lights/",
        "Soft Boxes": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/lighting-and-studio/soft-boxes/",
        "Backgrounds": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/lighting-and-studio/backgrounds/",
        "Reflectors": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/lighting-and-studio/reflectors/",
        "Photographic Background Weighting Rails": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/lighting-and-studio/photographic-background-weighting-rails/",
        "Photo Screen Umbrellas": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/lighting-and-studio/photo-screen-umbrellas/",
        "Photography Meters": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/lighting-and-studio/photography-meters/",
        "Complete Tripod Units": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/tripods-and-monopods/complete-tripod-units/",
        "Tripod & Monopod Accessories": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/tripods-and-monopods/tripod-and-monopod-accessories/",
        "Tripod Heads": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/tripods-and-monopods/tripod-heads/",
        "Dynamic": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/camera-microphones/dynamic/",
        "Condenser": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/camera-microphones/condenser/",
        "Lavalier": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/camera-microphones/lavalier/",
        "Batteries & Chargers": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/batteries-and-chargers-17570/",
        "Connection Kits": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/connection-kits/",
        "Camera Stabilizers": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/camera-supports-and-stabilizers/camera-stabilizers/",
        "Camera Shoulder Supports": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/camera-supports-and-stabilizers/camera-shoulder-supports/",
        "Film": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/film/",
        "Diffusers": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/flash-accessories/diffusers-23071/",
        "Camera Brackets": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/flash-accessories/camera-brackets/",
        "Adapter Rings": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/flash-accessories/adapter-rings/",
        "Accessory Bundles": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/accessory-bundles/",
        "Camera Microphone Accessories": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/camera-microphone-accessories/",
        "Safelights": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/darkroom-supplies/safelights/",
        "Film Processing Equipment": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/darkroom-supplies/film-processing-equipment/",
        "Lens Accessories": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/lens-accessories/",
        "Filter Sets": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/filters-and-accessories/filter-sets/",
        "Neutral Density Filters": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/filters-and-accessories/neutral-density-filters/",
        "Black & White Contrast Filters": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/filters-and-accessories/black-and-white-contrast-filters/",
        "Polarizing Filters": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/filters-and-accessories/polarizing-filters/",
        "Infrared Filters": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/filters-and-accessories/infrared-filters/",
        "Skylight & UV Filters": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/filters-and-accessories/skylight-and-uv-filters/",
        "Photography Paper": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/photography-paper/",
        "Surveillance Housing & Mounting Brackets": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/surveillance-accessories/surveillance-housing-and-mounting-brackets-24194/",
        "Battery Grips": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/digital-camera-accessories/battery-grips/",
        "Microscope Accessories": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/telescope-and-microscope-accessories/microscope-accessories/",
        "Telescope Accessories": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/telescope-and-microscope-accessories/telescope-accessories/",
        "Digital Picture Frames": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/digital-picture-frames-25455/",
        "Binocular Camera & Camcorder Straps": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/binocular-camera-and-camcorder-straps-19086/",
        "Case & Bag Accessories": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/accessories-16794/case-and-bag-accessories/",
        "Dome Cameras": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/surveillance-cameras-18886/dome-cameras-20881/",
        "Bullet Cameras": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/surveillance-cameras-18886/bullet-cameras-18887/",
        "Video": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/video-17975/",
        "Instant Cameras": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/instant-cameras/",
        "Camera Cases": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/bags-and-cases-19385/camera-cases-19386/",
        "Camera Bags & Backpacks": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/bags-and-cases-19385/camera-bags-and-backpacks/",
        "Camcorder Cases": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/bags-and-cases-19385/camcorder-cases-24803/",
        "Mirrorless Camera Lenses": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/lenses-16166/mirrorless-camera-lenses/",
        "Digital Camera Lenses": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/lenses-16166/digital-camera-lenses/",
        "Point & Shoot Digital Cameras": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/digital-cameras/point-and-shoot-digital-cameras/",
        "Mirrorless Cameras": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/digital-cameras/mirrorless-cameras/",
        "Digital SLR Cameras": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/digital-cameras/digital-slr-cameras/",
        "Binoculars": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/binoculars-and-scopes/binoculars-21342/",
        "Microscopes": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/binoculars-and-scopes/microscopes-21504/",
        "Borescopes": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/binoculars-and-scopes/borescopes/",
        "Telescopes": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/binoculars-and-scopes/telescopes/",
        "Monoculars": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/binoculars-and-scopes/monoculars/",
        "Laser Rangefinders": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/binoculars-and-scopes/laser-rangefinders/",
        "Rifle Scopes": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/binoculars-and-scopes/rifle-scopes-20336/",
        "External Flash": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/flashes/external-flash/",
        "Camcorders": "https://www.noon.com/egypt-en/electronics-and-mobiles/camera-and-photo-16165/camcorders/",
    },
    "TV & Video": {
        "TV Mounts": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/television-accessories-16510/tv-mounts-22554/",
        "Video Converters": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/television-accessories-16510/video-converters-22403/",
        "Remote Controls": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/television-accessories-16510/remote-controls-16511/",
        "Projection Screens": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/television-accessories-16510/projector-accessories-18907/projection-screens-18908/",
        "Lamps": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/television-accessories-16510/projector-accessories-18907/lamps-20661/",
        "Remote Control Holder": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/television-accessories-16510/remote-control-holder/",
        "TV Screen Protectors": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/television-accessories-16510/tv-screen-protectors/",
        "3D Glasses": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/television-accessories-16510/3d-glasses/",
        "Projectors": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/projectors/",
        "Streaming Media Players": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/streaming-media-players/",
        "Televisions": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/televisions/",
        "Speaker Systems": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/home-theater-systems-19095/speaker-systems-19600/",
        "AV Receivers": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/home-theater-systems-19095/av-receivers/",
        "Home Theater": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/home-theater-systems-19095/home-theater/",
        "Book Shelf Speaker": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/home-theater-systems-19095/book-shelf-speaker/",
        "Floor Standing Speakers": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/home-theater-systems-19095/floor-standing-speakers/",
        "Tall Boy Speaker": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/home-theater-systems-19095/tall-boy-speaker/",
        "Satellite Speaker": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/home-theater-systems-19095/satellite-speaker/",
        "Set Top Boxes": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/set-top-boxes-47527/",
        "LNB Converters": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/satellite-equipments-accessories/lnb-converters/",
        "Satellite Finders": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/satellite-equipments-accessories/satellite-finders/",
        "Satellite Dishes": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/satellite-equipments-accessories/satellite-dishes/",
        "Projection Screens (20836)": "https://www.noon.com/egypt-en/electronics-and-mobiles/television-and-video/projection-screens-20836/",
    },
    "Audio/Video Accessories": {
        "Headphone Cases": "https://www.noon.com/egypt-en/electronics-and-mobiles/accessories-and-supplies/audio-and-video-accessories-16161/headphone-earphone-accessories/headphone-cases/",
        "Headphone Earpads": "https://www.noon.com/egypt-en/electronics-and-mobiles/accessories-and-supplies/audio-and-video-accessories-16161/headphone-earphone-accessories/headphone-earpads/",
        "Headphone Extension Cords": "https://www.noon.com/egypt-en/electronics-and-mobiles/accessories-and-supplies/audio-and-video-accessories-16161/headphone-earphone-accessories/headphone-extension-cords/",
        "Earbud Tips": "https://www.noon.com/egypt-en/electronics-and-mobiles/accessories-and-supplies/audio-and-video-accessories-16161/headphone-earphone-accessories/earbud-tips/",
        "Headphone Stands": "https://www.noon.com/egypt-en/electronics-and-mobiles/accessories-and-supplies/audio-and-video-accessories-16161/headphone-earphone-accessories/headphone-stands/",
        "Earphone Hooks": "https://www.noon.com/egypt-en/electronics-and-mobiles/accessories-and-supplies/audio-and-video-accessories-16161/headphone-earphone-accessories/earphone-hooks/",
        "Earphone Dust Guards": "https://www.noon.com/egypt-en/electronics-and-mobiles/accessories-and-supplies/audio-and-video-accessories-16161/headphone-earphone-accessories/earphone-dust-guards/",
        "Connectors & Adapters": "https://www.noon.com/egypt-en/electronics-and-mobiles/accessories-and-supplies/audio-and-video-accessories-16161/connectors-and-adapters/",
        "Speaker Stands": "https://www.noon.com/egypt-en/electronics-and-mobiles/accessories-and-supplies/audio-and-video-accessories-16161/speaker-stands-18112/",
        "Cleaning & Repair": "https://www.noon.com/egypt-en/electronics-and-mobiles/accessories-and-supplies/cleaning-and-repair/",
        "Accessory Kits": "https://www.noon.com/egypt-en/electronics-and-mobiles/accessories-and-supplies/accessory-kits-19142/",
    },
    "Portable Audio": {
        "Headphones": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/headphones-24056/",
        "Bluetooth Speakers": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/bluetooth-speakers/",
        "Microphone Stand": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/microphones-and-accessories/microphone-accessories/microphone-stand/",
        "Microphone Cables": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/microphones-and-accessories/microphone-accessories/microphone-cables/",
        "Pop Filters": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/microphones-and-accessories/microphone-accessories/pop-filters/",
        "Shock Mount": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/microphones-and-accessories/microphone-accessories/shock-mount/",
        "Mic Windscreen": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/microphones-and-accessories/microphone-accessories/mic-windscreen/",
        "Dynamic Microphones": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/microphones-and-accessories/dynamic-microphones/",
        "Condenser Microphones": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/microphones-and-accessories/condenser-microphones/",
        "Karaoke Microphones": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/microphones-and-accessories/karaoke-microphones-47669/",
        "Kids Headphones": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/kids-headphones/",
        "MP3 & MP4 Players": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/mp3-and-mp4-players/",
        "MP3 MP4 Player Accessories": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/mp3-mp4-player-accessories/",
        "Voice Recorders": "https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/voice-recorders/",
    },
    "Tablets": {
        "Cases & Sleeves": "https://www.noon.com/egypt-en/electronics-and-mobiles/tablets-and-accessories/tablet-accessories/cases-and-sleeves/",
        "Styluses": "https://www.noon.com/egypt-en/electronics-and-mobiles/tablets-and-accessories/tablet-accessories/styluses/",
        "Stands": "https://www.noon.com/egypt-en/electronics-and-mobiles/tablets-and-accessories/tablet-accessories/stands-27718/",
        "Screen Protectors": "https://www.noon.com/egypt-en/electronics-and-mobiles/tablets-and-accessories/tablet-accessories/screen-protectors-27716/",
        "Tablet Keyboards": "https://www.noon.com/egypt-en/electronics-and-mobiles/tablets-and-accessories/tablet-accessories/tablet-keyboards/",
        "Tablet Batteries": "https://www.noon.com/egypt-en/electronics-and-mobiles/tablets-and-accessories/tablet-accessories/tablet-batteries/",
        "Tablets": "https://www.noon.com/egypt-en/electronics-and-mobiles/tablets-and-accessories/tablets/",
    },
    "Home Audio": {
        "Boomboxes": "https://www.noon.com/egypt-en/electronics-and-mobiles/home-audio/radios-and-boomboxes/boomboxes/",
        "Soundbar Speakers": "https://www.noon.com/egypt-en/electronics-and-mobiles/home-audio/soundbar-speakers/",
        "Amplifiers": "https://www.noon.com/egypt-en/electronics-and-mobiles/home-audio/amplifiers/",
        "Subwoofers": "https://www.noon.com/egypt-en/electronics-and-mobiles/home-audio/subwoofers-17776/",
        "Home Stereo Systems": "https://www.noon.com/egypt-en/electronics-and-mobiles/home-audio/home-stereo-systems/",
        "Karaoke System": "https://www.noon.com/egypt-en/electronics-and-mobiles/home-audio/karaoke-system/",
        "Home Theater Systems": "https://www.noon.com/egypt-en/electronics-and-mobiles/home-audio/home-theater-systems-24545/",
        "AV Receiver": "https://www.noon.com/egypt-en/electronics-and-mobiles/home-audio/av-receiver/",
        "Audio Mixers": "https://www.noon.com/egypt-en/electronics-and-mobiles/home-audio/audio-mixers/",
        "Minidisc Players": "https://www.noon.com/egypt-en/electronics-and-mobiles/home-audio/minidisc-players/",
        "Tape Decks": "https://www.noon.com/egypt-en/electronics-and-mobiles/home-audio/tape-decks/",
    },
    "Gift Cards": {
        "Gift Card": "https://www.noon.com/egypt-en/electronics-and-mobiles/gift-card/",
    },
    "Software": {
        "Antivirus Security": "https://www.noon.com/egypt-en/electronics-and-mobiles/software-10182/antivirus-security/",
        "Operating Systems": "https://www.noon.com/egypt-en/electronics-and-mobiles/software-10182/operating-systems-25019/",
        "Utilities": "https://www.noon.com/egypt-en/electronics-and-mobiles/software-10182/utilities/",
        "Graphics Video": "https://www.noon.com/egypt-en/electronics-and-mobiles/software-10182/multimedia/graphics-video/",
        "Design Illustration": "https://www.noon.com/egypt-en/electronics-and-mobiles/software-10182/multimedia/design-illustration/",
        "Photography Software": "https://www.noon.com/egypt-en/electronics-and-mobiles/software-10182/multimedia/photography-software/",
        "Education & Reference": "https://www.noon.com/egypt-en/electronics-and-mobiles/software-10182/education-and-reference/",
    },
    "GPS & Navigation": {
        "GPS & Navigation": "https://www.noon.com/egypt-en/electronics-and-mobiles/gps-and-navigation/",
    },
}
# ============================================================================

PARAMS = "limit=50&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc"
NAME_SEL = '[data-qa="plp-product-box-name"]'
PRICE_SEL = '[data-qa="plp-product-box-price"] strong'
MAX_PAGES = 12         
BACKFILL = False      
OUT_DIR = os.path.join(os.path.expanduser("~"), "noon_data")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_CSV = os.path.join(OUT_DIR, "noon_all.csv")
OUT_PARQUET = os.path.join(OUT_DIR, "noon_all.parquet")
DONE_FILE = os.path.join(OUT_DIR, "done_backfill.txt" if BACKFILL else "done_leaves.txt")   
print("saving to:", OUT_DIR)

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_argument("--window-size=1920,1080")
options.add_argument("--lang=en-US")
options.add_experimental_option("prefs", {"intl.accept_languages": "en-US,en"})
driver = webdriver.Chrome(options=options)


def safe_text(parent, selector):
    try:
        return parent.find_element(By.CSS_SELECTOR, selector).text.strip()
    except Exception:
        return ""



REVIEWS_SEL = '[class*="countCtr"]'
RATING_RE = re.compile(r"(?<![\d.,])([0-5]\.\d)(?![\d.,])")
COUNT_RE = re.compile(r"[\d.,]+[KkMm]?")


def get_rating_reviews(card):
    reviews = ""
    try:
        el = card.find_element(By.CSS_SELECTOR, REVIEWS_SEL)
        reviews = (el.text or el.get_attribute("textContent") or "").strip()
    except Exception:
        pass
    if not COUNT_RE.fullmatch(reviews):
        reviews = ""

    text = card.text
    try:
        name = card.find_element(By.CSS_SELECTOR, NAME_SEL).text
        text = text.replace(name, " ")        
    except Exception:
        pass
    if reviews:
        
        pat = r"(?<![\d.,])" + re.escape(reviews) + r"(?![\d.,KkMm])"
        text = re.sub(pat, " ", text, count=1)
    m = RATING_RE.search(text)
    return (m.group(1) if m else ""), reviews


def clean_link(link):
    if not link:
        return link
    link = link.split("?")[0]
    return link.replace("/egypt-ar/", "/egypt-en/")


def get_image(card):
    
    for attempt in range(2):
        for im in card.find_elements(By.TAG_NAME, "img"):
            src = im.get_attribute("src") or ""
            if "nooncdn.com/p/" in src:
                return src
        if attempt == 0:
           
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", card)
            time.sleep(0.8)
    return ""


def save_all():
    df = pd.DataFrame(list(all_products.values())).astype(str)
    df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    df.to_parquet(OUT_PARQUET, index=False)  


all_products = {}
if os.path.exists(OUT_CSV):
    old = pd.read_csv(OUT_CSV, encoding="utf-8-sig", dtype=str, keep_default_na=False)
    for rec in old.to_dict("records"):
        rec["Link"] = clean_link(rec["Link"])
        all_products[rec["Link"]] = rec
done = set()
if os.path.exists(DONE_FILE):
    done = set(open(DONE_FILE, encoding="utf-8").read().split())
print("resuming:", len(all_products), "products,", len(done), "leaves done")

capped = []   

def extract_page(category, sub):
    
    for attempt in range(3):
        try:
            names = driver.find_elements(By.CSS_SELECTOR, NAME_SEL)
            if not names:
                return {}
            page_items = {}
            for n in names:
                try:
                    card = n.find_element(By.XPATH, "./ancestor::a[contains(@href,'/p/')][1]")
                except StaleElementReferenceException:
                    raise
                except Exception:
                    continue
                link = clean_link(card.get_attribute("href"))
                if not link or link in page_items:
                    continue
                img = get_image(card)
                rating, reviews = get_rating_reviews(card)
                page_items[link] = {
                    "Category": category,
                    "Subcategory": sub,
                    "Name": n.text.strip(),
                    "Link": link,
                    "Image": img,
                    "Rating": rating,
                    "Reviews": reviews,
                    "Price": safe_text(card, PRICE_SEL),
                }
            return page_items
        except StaleElementReferenceException:
            time.sleep(1.5)
    raise RuntimeError("page kept re-rendering (stale elements) after 3 attempts")


def scrape_leaf(category, sub, url):
    seen_in_leaf = set()
    added = 0
    fixed = 0
    page = 1
    while page <= MAX_PAGES:
        driver.get(f"{url}?{PARAMS}&page={page}")
        time.sleep(4)
        for _ in range(8):
            driver.execute_script("window.scrollBy(0, 1000)")
            time.sleep(0.7)

        page_items = extract_page(category, sub)
        if not page_items:
            break

        new_in_leaf = [l for l in page_items if l not in seen_in_leaf]
        
        print(f"\r  page {page}: {len(page_items)} items, {len(new_in_leaf)} new in leaf | total {len(all_products)}".ljust(90), end="", flush=True)

        
        if len(new_in_leaf) < len(page_items) * 0.5:
            break

        seen_in_leaf.update(new_in_leaf)
        for l in new_in_leaf:
            if l not in all_products:
                all_products[l] = page_items[l]
                added += 1
            elif BACKFILL:
                old_rec = all_products[l]
                for k in ("Reviews", "Rating", "Image"):
                    val = page_items[l][k]
                    cur = str(old_rec.get(k, "") or "")
                    if val and (not cur or (k == "Image" and "placeholder" in cur)):
                        old_rec[k] = val
                        fixed += 1

        if page >= 10:
            capped.append(f"{category} / {sub}")
        page += 1
        time.sleep(random.uniform(2, 5))
    return added + fixed, len(seen_in_leaf)


failed = []
empty_leaves = []     
empty_streak = 0

for category, subs in CATEGORIES.items():
    print(f"\n===== {category} ({len(subs)} subcategories) =====")
    for sub, url in subs.items():
        if url in done:
            continue
        try:
            added, seen = scrape_leaf(category, sub, url)
        except Exception as e:
            print(f"!! {sub} failed: {e}")
            failed.append(f"{category} / {sub}")
            continue

        print("\r" + " " * 90 + "\r", end="")
        print(f"== {category} / {sub}: {added} new, {seen} seen (total {len(all_products)}) ==", flush=True)
        save_all()

        if seen == 0:
            
            empty_leaves.append(f"{category} / {sub}")
            empty_streak += 1
            if empty_streak >= 5:
                print("!! 5 leaves in a row with NO products on the page - probably blocked. title:", driver.title)
                raise SystemExit
        else:
            
            empty_streak = 0
            with open(DONE_FILE, "a", encoding="utf-8") as f:
                f.write(url + "\n")
            done.add(url)
        time.sleep(random.uniform(5, 10))

print("\nTotal products:", len(all_products))
print("Failed (re-run to retry):", failed)
print("Empty leaves (no products on page, will retry next run):", empty_leaves)
print("Hit the 10-page cap (split by brand/price):", capped)
