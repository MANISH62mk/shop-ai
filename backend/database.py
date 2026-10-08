import os
import json
import sqlite3
import datetime
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

try:
    from backend.expand_catalog import NEW_PRODUCTS as EXPANDED_PRODUCTS
except Exception:
    EXPANDED_PRODUCTS = []

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "shopai.db"

DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initial seed products data (32 items across 8 categories with INR pricing)
SEED_PRODUCTS = [
    # --- LAPTOPS ---
    {
        "name": "Acer Swift Go 14 OLED Thin & Light Laptop",
        "category": "Laptops",
        "brand": "Acer",
        "price": 56990.0,
        "stock_quantity": 8,
        "description": "Ultra-lightweight 1.25 kg laptop powered by 13th Gen Intel Core i5 with 16GB LPDDR5 RAM and 512GB NVMe SSD. Features stunning 2.8K OLED display, backlit keyboard, and 12-hour battery life. Ideal for coding, compilation, and college portability.",
        "rating": 4.6,
        "tags": "laptop, coding, programming, lightweight, thin, portable, student, python, developer, intel i5, 16gb ram, oled",
        "image_url": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Processor": "Intel Core i5-13500H (12 Cores, 16 Threads)",
            "RAM": "16 GB LPDDR5 4800MHz",
            "Storage": "512 GB PCIe Gen4 NVMe SSD",
            "Display": "14-inch 2.8K OLED 90Hz (100% DCI-P3)",
            "Weight": "1.25 kg (Ultra-light)",
            "Battery Life": "Up to 12 Hours",
            "OS": "Windows 11 Home + MS Office"
        })
    },
    {
        "name": "ASUS Vivobook 15 Thin & Light Laptop",
        "category": "Laptops",
        "brand": "ASUS",
        "price": 49990.0,
        "stock_quantity": 6,
        "description": "Sleek and portable 15.6-inch laptop with AMD Ryzen 5 7530U (6 cores / 12 threads), 16GB RAM, and 512GB SSD. Perfect balance of speed and battery life for web development, software engineering, and daily tasks under ₹50,000.",
        "rating": 4.4,
        "tags": "laptop, coding, programming, ryzen 5, 16gb ram, thin, budget, student, developer, lightweight",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Processor": "AMD Ryzen 5 7530U (6 Cores, 12 Threads, Up to 4.5GHz)",
            "RAM": "16 GB DDR4 3200MHz",
            "Storage": "512 GB M.2 NVMe SSD",
            "Display": "15.6-inch Full HD Anti-Glare (1920x1080)",
            "Weight": "1.7 kg",
            "Battery Life": "Up to 8 Hours",
            "OS": "Windows 11 Home"
        })
    },
    {
        "name": "Lenovo IdeaPad Slim 3 Gen 8",
        "category": "Laptops",
        "brand": "Lenovo",
        "price": 54490.0,
        "stock_quantity": 5,
        "description": "Engineered for smooth multitasking and software development. Features 13th Gen Intel Core i5-13420H, 16GB RAM, rapid charge (80% in 60 min), and military-grade durability weighing only 1.43 kg.",
        "rating": 4.5,
        "tags": "laptop, coding, programming, lightweight, lenovo, slim, developer, student, portable, 16gb ram",
        "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Processor": "Intel Core i5-13420H 8-Core",
            "RAM": "16 GB LPDDR5 4800MHz",
            "Storage": "512 GB NVMe SSD",
            "Display": "15.0-inch FHD IPS 300 nits",
            "Weight": "1.43 kg",
            "Battery Life": "Up to 10 Hours",
            "OS": "Windows 11 Home"
        })
    },
    {
        "name": "HP Pavilion 14 Ergonomic Laptop",
        "category": "Laptops",
        "brand": "HP",
        "price": 58990.0,
        "stock_quantity": 4,
        "description": "Premium aluminum finish laptop equipped with Intel Core i5 12th Gen, 16GB dual-channel RAM, B&O audio, and backlit keyboard. Highly responsive for IDEs like VS Code, IntelliJ, and Docker containers under ₹60,000.",
        "rating": 4.5,
        "tags": "laptop, coding, programming, hp, lightweight, 14 inch, student, developer, portable, compact",
        "image_url": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Processor": "Intel Core i5-1235U (10 Cores, Up to 4.4GHz)",
            "RAM": "16 GB DDR4-3200MHz",
            "Storage": "512 GB PCIe NVMe M.2 SSD",
            "Display": "14-inch FHD IPS Micro-edge Display",
            "Weight": "1.41 kg",
            "Battery Life": "Up to 9 Hours",
            "OS": "Windows 11 Home"
        })
    },
    {
        "name": "ASUS TUF Gaming F15",
        "category": "Laptops",
        "brand": "ASUS",
        "price": 68990.0,
        "stock_quantity": 4,
        "description": "High performance gaming laptop featuring 12th Gen Intel Core i5-12500H, NVIDIA GeForce RTX 3050 4GB GPU, 16GB RAM, and 144Hz IPS display. Built for gaming enthusiasts and heavy GPU rendering tasks.",
        "rating": 4.7,
        "tags": "laptop, gaming, rtx 3050, high performance, asus tuf, dedicated gpu, 144hz, games, steam",
        "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Processor": "Intel Core i5-12500H (12 Cores, 16 Threads)",
            "Graphics": "NVIDIA GeForce RTX 3050 4GB GDDR6",
            "RAM": "16 GB DDR4 3200MHz",
            "Storage": "512 GB PCIe 4.0 SSD",
            "Display": "15.6-inch FHD 144Hz Adaptive-Sync",
            "Weight": "2.20 kg",
            "Battery Life": "Up to 5 Hours"
        })
    },
    {
        "name": "Acer Aspire 5 Slim Edition (Demo Item)",
        "category": "Laptops",
        "brand": "Acer",
        "price": 52990.0,
        "stock_quantity": 0, # Intentionally set to 0 to demonstrate out-of-stock alternative recommendation!
        "description": "Budget-friendly thin productivity notebook featuring 12th Gen Intel Core i5 with 16GB RAM and fast NVMe storage. (Currently Out of Stock for testing recommendation fallback).",
        "rating": 4.2,
        "tags": "laptop, coding, programming, lightweight, budget, out of stock test",
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Processor": "Intel Core i5-1235U",
            "RAM": "16 GB DDR4",
            "Storage": "512 GB SSD",
            "Display": "15.6-inch FHD IPS",
            "Weight": "1.78 kg",
            "Stock Status": "Out of Stock"
        })
    },

    # --- SMARTPHONES ---
    {
        "name": "Redmi Note 13 Pro 5G (200MP OIS Camera)",
        "category": "Smartphones",
        "brand": "Xiaomi",
        "price": 24999.0,
        "stock_quantity": 9,
        "description": "Pro-grade mobile photography with flagship 200MP Samsung ISOCELL sensor with Optical Image Stabilization (OIS). Features 1.5K 120Hz AMOLED curved display, Snapdragon 7s Gen 2, and 67W Turbo Charge.",
        "rating": 4.6,
        "tags": "smartphone, phone, camera, 200mp, ois, photography, photos, 5g, amoled, redmi, under 25000",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Main Camera": "200 MP Samsung HP3 with OIS + 8MP Ultra-wide + 2MP Macro",
            "Selfie Camera": "16 MP HDR",
            "Processor": "Qualcomm Snapdragon 7s Gen 2 (4nm)",
            "Display": "6.67-inch 1.5K 120Hz Curved AMOLED Dolby Vision",
            "Battery": "5100 mAh with 67W Fast Charging",
            "RAM / Storage": "8GB RAM + 128GB Storage"
        })
    },
    {
        "name": "Realme 12 Pro 5G (Sony IMX882 OIS)",
        "category": "Smartphones",
        "brand": "Realme",
        "price": 23999.0,
        "stock_quantity": 7,
        "description": "Luxury watch design with 50MP Sony IMX882 sensor with OIS and 32MP telephoto portrait camera. Provides unmatched portrait clarity and cinematic bokeh effects under ₹25,000.",
        "rating": 4.5,
        "tags": "smartphone, phone, camera, sony sensor, ois, portrait, photography, 5g, realme, under 25000",
        "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Main Camera": "50 MP Sony IMX882 OIS + 32MP Telephoto 2x Optical Zoom",
            "Selfie Camera": "16 MP Ultra Clear",
            "Processor": "Qualcomm Snapdragon 6 Gen 1",
            "Display": "6.7-inch 120Hz Curved Vision OLED",
            "Battery": "5000 mAh with 67W SuperVOOC Charge",
            "RAM / Storage": "8GB RAM + 256GB Storage"
        })
    },
    {
        "name": "OnePlus Nord CE 3 5G",
        "category": "Smartphones",
        "brand": "OnePlus",
        "price": 22999.0,
        "stock_quantity": 10,
        "description": "Smooth OxygenOS experience powered by Snapdragon 782G with flagship Sony IMX890 50MP OIS camera, 80W SUPERVOOC charging, and vibrant 120Hz Fluid AMOLED display.",
        "rating": 4.4,
        "tags": "smartphone, phone, camera, oneplus, nord, smooth, 5g, ois, oxygenos, under 25000",
        "image_url": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Camera": "50 MP Sony IMX890 OIS + 8MP Ultra-wide + 2MP Macro",
            "Processor": "Qualcomm Snapdragon 782G 5G",
            "Display": "6.7-inch 120Hz Fluid AMOLED",
            "Charging": "80W SUPERVOOC (1-100% in 31 mins)",
            "RAM / Storage": "8GB RAM + 128GB Storage"
        })
    },
    {
        "name": "Samsung Galaxy M34 5G Monster Battery",
        "category": "Smartphones",
        "brand": "Samsung",
        "price": 18999.0,
        "stock_quantity": 12,
        "description": "Massive 6000mAh battery for two-day stamina with 50MP No-Shake Cam (OIS), 120Hz Super AMOLED display, and Knox security.",
        "rating": 4.3,
        "tags": "smartphone, phone, battery, samsung, 6000mah, long battery life, camera, 5g, amoled",
        "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Battery": "6000 mAh Monster Battery",
            "Camera": "50 MP OIS Triple Camera",
            "Display": "6.5-inch FHD+ 120Hz Super AMOLED",
            "Processor": "Exynos 1280 5nm Octa-core",
            "RAM / Storage": "6GB RAM + 128GB Storage"
        })
    },

    # --- HEADPHONES ---
    {
        "name": "boAt Rockerz 550 Over-Ear Wireless Headphones",
        "category": "Headphones",
        "brand": "boAt",
        "price": 1999.0,
        "stock_quantity": 15,
        "description": "Comfortable wireless over-ear headphones featuring 50mm dynamic drivers, punchy bass, Bluetooth 5.0, physical playback controls, and 20 hours playback.",
        "rating": 4.3,
        "tags": "headphones, wireless, bluetooth, over ear, bass, boat, under 3000, under 2000, audio, mic",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Driver Size": "50 mm Dynamic Drivers",
            "Battery Life": "20 Hours Playback",
            "Connectivity": "Bluetooth v5.0 & 3.5mm AUX Cable",
            "Weight": "245 grams",
            "Microphone": "Built-in with Voice Assistant support"
        })
    },
    {
        "name": "Noise Two Wireless Bluetooth Headphones",
        "category": "Headphones",
        "brand": "Noise",
        "price": 1799.0,
        "stock_quantity": 12,
        "description": "Lightweight foldable design with deep bass, low latency mode for casual gaming, dual pairing, FM radio, and up to 50 hours of battery life under ₹2,000.",
        "rating": 4.2,
        "tags": "headphones, wireless, bluetooth, low latency, noise, budget, long battery, under 3000",
        "image_url": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Battery Life": "Up to 50 Hours Playtime",
            "Latency": "40ms Low Latency Gaming Mode",
            "Bluetooth": "v5.3 with Dual Device Pairing",
            "Driver": "40 mm Speaker Drivers",
            "Controls": "Tactile On-ear Buttons"
        })
    },
    {
        "name": "OnePlus Bullets Wireless Z2 Neckband",
        "category": "Headphones",
        "brand": "OnePlus",
        "price": 1999.0,
        "stock_quantity": 18,
        "description": "High performance magnetic wireless neckband with 12.4mm bass drivers, IP55 sweat resistance, and warp charge giving 20 hours of music in 10 minutes.",
        "rating": 4.6,
        "tags": "headphones, earphones, wireless, neckband, bluetooth, oneplus, bass, fast charging, under 3000",
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Drivers": "12.4 mm Bass Driver",
            "Battery": "30 Hours total playtime",
            "Fast Charge": "10 min charge = 20 hours audio",
            "Water Resistance": "IP55 Water & Sweat Resistance"
        })
    },
    {
        "name": "Sony WH-CH520 Wireless On-Ear Headphones",
        "category": "Headphones",
        "brand": "Sony",
        "price": 4490.0,
        "stock_quantity": 10,
        "description": "Exceptional audio fidelity featuring DSEE sound upscaling, 360 Reality Audio, multipoint connection, and 50-hour battery life with premium memory foam ear cushions.",
        "rating": 4.7,
        "tags": "headphones, wireless, bluetooth, sony, high quality, audio, studio, long battery life",
        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Battery Life": "Up to 50 Hours",
            "Sound Enhancement": "DSEE Sound Enhancement Engine",
            "Connectivity": "Bluetooth 5.2 Multipoint (2 Devices)",
            "Microphone": "Crystal Clear Hands-free with EQ customization"
        })
    },

    # --- KEYBOARDS ---
    {
        "name": "Redragon K552 Kumara RGB Mechanical Gaming Keyboard",
        "category": "Keyboards",
        "brand": "Redragon",
        "price": 2799.0,
        "stock_quantity": 14,
        "description": "Tactile blue switch mechanical keyboard with durable aircraft-grade aluminum chassis, 87 tenkeyless keys, rainbow RGB backlighting, and anti-ghosting. Superb for programming and gaming feedback.",
        "rating": 4.6,
        "tags": "keyboard, mechanical, blue switch, coding, gaming, typing, rgb, tactile, developer",
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Switch Type": "Custom Mechanical Blue Switches (Clicky & Tactile)",
            "Layout": "Tenkeyless 87 Keys (TKL)",
            "Backlighting": "18 RGB Backlight Modes",
            "Keycaps": "Double-shot Injection Molded",
            "Connection": "Gold-plated USB-A Cable"
        })
    },
    {
        "name": "Logitech K380 Multi-Device Bluetooth Keyboard",
        "category": "Keyboards",
        "brand": "Logitech",
        "price": 2995.0,
        "stock_quantity": 11,
        "description": "Compact, minimalist wireless keyboard with scooped keys for whisper-quiet typing. Switches effortlessly between laptop, tablet, and phone with Easy-Switch keys. 2-year battery life.",
        "rating": 4.6,
        "tags": "keyboard, wireless, bluetooth, logitech, portable, quiet, typing, coding, compact, multi-device",
        "image_url": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Connectivity": "Bluetooth Low Energy 4.2",
            "Compatibility": "Windows, macOS, Chrome OS, Android, iOS",
            "Battery Life": "24 Months (2x AAA included)",
            "Dimensions": "279 x 124 x 16 mm (423g)"
        })
    },
    {
        "name": "Keychron K2 Wireless Mechanical Keyboard (Brown Switch)",
        "category": "Keyboards",
        "brand": "Keychron",
        "price": 7999.0,
        "stock_quantity": 6,
        "description": "Premium 75% mechanical keyboard designed for Mac and Windows software engineers. Features hot-swappable Gateron G Pro Brown tactile switches, 4000mAh battery, and wireless/wired mode.",
        "rating": 4.8,
        "tags": "keyboard, mechanical, keychron, developer, coding, brown switch, mac, windows, wireless, tactile",
        "image_url": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Switches": "Gateron G Pro Brown (Gentle Tactile)",
            "Layout": "75% Compact 84 Keys",
            "Battery": "4000 mAh Rechargeable (Up to 240 hrs without backlight)",
            "OS Layout": "Dedicated Mac and Windows Keycaps included"
        })
    },

    # --- MONITORS ---
    {
        "name": "BenQ GW2480 24-inch Eye-Care IPS Monitor",
        "category": "Monitors",
        "brand": "BenQ",
        "price": 8990.0,
        "stock_quantity": 8,
        "description": "The gold standard for programmers and students. 24-inch Full HD IPS panel with Brightness Intelligence sensor that auto-adjusts screen brightness, zero-flicker technology, and low blue light for fatigue-free coding.",
        "rating": 4.5,
        "tags": "monitor, coding, programming, ips, eye care, benq, 24 inch, anti-glare, screen, display",
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Screen Size": "23.8 inch Full HD (1920x1080) IPS",
            "Refresh Rate": "60Hz / 75Hz",
            "Eye-Care Tech": "Brightness Intelligence, Low Blue Light Plus, Flicker-Free",
            "Ports": "HDMI, DisplayPort, VGA, Audio In/Out",
            "Speakers": "Built-in 2W x 2 Stereo Speakers"
        })
    },
    {
        "name": "Dell 24-inch Professional FHD IPS Monitor (P2422H)",
        "category": "Monitors",
        "brand": "Dell",
        "price": 13990.0,
        "stock_quantity": 5,
        "description": "Ergonomic coding monitor with pivot, tilt, swivel, and height adjustable stand. Allows 90-degree vertical rotation for full-page code editing. Features ComfortView Plus blue light reduction.",
        "rating": 4.7,
        "tags": "monitor, coding, programming, vertical, pivot, dell, ergonomic, ips, 24 inch, developer",
        "image_url": "https://images.unsplash.com/photo-1547119957-637f8679db1e?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Panel": "23.8 inch IPS Anti-Glare 99% sRGB",
            "Stand": "Height adjustable (150 mm), Pivot (90° vertical), Swivel, Tilt",
            "Connectivity": "HDMI, DisplayPort, VGA, 4x USB 3.2 Hub Ports",
            "Eye Comfort": "TÜV Rheinland Certified ComfortView Plus"
        })
    },
    {
        "name": "LG Ultragear 24-inch 144Hz Gaming Monitor",
        "category": "Monitors",
        "brand": "LG",
        "price": 11490.0,
        "stock_quantity": 7,
        "description": "Fast 1ms MBR response time with 144Hz refresh rate, AMD FreeSync Premium, and 99% sRGB color gamut. Ideal for fast-paced gaming and dual-monitor creative setups.",
        "rating": 4.6,
        "tags": "monitor, gaming, 144hz, 1ms, lg, ips, freesync, esports, display",
        "image_url": "https://images.unsplash.com/photo-1551645120-d70bfe84c826?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Resolution": "1920 x 1080 FHD IPS",
            "Refresh Rate": "144 Hz with AMD FreeSync",
            "Response Time": "1ms MBR",
            "Color Gamut": "sRGB 99% (CIE1931)"
        })
    },

    # --- SMARTWATCHES ---
    {
        "name": "Noise ColorFit Pulse 2 Max Smartwatch",
        "category": "Smartwatches",
        "brand": "Noise",
        "price": 1499.0,
        "stock_quantity": 16,
        "description": "1.85-inch bright TFT display with Tru Sync Bluetooth calling, 100 sports modes, SpO2 & 24/7 heart rate monitor, IP68 water resistance, and 10-day battery life.",
        "rating": 4.2,
        "tags": "smartwatch, watch, bluetooth calling, fitness, noise, heart rate, under 2000, sports",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Display": "1.85 inch 550 nits Bright Display",
            "Calling": "Bluetooth Calling with Dial Pad & Recent Calls",
            "Sensors": "Heart Rate, SpO2, Sleep Tracker, Stress Monitor",
            "Battery": "Up to 10 Days (3 Days with BT Calling)"
        })
    },
    {
        "name": "Amazfit Bip 3 Pro GPS Smartwatch",
        "category": "Smartwatches",
        "brand": "Amazfit",
        "price": 3999.0,
        "stock_quantity": 9,
        "description": "Standalone 4 satellite positioning GPS system, 1.69-inch large color display, 5 ATM water resistance for swimming, 60+ sports modes, and 14 days ultra-long battery life.",
        "rating": 4.5,
        "tags": "smartwatch, watch, gps, running, amazfit, fitness, swimming, long battery",
        "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Positioning": "Built-in 4 Satellite GPS",
            "Water Resistance": "5 ATM (50 meters water resistant)",
            "Battery": "14 Days Typical Usage",
            "Health Engine": "BioTracker 2 PPG Biometric Sensor"
        })
    },
    {
        "name": "Samsung Galaxy Watch 4 Bluetooth",
        "category": "Smartwatches",
        "brand": "Samsung",
        "price": 9999.0,
        "stock_quantity": 5,
        "description": "Wear OS powered by Samsung with Google Play Store app access, body composition BIA analysis, optical heart sensor, ECG tracker, and sleek aluminum armor frame.",
        "rating": 4.6,
        "tags": "smartwatch, watch, wear os, samsung, premium, apps, health, ecg",
        "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "OS": "Wear OS Powered by Samsung",
            "Body Analysis": "BioActive Sensor (BIA Body Fat, Skeletal Muscle, Water %)",
            "Display": "Super AMOLED 1.2-inch Always On",
            "Connectivity": "Bluetooth 5.0, Wi-Fi, NFC, GPS"
        })
    },

    # --- TABLETS ---
    {
        "name": "Samsung Galaxy Tab A9+ Wi-Fi (11-inch)",
        "category": "Tablets",
        "brand": "Samsung",
        "price": 18999.0,
        "stock_quantity": 8,
        "description": "Expansive 11.0-inch 90Hz display with quad speakers powered by Dolby Atmos. Powered by Qualcomm Snapdragon 695 with Samsung DeX mode for desktop-like multitasking and study.",
        "rating": 4.5,
        "tags": "tablet, tab, samsung, student, reading, dex, 11 inch, 90hz, study, movies",
        "image_url": "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Display": "11.0 inch 90Hz WQXGA (1920x1200)",
            "Processor": "Qualcomm Snapdragon 695 5G Octa-Core",
            "Audio": "Quad Speakers tuned by Dolby Atmos",
            "Multitasking": "Samsung DeX Multi-Window (up to 3 apps)",
            "Battery": "7040 mAh with 15W Fast Charge"
        })
    },
    {
        "name": "Xiaomi Pad 6 (Snapdragon 870)",
        "category": "Tablets",
        "brand": "Xiaomi",
        "price": 24999.0,
        "stock_quantity": 6,
        "description": "High-tier tablet with 144Hz 2.8K display, Snapdragon 870 powerhouse processor, aluminum unibody, and 8840mAh battery. Excellent for note-taking, sketching, and programming web previews.",
        "rating": 4.7,
        "tags": "tablet, tab, xiaomi, 144hz, snapdragon 870, student, high performance, stylus support",
        "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Display": "11-inch 2.8K 144Hz IPS Dolby Vision HDR10",
            "Processor": "Snapdragon 870 Flagship 7nm",
            "Battery": "8840 mAh with 33W Fast Charger included",
            "Weight": "490 grams (Ultra slim 6.51mm)"
        })
    },
    {
        "name": "Apple iPad 10th Generation (A14 Bionic)",
        "category": "Tablets",
        "brand": "Apple",
        "price": 34900.0,
        "stock_quantity": 5,
        "description": "Striking all-screen design with 10.9-inch Liquid Retina display, blazing fast A14 Bionic chip, landscape 12MP Ultra-Wide front camera, and USB-C connectivity.",
        "rating": 4.8,
        "tags": "tablet, ipad, apple, ios, a14 bionic, student, note taking, drawing, premium",
        "image_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Chip": "A14 Bionic with 6-core CPU and 4-core GPU",
            "Display": "10.9-inch Liquid Retina True Tone",
            "Cameras": "12MP Wide back, 12MP Ultra Wide front Center Stage",
            "Security": "Touch ID integrated in top power button"
        })
    },

    # --- ACCESSORIES ---
    {
        "name": "Portronics Adjustable Aluminum Laptop Stand",
        "category": "Accessories",
        "brand": "Portronics",
        "price": 799.0,
        "stock_quantity": 25,
        "description": "Ergonomic foldable aluminum laptop riser with 7 adjustable height levels and silicone non-slip pads. Improves posture and heat dissipation for programmers working long hours.",
        "rating": 4.5,
        "tags": "accessories, laptop stand, ergonomic, aluminum, riser, desk setup, coding, cooling",
        "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Material": "Anodized Aluminum Alloy",
            "Adjustability": "7 Levels (from 15° to 45° angle)",
            "Compatibility": "Laptops & Tablets up to 15.6 inches",
            "Folded Weight": "260 grams"
        })
    },
    {
        "name": "Logitech B170 Wireless Optical Mouse",
        "category": "Accessories",
        "brand": "Logitech",
        "price": 599.0,
        "stock_quantity": 30,
        "description": "Reliable 2.4GHz wireless mouse with nano USB receiver, 10-meter range, smooth optical tracking, and 12-month battery life. Ambidextrous shape fits left and right hands comfortably.",
        "rating": 4.4,
        "tags": "accessories, mouse, wireless, logitech, optical, usb, budget, office, coding",
        "image_url": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Connection": "2.4 GHz USB Nano Wireless Receiver",
            "Battery": "1x AA Battery (up to 12 months)",
            "Sensor": "1000 DPI Optical Tracking",
            "Range": "Up to 10 meters"
        })
    },
    {
        "name": "Anker 65W GaN II 3-Port Fast Charger",
        "category": "Accessories",
        "brand": "Anker",
        "price": 3299.0,
        "stock_quantity": 14,
        "description": "Pocket-sized Gallium Nitride (GaN) fast charger with 2 USB-C and 1 USB-A port. Can fast charge a laptop, phone, and earbuds simultaneously with PowerIQ 3.0 technology.",
        "rating": 4.7,
        "tags": "accessories, charger, gan, 65w, fast charging, usb-c, anker, laptop charger, travel",
        "image_url": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Total Output": "65W Max",
            "Ports": "2x USB-C (Power Delivery) + 1x USB-A (PowerIQ)",
            "Technology": "GaN II (Gallium Nitride, cooler and 59% smaller)",
            "Safety": "ActiveShield Intelligent Temperature Monitoring"
        })
    },
    {
        "name": "SanDisk Extreme 128GB High-Speed USB 3.2 Flash Drive",
        "category": "Accessories",
        "brand": "SanDisk",
        "price": 1299.0,
        "stock_quantity": 22,
        "description": "High performance USB 3.2 Gen 1 thumb drive with transfer speeds up to 150MB/s. Includes SanDisk SecureAccess 128-bit AES encryption software for safe backup of project files.",
        "rating": 4.5,
        "tags": "accessories, pen drive, usb, storage, sandisk, flash drive, 128gb, backup",
        "image_url": "https://images.unsplash.com/photo-1563770660941-20978e870e26?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Capacity": "128 GB",
            "Interface": "USB 3.2 Gen 1 (Backwards compatible with USB 2.0)",
            "Read Speed": "Up to 150 MB/s",
            "Security": "128-bit AES Encryption password protection"
        })
    },
    {
        "name": "TP-Link USB Wi-Fi Adapter 300Mbps",
        "category": "Accessories",
        "brand": "TP-Link",
        "price": 499.0,
        "stock_quantity": 18,
        "description": "Miniature high-speed wireless USB dongle offering 300Mbps transmission rates for desktop PCs and laptops with weak antenna reception. Plug and play on modern OS.",
        "rating": 4.3,
        "tags": "accessories, wifi, adapter, tp-link, usb, wireless, network, dongle",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Speed": "Up to 300 Mbps (2.4 GHz)",
            "Form Factor": "Miniature thumb-size design",
            "Security": "Supports 64/128 WEP, WPA/WPA2 encryption",
            "Compatibility": "Windows 11/10/8.1/8/7, Linux"
        })
    }
]

def init_db():
    from backend.models import Base, User, Product, Order, OrderItem
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if users exist
        admin_user = db.query(User).filter(User.email == "admin@shopai.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@shopai.com",
                password_hash="admin123", # Plain for college demo authentication
                name="Admin Manager",
                role="admin"
            )
            db.add(admin_user)

        demo_user = db.query(User).filter(User.email == "demo@shopai.com").first()
        if not demo_user:
            demo_user = User(
                email="demo@shopai.com",
                password_hash="demo123",
                name="Demo Student Customer",
                role="customer"
            )
            db.add(demo_user)

        db.commit()

        # Check products count
        count = db.query(Product).count()
        if count == 0:
            all_items = SEED_PRODUCTS + [p for p in EXPANDED_PRODUCTS if p["name"] not in [x["name"] for x in SEED_PRODUCTS]]
            for item in all_items:
                p = Product(
                    name=item["name"],
                    category=item["category"],
                    brand=item["brand"],
                    price=item["price"],
                    stock_quantity=item["stock_quantity"],
                    description=item["description"],
                    rating=item["rating"],
                    tags=item["tags"],
                    image_url=item["image_url"],
                    specs=item.get("specs", "{}"),
                    created_at=datetime.datetime.utcnow()
                )
                db.add(p)
            db.commit()
            print(f"Initialized database with {len(all_items)} seed products across all categories.")

            # Seed a couple of historical demo orders for the sales chart to look great immediately
            p1 = db.query(Product).filter(Product.name.like("%Acer Swift%")).first()
            p2 = db.query(Product).filter(Product.name.like("%Redragon%")).first()
            p3 = db.query(Product).filter(Product.name.like("%boAt%")).first()

            if p1 and p2 and p3:
                demo_order = Order(
                    user_id=demo_user.id if demo_user else None,
                    customer_name="Rohan Verma",
                    customer_email="rohan@example.com",
                    customer_phone="+91 9876543210",
                    shipping_address="42 MG Road, Koramangala, Bengaluru, Karnataka 560034",
                    payment_method="Demo Card Payment",
                    total_amount=p1.price + p2.price,
                    status="Confirmed"
                )
                db.add(demo_order)
                db.commit()

                db.add(OrderItem(
                    order_id=demo_order.id,
                    product_id=p1.id,
                    product_name=p1.name,
                    unit_price=p1.price,
                    quantity=1,
                    subtotal=p1.price
                ))
                db.add(OrderItem(
                    order_id=demo_order.id,
                    product_id=p2.id,
                    product_name=p2.name,
                    unit_price=p2.price,
                    quantity=1,
                    subtotal=p2.price
                ))

                demo_order_2 = Order(
                    user_id=demo_user.id if demo_user else None,
                    customer_name="Priya Sharma",
                    customer_email="priya@example.com",
                    customer_phone="+91 9812345678",
                    shipping_address="102 Park Street, Kolkata, West Bengal 700016",
                    payment_method="Cash on Delivery",
                    total_amount=p3.price * 2,
                    status="Delivered"
                )
                db.add(demo_order_2)
                db.commit()

                db.add(OrderItem(
                    order_id=demo_order_2.id,
                    product_id=p3.id,
                    product_name=p3.name,
                    unit_price=p3.price,
                    quantity=2,
                    subtotal=p3.price * 2
                ))
                db.commit()

    finally:
        db.close()

if __name__ == "__main__":
    init_db()
