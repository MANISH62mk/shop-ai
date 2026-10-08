import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "shopai.db"

NEW_PRODUCTS = [
    # ==========================================
    # 1. CLOTHING (8 items)
    # ==========================================
    {
        "name": "Allen Solly Men's Slim Fit 100% Pure Cotton Shirt",
        "category": "Clothing",
        "brand": "Allen Solly",
        "price": 1199.0,
        "stock_quantity": 14,
        "description": "Premium 100% breathable pure cotton formal and casual button-down shirt. Features curved hem, point collar, and comfortable slim fit tailored for work and weekend outings under ₹1,500.",
        "rating": 4.5,
        "tags": "clothing, shirt, shirts, cotton, pure cotton, cotton shirt, slim fit, casual, formal, breathable, under 1500",
        "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Fabric": "100% Pure Cotton",
            "Fit": "Slim Fit",
            "Collar": "Classic Spread Collar",
            "Sleeve": "Long Sleeves with Button Cuffs",
            "Care Instructions": "Machine Wash Warm"
        })
    },
    {
        "name": "Peter England Casual Breathable Pure Cotton Shirt",
        "category": "Clothing",
        "brand": "Peter England",
        "price": 1349.0,
        "stock_quantity": 16,
        "description": "Soft pre-washed 100% cotton casual shirt featuring micro-check pattern, lightweight breathable weave, and regular comfort fit for tropical weather under ₹1,500.",
        "rating": 4.4,
        "tags": "clothing, shirt, shirts, cotton, cotton shirt, casual, peter england, breathable, summer wear, under 1500",
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Fabric": "100% Combed Cotton",
            "Fit": "Regular Fit",
            "Pattern": "Subtle Micro Check",
            "Closure": "Full Button Placket",
            "Hemline": "Curved"
        })
    },
    {
        "name": "US Polo Assn Solid Casual Cotton Shirt",
        "category": "Clothing",
        "brand": "U.S. Polo Assn.",
        "price": 1449.0,
        "stock_quantity": 12,
        "description": "Authentic casual long-sleeve cotton shirt with signature embroidered chest logo, soft garment wash, and durable double-stitched seams under ₹1,500.",
        "rating": 4.6,
        "tags": "clothing, shirt, shirts, cotton, cotton shirt, casual shirt, us polo, under 1500, solid",
        "image_url": "https://images.unsplash.com/photo-1603252109303-2751441dd157?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Material": "100% Premium Twill Cotton",
            "Fit": "Tailored Fit",
            "Pocket": "Single Chest Pocket with Logo",
            "Style": "Casual / Smart Casual"
        })
    },
    {
        "name": "H&M Regular Fit Oxford Cotton Shirt",
        "category": "Clothing",
        "brand": "H&M",
        "price": 1499.0,
        "stock_quantity": 10,
        "description": "Timeless Oxford weave shirt crafted from pure organic cotton with a button-down collar, chest patch pocket, and round hem under ₹1,500.",
        "rating": 4.3,
        "tags": "clothing, shirt, shirts, cotton, oxford shirt, cotton shirt, hm, under 1500, smart casual",
        "image_url": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Fabric": "100% Organic Oxford Cotton",
            "Collar": "Button-Down Collar",
            "Fit": "Regular Fit",
            "Color": "Classic Light Blue"
        })
    },
    {
        "name": "Fabindia Handwoven Pure Cotton Long Kurta Shirt",
        "category": "Clothing",
        "brand": "Fabindia",
        "price": 1399.0,
        "stock_quantity": 9,
        "description": "Traditional handloom pure cotton kurta shirt with mandarin collar, side pockets, and fine artisan weave. Highly comfortable and breathable under ₹1,500.",
        "rating": 4.7,
        "tags": "clothing, kurta, shirt, cotton, handwoven, fabindia, ethnic, breathable, under 1500",
        "image_url": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Weave": "Handspun Cotton",
            "Collar": "Mandarin / Chinese Collar",
            "Length": "Mid-Thigh Long Kurta",
            "Pockets": "Two Slit Side Pockets"
        })
    },
    {
        "name": "Raymond Luxury Formal Pure Cotton Shirt",
        "category": "Clothing",
        "brand": "Raymond",
        "price": 1899.0,
        "stock_quantity": 8,
        "description": "High-thread-count Egyptian Giza cotton executive shirt with French placket, semi-cutaway collar, and stain-resistant finish for boardrooms.",
        "rating": 4.7,
        "tags": "clothing, shirt, cotton, formal, raymond, luxury, executive, business",
        "image_url": "https://images.unsplash.com/photo-1620012253295-c15c429f66bf?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Material": "100% Giza Long-Staple Cotton",
            "Fit": "Contemporary Fit",
            "Collar": "Semi Cutaway Collar",
            "Cuff": "Chiseled Double Button Cuffs"
        })
    },
    {
        "name": "Levi's Men's 511 Slim Fit Stretch Denim Jeans",
        "category": "Clothing",
        "brand": "Levi's",
        "price": 2499.0,
        "stock_quantity": 15,
        "description": "Iconic modern slim jeans with room to move. Crafted with premium stretch denim, 5-pocket styling, and authentic copper rivets.",
        "rating": 4.6,
        "tags": "clothing, jeans, denim, pants, levis, 511, slim fit, stretch, casual",
        "image_url": "https://images.unsplash.com/photo-1542272604-780c96856592?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Fabric": "98% Cotton, 2% Elastane",
            "Fit": "Slim from Hip to Ankle",
            "Fly": "Zip Fly with Shank Button Closure",
            "Rise": "Mid Rise"
        })
    },
    {
        "name": "Zara Relaxed Fit Pure Linen Summer Casual Shirt",
        "category": "Clothing",
        "brand": "Zara",
        "price": 2290.0,
        "stock_quantity": 7,
        "description": "Breezy pure European linen shirt designed with a camp collar, short sleeves, and relaxed drape for resort and summer styling.",
        "rating": 4.5,
        "tags": "clothing, shirt, linen, casual, summer, zara, relaxed, stylish",
        "image_url": "https://images.unsplash.com/photo-1563630423918-b58f07336ac9?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Material": "100% European Flax Linen",
            "Fit": "Relaxed Camp Fit",
            "Sleeve": "Short Sleeve",
            "Collar": "Resort Notch Collar"
        })
    },

    # ==========================================
    # 2. SHOES (8 items)
    # ==========================================
    {
        "name": "Puma Velocity Nitro Lightweight Running Shoes",
        "category": "Shoes",
        "brand": "Puma",
        "price": 2799.0,
        "stock_quantity": 14,
        "description": "Responsive road running shoes featuring advanced NITRO foam cushioning, engineered breathable mesh upper, and PUMAGRIP durable rubber outsole under ₹3,000.",
        "rating": 4.6,
        "tags": "shoes, shoe, running shoes, running shoe, puma, nitro, running, sneakers, under 3000, athletic",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Cushioning": "NITRO Foam Technology",
            "Upper": "Engineered Breathable Mesh",
            "Outsole": "PUMAGRIP High-Traction Rubber",
            "Drop": "8 mm Heel-to-Toe Drop",
            "Weight": "250g per shoe"
        })
    },
    {
        "name": "Nike Revolution 6 Breathable Road Running Shoes",
        "category": "Shoes",
        "brand": "Nike",
        "price": 2995.0,
        "stock_quantity": 11,
        "description": "Minimalist design with soft foam midsole delivering smooth cushioning for daily 5k and 10k runs. Lightweight mesh keeps feet cool under ₹3,000.",
        "rating": 4.5,
        "tags": "shoes, shoe, running shoes, running, nike, revolution 6, road running, under 3000",
        "image_url": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Midsole": "Plush Foam Cushioning",
            "Heel Pods": "Padded Heel Collar for Achilles Support",
            "Outsole": "Computer-Generated Traction Pattern",
            "Weight": "265g"
        })
    },
    {
        "name": "Adidas Runfalcon 3.0 Cushioning Running Shoes",
        "category": "Shoes",
        "brand": "Adidas",
        "price": 2899.0,
        "stock_quantity": 13,
        "description": "Cloudfoam midsole provides pillow-soft step-in comfort for track and treadmill workouts with grippy rubber outsole under ₹3,000.",
        "rating": 4.5,
        "tags": "shoes, shoe, running shoes, running, adidas, runfalcon, cloudfoam, under 3000",
        "image_url": "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Midsole": "Cloudfoam Shock-Absorbing Unit",
            "Upper": "Textile Knit with 50% Recycled Content",
            "Fit": "Regular Fit with Lace Closure",
            "Ideal For": "Daily Jogging & Treadmill"
        })
    },
    {
        "name": "Reebok Floatride Energy Daily Running Shoes",
        "category": "Shoes",
        "brand": "Reebok",
        "price": 2499.0,
        "stock_quantity": 10,
        "description": "Lightweight performance trainers with Floatride Energy foam for smooth energy return on every stride under ₹3,000.",
        "rating": 4.4,
        "tags": "shoes, shoe, running shoes, running, reebok, floatride, lightweight, under 3000",
        "image_url": "https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Foam": "Floatride Energy Midsole",
            "Sockliner": "Molded EVA Cushion",
            "Outer Material": "Breathable Jacquard Mesh"
        })
    },
    {
        "name": "Campus North Plus Responsive Running Shoes",
        "category": "Shoes",
        "brand": "Campus",
        "price": 1499.0,
        "stock_quantity": 20,
        "description": "Budget road runners with Springy Fit sole, anti-skid bottom, and memory tech insole for morning walks and sprints under ₹1,500.",
        "rating": 4.3,
        "tags": "shoes, shoe, running shoes, running, campus, budget, under 3000, under 1500",
        "image_url": "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Sole": "Phylon Anti-Skid Sole",
            "Insole": "Memory Foam Insole",
            "Closure": "Lace-Up",
            "Weight": "220g"
        })
    },
    {
        "name": "Sparx Sporty Mesh Lightweight Running Shoes",
        "category": "Shoes",
        "brand": "Sparx",
        "price": 1299.0,
        "stock_quantity": 25,
        "description": "Ultra-lightweight mesh runners with flexible EVA grooved sole for natural foot motion during gym training and running.",
        "rating": 4.3,
        "tags": "shoes, shoe, running shoes, running, sparx, athletic, under 3000, under 1500",
        "image_url": "https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Upper": "Air Mesh",
            "Sole": "Flexible EVA Grooves",
            "Color": "Navy Blue / Neon Orange"
        })
    },
    {
        "name": "Asics Gel-Contend 8 Engineered Mesh Running Shoes",
        "category": "Shoes",
        "brand": "Asics",
        "price": 3499.0,
        "stock_quantity": 8,
        "description": "Rearfoot GEL technology cushioning reduces impact shock, paired with AMPLIFOAM midsole and OrthoLite sockliner for marathons.",
        "rating": 4.7,
        "tags": "shoes, shoe, running shoes, running, asics, gel, marathon, professional",
        "image_url": "https://images.unsplash.com/photo-1579338559194-a162d19bf842?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Cushioning": "Rearfoot GEL Tech + AMPLIFOAM",
            "Sockliner": "OrthoLite Moisture-Wicking",
            "Support Type": "Neutral Pronation"
        })
    },
    {
        "name": "Skechers Go Run Elevate Slip-On Performance Shoes",
        "category": "Shoes",
        "brand": "Skechers",
        "price": 3899.0,
        "stock_quantity": 7,
        "description": "Hands-free slip-on running shoes with ULTRA GO lightweight responsive cushioning and Air-Cooled Goga Mat breathable insole.",
        "rating": 4.6,
        "tags": "shoes, shoe, running shoes, running, skechers, slip on, walking, comfort",
        "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Midsole": "ULTRA GO Responsive Tech",
            "Insole": "Air-Cooled Goga Mat",
            "Construction": "Stretch Fit Slip-On Knit"
        })
    },

    # ==========================================
    # 3. REFRIGERATORS (8 items)
    # ==========================================
    {
        "name": "Samsung 253L 3-Star Inverter Double Door Refrigerator",
        "category": "Refrigerators",
        "brand": "Samsung",
        "price": 24990.0,
        "stock_quantity": 7,
        "description": "Frost-free double door refrigerator engineered for modern families of 3-4 members. Features Digital Inverter Compressor with 20-year warranty, all-around cooling, toughened glass shelves, and stabilizer-free operation under ₹40,000.",
        "rating": 4.5,
        "tags": "refrigerators, refrigerator, fridge, double door, samsung, 253l, inverter, frost free, family, under 40000",
        "image_url": "https://images.unsplash.com/photo-1584992236310-6edddc08acff?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Capacity": "253 Litres (Ideal for 3-4 members)",
            "Door Type": "Double Door (Frost Free)",
            "Energy Rating": "3 Star Energy Efficiency",
            "Compressor": "Digital Inverter Compressor (50% less power)",
            "Cooling System": "All-Around Multi-Air Flow Cooling",
            "Shelves": "Spill-Proof Toughened Glass",
            "Warranty": "1 Year on Product, 20 Years on Compressor"
        })
    },
    {
        "name": "LG 242L 3-Star Smart Inverter Double Door Refrigerator",
        "category": "Refrigerators",
        "brand": "LG",
        "price": 25990.0,
        "stock_quantity": 8,
        "description": "Double door frost-free refrigerator with Smart Inverter Compressor, Multi Air Flow vents, anti-bacterial gasket, and fast ice making for family kitchens under ₹40,000.",
        "rating": 4.6,
        "tags": "refrigerators, refrigerator, fridge, double door, lg, 242l, smart inverter, family, frost free, under 40000",
        "image_url": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Capacity": "242 Litres",
            "Type": "Double Door Frost-Free",
            "Energy Rating": "3 Star Rating",
            "Technology": "Smart Inverter & Multi Air Flow",
            "Special Feature": "Moist 'N' Fresh Vegetable Box"
        })
    },
    {
        "name": "Whirlpool 265L 3-Star IntelliFresh Inverter Double Door Refrigerator",
        "category": "Refrigerators",
        "brand": "Whirlpool",
        "price": 27490.0,
        "stock_quantity": 6,
        "description": "IntelliSense inverter technology adapts cooling based on internal load and ambient room temperature. Keeps garden freshness for up to 15 days under ₹40,000.",
        "rating": 4.4,
        "tags": "refrigerators, refrigerator, fridge, double door, whirlpool, 265l, intellifresh, family, under 40000",
        "image_url": "https://images.unsplash.com/photo-1584992236310-6edddc08acff?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Capacity": "265 Litres (Fresh Food 190L, Freezer 75L)",
            "Energy Efficiency": "3 Star Rating",
            "Technology": "Microblock & Zeolite Anti-Odor",
            "Compressor": "IntelliSense Inverter"
        })
    },
    {
        "name": "Haier 256L 3-Star Double Door Refrigerator with Twin Inverter",
        "category": "Refrigerators",
        "brand": "Haier",
        "price": 23990.0,
        "stock_quantity": 9,
        "description": "Twin Inverter technology connects fan and compressor simultaneously for low noise and minimal vibration. Features 8-in-1 convertible cooling modes under ₹40,000.",
        "rating": 4.4,
        "tags": "refrigerators, refrigerator, fridge, double door, haier, 256l, twin inverter, convertible, under 40000",
        "image_url": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Capacity": "256 Litres",
            "Convertible": "8-in-1 Convertible Modes",
            "Cooling": "Turbo Icing in 60 Minutes",
            "Energy Star": "3 Star"
        })
    },
    {
        "name": "Godrej 244L 3-Star Nano Shield Double Door Refrigerator",
        "category": "Refrigerators",
        "brand": "Godrej",
        "price": 22490.0,
        "stock_quantity": 10,
        "description": "Environment-friendly green refrigerant with Nano Shield Disinfection technology that sterilizes 95%+ surface bacteria. Ample vegetable tray for families under ₹40,000.",
        "rating": 4.3,
        "tags": "refrigerators, refrigerator, fridge, double door, godrej, nano shield, family, under 40000",
        "image_url": "https://images.unsplash.com/photo-1584992236310-6edddc08acff?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Capacity": "244 Litres",
            "Hygiene": "Nano Shield 95% Germ Disinfection",
            "Freezer Capacity": "50 Litres",
            "Star Rating": "3 Star"
        })
    },
    {
        "name": "LG 322L 3-Star Frost-Free Double Door Refrigerator for Family",
        "category": "Refrigerators",
        "brand": "LG",
        "price": 34990.0,
        "stock_quantity": 5,
        "description": "Spacious double door model built for families of 4-6 members with Door Cooling+ system that cools 35% faster. Features auto-smart connect for home inverter under ₹40,000.",
        "rating": 4.7,
        "tags": "refrigerators, refrigerator, fridge, double door, lg, 322l, large family, door cooling, under 40000",
        "image_url": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Capacity": "322 Litres (Big Family Size)",
            "Cooling": "Door Cooling+ & Multi Air Flow",
            "Diagnostics": "Smart Diagnosis via Smartphone App",
            "Energy Rating": "3 Star"
        })
    },
    {
        "name": "Samsung 345L 3-Star Convertible 5-in-1 Double Door Refrigerator",
        "category": "Refrigerators",
        "brand": "Samsung",
        "price": 38990.0,
        "stock_quantity": 4,
        "description": "Convertible 5-in-1 modes allow turning freezer into extra fridge space for celebrations. Features Twin Cooling Plus with 70% humidity preservation under ₹40,000.",
        "rating": 4.7,
        "tags": "refrigerators, refrigerator, fridge, double door, samsung, 345l, convertible, twin cooling, family, under 40000",
        "image_url": "https://images.unsplash.com/photo-1584992236310-6edddc08acff?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Capacity": "345 Litres",
            "Modes": "5 Convertible Cooling Modes",
            "Humidity Control": "Twin Cooling Plus Technology",
            "Interior": "Bright Power LED Tower"
        })
    },
    {
        "name": "Samsung 653L Side-by-Side Frost Free AI Inverter Refrigerator",
        "category": "Refrigerators",
        "brand": "Samsung",
        "price": 74990.0,
        "stock_quantity": 3,
        "description": "Flagship side-by-side luxury refrigerator with SpaceMax technology, Wi-Fi SmartThings AI Energy mode, and sleek non-plumbing water and ice dispenser.",
        "rating": 4.8,
        "tags": "refrigerators, refrigerator, fridge, side by side, luxury, 653l, smartthings, premium",
        "image_url": "https://images.unsplash.com/photo-1584992236310-6edddc08acff?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Capacity": "653 Litres Mega Capacity",
            "Design": "Side by Side French Clean Look",
            "Smart Features": "Wi-Fi AI Energy & SmartThings Control",
            "Cooling": "Twin Cooling Plus with Metal Cooling Duct"
        })
    },

    # ==========================================
    # 4. TELEVISIONS (7 items)
    # ==========================================
    {
        "name": "Samsung 43-inch Crystal 4K Vivid Pro Smart LED TV",
        "category": "Televisions",
        "brand": "Samsung",
        "price": 28990.0,
        "stock_quantity": 8,
        "description": "Ultra HD 4K visual clarity with Crystal Processor 4K, PurColor lifelike hues, HDR10+, OTS Lite object-tracking sound, and built-in voice assistants under ₹30,000.",
        "rating": 4.6,
        "tags": "televisions, television, tv, smart tv, 4k, samsung, 43 inch, hdr, crystal 4k",
        "image_url": "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Display": "43-inch 4K Ultra HD (3840 x 2160)",
            "Processor": "Crystal Processor 4K",
            "Audio": "20W 2-Channel OTS Lite Sound",
            "Operating System": "Tizen OS with Netflix, Prime, Disney+",
            "Connectivity": "3 HDMI, 1 USB, Wi-Fi, Bluetooth"
        })
    },
    {
        "name": "LG 43-inch 4K UHD Smart WebOS LED TV (43UR7500)",
        "category": "Televisions",
        "brand": "LG",
        "price": 31990.0,
        "stock_quantity": 7,
        "description": "Brilliant 4K cinema display with α5 AI Processor Gen6, 4K Upscaling, AI Brightness Control, Filmmaker Mode, and intuitive Magic Remote control.",
        "rating": 4.6,
        "tags": "televisions, television, tv, smart tv, 4k, lg, webos, 43 inch, magic remote",
        "image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Screen": "43-inch 4K UHD LED 60Hz",
            "AI Engine": "α5 AI Processor 4K Gen6",
            "Sound": "20W AI Sound Pro (Virtual 5.1.2 Up-mix)",
            "OS": "webOS 23 with User Profiles"
        })
    },
    {
        "name": "Sony Bravia 55-inch 4K Ultra HD Smart LED Google TV",
        "category": "Televisions",
        "brand": "Sony",
        "price": 57990.0,
        "stock_quantity": 6,
        "description": "Powered by Sony X1 4K Processor with 4K X-Reality PRO, Live Color technology, Motionflow XR 100, Dolby Audio, and seamless Google TV interface.",
        "rating": 4.8,
        "tags": "televisions, television, tv, sony, bravia, 55 inch, 4k, google tv, dolby audio",
        "image_url": "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Screen Size": "55-inch 4K Ultra HD",
            "Picture Processor": "Sony 4K Processor X1",
            "Speaker": "20W Bass Reflex Speakers with Dolby Audio",
            "Smart Platform": "Google TV with Hands-Free Google Assistant"
        })
    },
    {
        "name": "Xiaomi 43-inch 4K Dolby Vision Smart Google TV X Series",
        "category": "Televisions",
        "brand": "Xiaomi",
        "price": 23999.0,
        "stock_quantity": 10,
        "description": "Bezel-less metallic design with 4K Dolby Vision HDR10, 30W stereo speakers with Dolby Audio & DTS-X, PatchWall integration, and Google TV under ₹25,000.",
        "rating": 4.4,
        "tags": "televisions, television, tv, smart tv, xiaomi, 43 inch, 4k, dolby vision, budget 4k",
        "image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Resolution": "4K Ultra HD (3840 x 2160)",
            "HDR Format": "Dolby Vision, HDR10, HLG",
            "Sound": "30W Dolby Audio + DTS-HD",
            "Storage": "2GB RAM + 8GB Storage"
        })
    },
    {
        "name": "OnePlus 32-inch Y Series HD Ready Smart Android LED TV",
        "category": "Televisions",
        "brand": "OnePlus",
        "price": 12999.0,
        "stock_quantity": 14,
        "description": "Compact bedroom/dorm room smart TV with Gamma Engine color tuning, 20W Dolby Audio, Google Assistant, and Android TV 11 under ₹15,000.",
        "rating": 4.3,
        "tags": "televisions, television, tv, smart tv, oneplus, 32 inch, android tv, budget",
        "image_url": "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Display": "32-inch HD Ready (1366 x 768) 60Hz",
            "Engine": "Gamma Engine Picture Enhancer",
            "Audio": "20W Dolby Audio Stereo",
            "OS": "Android TV with Chromecast built-in"
        })
    },
    {
        "name": "TCL 55-inch QLED 4K Ultra HD Google TV (55T6G)",
        "category": "Televisions",
        "brand": "TCL",
        "price": 36990.0,
        "stock_quantity": 5,
        "description": "Quantum Dot color technology with 1 billion colors, Dolby Vision Atmos, 120Hz Game Accelerator DLG, and hands-free voice control under ₹40,000.",
        "rating": 4.6,
        "tags": "televisions, television, tv, tcl, qled, 55 inch, 4k, gaming tv, 120hz, dolby vision",
        "image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Panel": "55-inch QLED 4K Ultra HD",
            "Gaming Tech": "120Hz DLG with AMD FreeSync",
            "Sound": "30W Dolby Atmos Soundbar built-in",
            "HDR": "Dolby Vision & HDR10+"
        })
    },
    {
        "name": "LG 55-inch 4K Cinema Smart OLED TV (OLED55C3)",
        "category": "Televisions",
        "brand": "LG",
        "price": 89990.0,
        "stock_quantity": 3,
        "description": "Self-lit OLED pixels delivering infinite contrast, true blacks, α9 AI Processor 4K Gen6, 0.1ms gaming response, 120Hz refresh, and Dolby Vision IQ.",
        "rating": 4.9,
        "tags": "televisions, television, tv, oled, 55 inch, lg oled, cinema, flagship, 120hz",
        "image_url": "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Panel Type": "Self-Lit OLED 4K (Infinite Contrast)",
            "Refresh Rate": "Native 120Hz, 0.1ms GtG",
            "Gaming": "NVIDIA G-Sync & AMD FreeSync Premium",
            "Audio": "40W 2.2 Channel Dolby Atmos"
        })
    },

    # ==========================================
    # 5. FURNITURE (9 items)
    # ==========================================
    {
        "name": "Green Soul Monster Ergonomic Office Chair with Lumbar Support",
        "category": "Furniture",
        "brand": "Green Soul",
        "price": 7499.0,
        "stock_quantity": 7,
        "description": "Heavy-duty ergonomic office chair designed for programmers and desk workers. Features 2D adjustable lumbar support, breathable Korean mesh backrest, pneumatic height adjustment, and 3-year warranty under ₹8,000.",
        "rating": 4.6,
        "tags": "furniture, chair, office chair, ergonomic, lumbar support, green soul, study chair, desk chair, under 8000",
        "image_url": "https://images.unsplash.com/photo-1580481077195-c3a821a58875?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Ergonomics": "2D Adjustable Lumbar Support & 2D Padded Armrests",
            "Backrest": "High-Density Breathable Mesh",
            "Mechanism": "Tilt Lock Mechanism (90° to 120°)",
            "Hydraulics": "Class 4 Gas Lift (TUV Certified up to 125 kg)",
            "Base": "Heavy-Duty Nylon Wheel Base"
        })
    },
    {
        "name": "Da Urban Miller Medium Back Executive Office Chair",
        "category": "Furniture",
        "brand": "Da Urban",
        "price": 5499.0,
        "stock_quantity": 11,
        "description": "Contoured executive desk chair with high-density molded foam seat cushion, torsion bar tilt, and smooth 360-degree swivel casters under ₹8,000.",
        "rating": 4.4,
        "tags": "furniture, chair, office chair, executive, mesh, da urban, study, under 8000",
        "image_url": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Seat": "Extra Thick Molded Foam Cushion",
            "Tilt": "Any Position Synchro Tilt Lock",
            "Castors": "60mm Smooth PU Wheels",
            "Max Weight": "110 kg"
        })
    },
    {
        "name": "Wakefit Ergonomic High Back Breathable Mesh Office Chair",
        "category": "Furniture",
        "brand": "Wakefit",
        "price": 6899.0,
        "stock_quantity": 9,
        "description": "Ergonomic high-back office chair with adjustable headrest, adaptive lumbar spine cushion, multi-point reclining lock, and scratch-resistant wheels under ₹8,000.",
        "rating": 4.5,
        "tags": "furniture, chair, office chair, wakefit, high back, headrest, ergonomic, under 8000",
        "image_url": "https://images.unsplash.com/photo-1580481077195-c3a821a58875?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Back Style": "Full High Back with Adjustable Headrest",
            "Spine Support": "Dual Wing Dynamic Lumbar Support",
            "Recline": "Up to 135-degree Synchro Tilt",
            "Seat Cushion": "45-Density Resilient PU Foam"
        })
    },
    {
        "name": "Savya Home Apollo Ergonomic Revolving Office Chair",
        "category": "Furniture",
        "brand": "Savya Home",
        "price": 4999.0,
        "stock_quantity": 12,
        "description": "Compact and sturdy office chair with reinforced polymer frame, breathable mesh back, pneumatic lift, and chrome finished metal base under ₹8,000.",
        "rating": 4.3,
        "tags": "furniture, chair, office chair, savya home, revolving chair, budget, under 8000, under 5000",
        "image_url": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Frame": "Heavy Duty Fiber Glass Reinforced Nylon",
            "Base": "Polished Chrome Metal Base",
            "Warranty": "1 Year Replacement Warranty"
        })
    },
    {
        "name": "The Sleep Company SmartGRID Onyx Orthopedic Office Chair",
        "category": "Furniture",
        "brand": "The Sleep Company",
        "price": 12999.0,
        "stock_quantity": 5,
        "description": "Patented Japanese SmartGRID seat technology that molds to tailbone shape, eliminates pelvic pressure, and provides active posture correction.",
        "rating": 4.8,
        "tags": "furniture, chair, office chair, smartgrid, orthopedic, luxury, sleep company, back pain",
        "image_url": "https://images.unsplash.com/photo-1580481077195-c3a821a58875?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Seat Material": "Patented SmartGRID Polymer Elastomer",
            "Recline": "Dynamic Dual Back Movement",
            "Armrests": "3D Multi-directional Armrests"
        })
    },
    {
        "name": "DeckUp Siena Engineered Wood Computer & Study Desk",
        "category": "Furniture",
        "brand": "DeckUp",
        "price": 4999.0,
        "stock_quantity": 8,
        "description": "Spacious 4-foot home office computer desk with 3 storage shelves, cable management grommet, and durable melamine matte finish.",
        "rating": 4.5,
        "tags": "furniture, desk, study desk, table, computer desk, office, work from home",
        "image_url": "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Dimensions": "120 cm (W) x 60 cm (D) x 75 cm (H)",
            "Material": "E1 Grade Engineered Wood with Melamine Laminate",
            "Storage": "3 Open Shelves for Books & CPU"
        })
    },
    {
        "name": "Bluewud Amalet Engineered Wood Coffee Table",
        "category": "Furniture",
        "brand": "Bluewud",
        "price": 3299.0,
        "stock_quantity": 10,
        "description": "Modern Scandinavian style center coffee table with lower utility magazine shelf, walnut finish, and water-resistant surface.",
        "rating": 4.4,
        "tags": "furniture, table, coffee table, living room, modern, wood table",
        "image_url": "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Dimensions": "90 cm x 45 cm x 40 cm",
            "Color": "Walnut & White Dual Tone",
            "Load Capacity": "65 kg"
        })
    },
    {
        "name": "Wakefit Orthopedic Memory Foam King Size Mattress",
        "category": "Furniture",
        "brand": "Wakefit",
        "price": 13490.0,
        "stock_quantity": 6,
        "description": "78x72 inch 6-inch orthopedic memory foam mattress with differential pressure zones for spinal alignment and breathable removable cover.",
        "rating": 4.7,
        "tags": "furniture, mattress, bed, memory foam, orthopedic, wakefit, king size",
        "image_url": "https://images.unsplash.com/photo-1582533561751-ef6f6ab93a2e?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Size": "King Size (78 inch x 72 inch x 6 inch)",
            "Foam Layers": "Next-Gen Memory Foam + High Resiliency Base Foam",
            "Warranty": "10-Year Manufacturer Warranty"
        })
    },
    {
        "name": "Solimo Solace 3-Seater Fabric Comfortable Sofa",
        "category": "Furniture",
        "brand": "Solimo",
        "price": 14999.0,
        "stock_quantity": 4,
        "description": "Ergonomic 3-seater living room couch built with solid Salwood frame, high-tensile zigzag springs, and stain-resistant poly-linen upholstery.",
        "rating": 4.5,
        "tags": "furniture, sofa, couch, 3 seater, living room, comfortable sofa",
        "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Structure": "Solid Kiln-Dried Wood Frame",
            "Seating": "32-Density Foam with Polyester Fiber Filling",
            "Dimensions": "188 cm (W) x 80 cm (D) x 85 cm (H)"
        })
    },

    # ==========================================
    # 6. HOME APPLIANCES (8 items)
    # ==========================================
    {
        "name": "Philips Digital Air Fryer 4.1L Rapid Air Technology",
        "category": "Home Appliances",
        "brand": "Philips",
        "price": 6999.0,
        "stock_quantity": 11,
        "description": "Healthy frying with up to 90% less fat using Rapid Air technology. Features digital touch screen with 7 presets, keep-warm function, and dishwasher safe basket.",
        "rating": 4.6,
        "tags": "home appliances, appliance, appliances, air fryer, philips, cooking, healthy, kitchen",
        "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Capacity": "4.1 Litres (0.8 kg food capacity)",
            "Power": "1400 Watts",
            "Programs": "7 Pre-Set Cooking Menus",
            "Technology": "Rapid Air Circulation (90% less oil)"
        })
    },
    {
        "name": "Preethi Zodiac MG-218 750W Mixer Grinder with 5 Jars",
        "category": "Home Appliances",
        "brand": "Preethi",
        "price": 8499.0,
        "stock_quantity": 9,
        "description": "Heavy-duty kitchen master mixer grinder with Vega W5 motor, Master Chef food processor jar for kneading atta, chopping vegetables, and citrus juicing.",
        "rating": 4.6,
        "tags": "home appliances, mixer grinder, mixer, grinder, preethi, kitchen, food processor",
        "image_url": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Motor": "750 Watt Vega W5 Pure Copper Motor",
            "Jars Included": "5 Stainless Steel & Polycarbonate Jars",
            "Speed Settings": "3 Speeds + Pulse Function",
            "Safety": "Overload Tripping Protection"
        })
    },
    {
        "name": "Bajaj 15L Storage Water Heater Geyser with Glassline Tank",
        "category": "Home Appliances",
        "brand": "Bajaj",
        "price": 6499.0,
        "stock_quantity": 8,
        "description": "Titanium armor and glassline inner tank geyser with 8 bar pressure rating suitable for high-rise buildings. Features swirl flow tech for 20% more hot water.",
        "rating": 4.4,
        "tags": "home appliances, geyser, water heater, bajaj, 15l, bathroom, storage geyser",
        "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Capacity": "15 Litres",
            "Tank": "Titanium Enamel Glassline Coated Tank",
            "Pressure Resistance": "8 Bar High-Rise Rating",
            "Star Rating": "4-Star Energy Efficient"
        })
    },
    {
        "name": "Havells Stealth Air 1200mm Silent BLDC Ceiling Fan",
        "category": "Home Appliances",
        "brand": "Havells",
        "price": 5199.0,
        "stock_quantity": 14,
        "description": "Aerodynamic quiet BLDC motor ceiling fan consuming only 26W (60% power saving). Includes RF remote with timer mode and sleep function.",
        "rating": 4.5,
        "tags": "home appliances, fan, ceiling fan, bldc, havells, energy efficient, remote control",
        "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Sweep Size": "1200 mm (48 inch)",
            "Motor Type": "BLDC Inverter Motor (26 Watt power consumption)",
            "Air Delivery": "240 m³/min",
            "Remote": "Smart RF Remote with Timer"
        })
    },
    {
        "name": "Kent Grand Plus RO+UV+UF Alkaline Water Purifier",
        "category": "Home Appliances",
        "brand": "Kent",
        "price": 14990.0,
        "stock_quantity": 6,
        "description": "Multi-stage RO purification with Mineral RO Technology and in-tank UV disinfection. Retains essential minerals while boosting water pH to alkaline levels.",
        "rating": 4.6,
        "tags": "home appliances, water purifier, ro, purifier, kent, drinking water, kitchen",
        "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Purification": "RO + UV + UF + Alkaline + TDS Controller",
            "Storage Tank": "9 Litres Food Grade Tank",
            "Purification Capacity": "20 Litres per hour",
            "Digital Display": "Filter Life & Purity Indicator"
        })
    },
    {
        "name": "Morphy Richards 30L Convection Microwave Oven",
        "category": "Home Appliances",
        "brand": "Morphy Richards",
        "price": 13490.0,
        "stock_quantity": 5,
        "description": "All-in-one baking, grilling, and reheating convection microwave with 200 auto-cook recipes, motorized rotisserie, and stainless steel cavity.",
        "rating": 4.5,
        "tags": "home appliances, microwave, oven, convection, baking, morphy richards, kitchen",
        "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Capacity": "30 Litres Large Cavity",
            "Functions": "Baking, Grilling, Roasting, Defrosting",
            "Cavity": "Mirror Finish Stainless Steel",
            "Power": "900W Microwave, 1200W Grill"
        })
    },
    {
        "name": "Eureka Forbes Smart Robotic Vacuum Cleaner with Mopping",
        "category": "Home Appliances",
        "brand": "Eureka Forbes",
        "price": 19990.0,
        "stock_quantity": 4,
        "description": "Smart LiDAR laser navigation robot that vacuums and mops floors simultaneously. App controlled scheduling with automatic recharge dock.",
        "rating": 4.5,
        "tags": "home appliances, vacuum cleaner, robotic vacuum, cleaner, eureka forbes, smart home",
        "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Suction Power": "3000 Pa Deep Suction",
            "Navigation": "360-degree LiDAR Laser Mapping",
            "Battery": "5200 mAh (150 min runtime)",
            "Tank": "2-in-1 Dustbin & Water Tank"
        })
    },
    {
        "name": "Dyson V8 Absolute Cordless Stick Vacuum Cleaner",
        "category": "Home Appliances",
        "brand": "Dyson",
        "price": 29900.0,
        "stock_quantity": 4,
        "description": "Powerful de-tangling cordless vacuum powered by Dyson digital motor V8. Captures allergens and expels cleaner air with whole-machine filtration.",
        "rating": 4.8,
        "tags": "home appliances, vacuum cleaner, dyson, cordless, deep cleaning, allergen",
        "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Suction": "115 Air Watts in Max Mode",
            "Runtime": "Up to 40 Minutes Fade-Free Power",
            "Filtration": "Advanced Whole-Machine HEPA Filtration",
            "Weight": "2.61 kg Ultra-Balanced"
        })
    },

    # ==========================================
    # 7. GAMING HEADPHONES & SMARTPHONES ADDITIONS
    # ==========================================
    {
        "name": "Razer BlackShark V2 X Gaming Headset",
        "category": "Headphones",
        "brand": "Razer",
        "price": 3499.0,
        "stock_quantity": 12,
        "description": "Esports gaming headset with TriForce 50mm dynamic drivers, HyperClear cardioid bendable microphone, advanced passive noise cancellation, and lightweight 240g design.",
        "rating": 4.7,
        "tags": "headphones, gaming, gaming headphones, headset, razer, 7.1 surround sound, microphone, esports",
        "image_url": "https://images.unsplash.com/photo-1599669454699-248893623440?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Drivers": "Razer TriForce 50mm Titanium Drivers",
            "Audio": "7.1 Surround Sound on PC",
            "Microphone": "Razer HyperClear Cardioid Mic",
            "Weight": "240 grams (Ultra-light)",
            "Compatibility": "PC, Mac, PS5, Xbox Series X/S, Nintendo Switch, Mobile"
        })
    },
    {
        "name": "HyperX Cloud Core DTS Headphone:X Gaming Headset",
        "category": "Headphones",
        "brand": "HyperX",
        "price": 4490.0,
        "stock_quantity": 9,
        "description": "Durable aluminum frame gaming headset with DTS Headphone:X Spatial Audio, signature HyperX memory foam ear cushions, and detachable noise-cancelling mic.",
        "rating": 4.7,
        "tags": "headphones, gaming, gaming headphones, hyperx, dts spatial audio, aluminum, mic",
        "image_url": "https://images.unsplash.com/photo-1599669454699-248893623440?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Audio Spatial": "DTS Headphone:X Spatial Audio",
            "Frame": "Durable Aluminum Construction",
            "Ear Cushions": "Signature HyperX Memory Foam",
            "Driver": "53 mm Dynamic Neodymium"
        })
    },
    {
        "name": "Cosmic Byte GS410 Gaming Headset with Mic",
        "category": "Headphones",
        "brand": "Cosmic Byte",
        "price": 1099.0,
        "stock_quantity": 18,
        "description": "Budget gaming headset with soft cushion head-pad, flexible noise-reduction microphone, and punchy bass for Battle Royale and competitive FPS games.",
        "rating": 4.2,
        "tags": "headphones, gaming, gaming headphones, cosmic byte, budget gaming, mic, under 2000",
        "image_url": "https://images.unsplash.com/photo-1599669454699-248893623440?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Drivers": "40 mm Speaker Drivers",
            "Cable": "2.1m Braided Cable with 3.5mm Jack",
            "Controls": "Inline Volume Controller & Mic Mute Switch"
        })
    },
    {
        "name": "Vivo V30 5G with 50MP Eye-AF Zeiss Portrait Camera",
        "category": "Smartphones",
        "brand": "Vivo",
        "price": 29999.0,
        "stock_quantity": 8,
        "description": "Ultra-slim 3D curved 1.5K AMOLED smartphone equipped with 50MP VCS True Color main camera with OIS and Studio-quality Smart Aura Light for night portraits under ₹30,000.",
        "rating": 4.6,
        "tags": "smartphones, smartphone, phone, camera, good camera, portrait, ois, vivo, 5g, under 30000",
        "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Rear Camera": "50 MP VCS True Color OIS + 50MP Ultra-Wide Angle",
            "Front Camera": "50 MP Eye-AF Group Selfie Camera",
            "Display": "6.78-inch 120Hz 1.5K 3D Curved AMOLED (2800 nits peak)",
            "Processor": "Qualcomm Snapdragon 7 Gen 3 (4nm)",
            "Battery": "5000 mAh with 80W FlashCharge"
        })
    },
    {
        "name": "Samsung Galaxy S23 FE 5G (Flagship Camera)",
        "category": "Smartphones",
        "brand": "Samsung",
        "price": 39999.0,
        "stock_quantity": 6,
        "description": "Pro-grade triple camera system with 50MP high-res sensor, 3x optical zoom, Nightography sensor, IP68 water resistance, and Dynamic AMOLED 2X 120Hz display.",
        "rating": 4.6,
        "tags": "smartphones, smartphone, phone, camera, samsung, flagship, nightography, s23, 5g",
        "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600&auto=format&fit=crop&q=80",
        "specs": json.dumps({
            "Camera": "50 MP Wide OIS + 12MP Ultra-Wide + 8MP 3x Optical Telephoto",
            "Display": "6.4-inch Dynamic AMOLED 2X 120Hz",
            "Durability": "Corning Gorilla Glass 5 & IP68 Water/Dust Proof"
        })
    }
]

def migrate_and_expand():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Update existing 'Keyboards', 'Monitors', and 'Accessories' to 'Computer Accessories'
    cursor.execute("""
        UPDATE products
        SET category = 'Computer Accessories'
        WHERE category IN ('Keyboards', 'Monitors', 'Accessories')
    """)
    updated_cat_count = cursor.rowcount
    print(f"Updated {updated_cat_count} products to 'Computer Accessories' category.")

    # 2. Insert new products if they don't already exist by name
    inserted = 0
    for item in NEW_PRODUCTS:
        cursor.execute("SELECT id FROM products WHERE name = ?", (item["name"],))
        existing = cursor.fetchone()
        if not existing:
            cursor.execute("""
                INSERT INTO products (name, category, brand, price, stock_quantity, description, rating, tags, image_url, specs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["name"],
                item["category"],
                item["brand"],
                item["price"],
                item["stock_quantity"],
                item["description"],
                item["rating"],
                item["tags"],
                item["image_url"],
                item.get("specs", "{}")
            ))
            inserted += 1

    conn.commit()
    print(f"Successfully inserted {inserted} new products.")

    # 3. Print breakdown by category
    cursor.execute("SELECT category, COUNT(*) FROM products GROUP BY category ORDER BY category")
    rows = cursor.fetchall()
    print("\n--- NEW CATALOG BREAKDOWN ---")
    total_count = 0
    for cat, count in rows:
        print(f"  {cat}: {count} products")
        total_count += count
    print(f"Total Products: {total_count}")

    conn.close()

if __name__ == "__main__":
    migrate_and_expand()
