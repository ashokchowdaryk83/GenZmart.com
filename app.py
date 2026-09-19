pythonimport os
import random
import time
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# 1. DATABASE STATE: 30 Premium Distributed Luxury Products with Embedded Image CDN Assets
inventory = {
    "1": {"name": "Multicolor Zardosi Kanchipuram Silk", "cat": "Sarees", "stock": 15, "price": 149900.0, "bulk_qty": 3, "bulk_disc": 10.0, "img": "https://unsplash.com"},
    "2": {"name": "Off White Zari Kanchipuram Silk", "cat": "Sarees", "stock": 20, "price": 57000.0, "bulk_qty": 3, "bulk_disc": 10.0, "img": "https://unsplash.com"},
    "3": {"name": "Pure Handwoven Mulberry Saree", "cat": "Sarees", "stock": 45, "price": 12879.0, "bulk_qty": 5, "bulk_disc": 12.0, "img": "https://unsplash.com"},
    "4": {"name": "Handloom Chocolate Pink Kanjivaram", "cat": "Sarees", "stock": 30, "price": 13570.0, "bulk_qty": 5, "bulk_disc": 12.0, "img": "https://unsplash.com"},
    "5": {"name": "Emerald Katan Banarasi Silk Saree", "cat": "Sarees", "stock": 12, "price": 85000.0, "bulk_qty": 3, "bulk_disc": 12.0, "img": "https://unsplash.com"},
    "6": {"name": "Hand-Painted Pure Floral Organza", "cat": "Sarees", "stock": 25, "price": 42000.0, "bulk_qty": 5, "bulk_disc": 15.0, "img": "https://unsplash.com"},
    
    "7": {"name": "Festive 22kt Gold Bead Necklace", "cat": "Jewelry", "stock": 8, "price": 78333.0, "bulk_qty": 2, "bulk_disc": 5.0, "img": "https://unsplash.com"},
    "8": {"name": "Keya Nakshi 22kt Gold Masterpiece", "cat": "Jewelry", "stock": 3, "price": 794275.0, "bulk_qty": 2, "bulk_disc": 5.0, "img": "https://unsplash.com"},
    "9": {"name": "Leafy Sanai Engraved Gold Choker", "cat": "Jewelry", "stock": 10, "price": 95811.0, "bulk_qty": 2, "bulk_disc": 5.0, "img": "https://unsplash.com"},
    "10": {"name": "Saanvi Royal 22kt Collar Matrix", "cat": "Jewelry", "stock": 2, "price": 1002766.0, "bulk_qty": 2, "bulk_disc": 5.0, "img": "https://unsplash.com"},
    "11": {"name": "Uncut Polki Diamond Luxury Choker", "cat": "Jewelry", "stock": 4, "price": 650000.0, "bulk_qty": 2, "bulk_disc": 8.0, "img": "https://unsplash.com"},
    "12": {"name": "Antique Temple Gold Kada Pair", "cat": "Jewelry", "stock": 6, "price": 320000.0, "bulk_qty": 3, "bulk_disc": 5.0, "img": "https://unsplash.com"},
    
    "13": {"name": "Tom Ford Tobacco Oud EDP", "cat": "Scents", "stock": 40, "price": 76707.0, "bulk_qty": 5, "bulk_disc": 10.0, "img": "https://unsplash.com"},
    "14": {"name": "Neesh Luxe Aoud Extrait Premium", "cat": "Scents", "stock": 150, "price": 1750.0, "bulk_qty": 10, "bulk_disc": 20.0, "img": "https://unsplash.com"},
    "15": {"name": "Gissah Imperial Valley 200ml", "cat": "Scents", "stock": 85, "price": 10500.0, "bulk_qty": 5, "bulk_disc": 10.0, "img": "https://unsplash.com"},
    "16": {"name": "Robert Piguet Oud EDP Classic", "cat": "Scents", "stock": 60, "price": 11999.0, "bulk_qty": 5, "bulk_disc": 10.0, "img": "https://unsplash.com"},
    "17": {"name": "Royal Ambergris Attar Oil Core", "cat": "Scents", "stock": 15, "price": 24500.0, "bulk_qty": 10, "bulk_disc": 18.0, "img": "https://unsplash.com"},
    "18": {"name": "Tuscan Leather & Saffron Intense", "cat": "Scents", "stock": 22, "price": 19000.0, "bulk_qty": 5, "bulk_disc": 10.0, "img": "https://unsplash.com"},
    
    "19": {"name": "Satjeevan Cold Pressed Oil 5-Pack", "cat": "Soaps", "stock": 200, "price": 900.0, "bulk_qty": 20, "bulk_disc": 15.0, "img": "https://unsplash.com"},
    "20": {"name": "Aaranyam French Pink Clay 4-Pack", "cat": "Soaps", "stock": 180, "price": 599.0, "bulk_qty": 20, "bulk_disc": 15.0, "img": "https://unsplash.com"},
    "21": {"name": "Thenpanai Vetiver Marikozhundhu Trio", "cat": "Soaps", "stock": 300, "price": 435.0, "bulk_qty": 30, "bulk_disc": 20.0, "img": "https://unsplash.com"},
    "22": {"name": "Coral and Sky Virgin Butter Suite", "cat": "Soaps", "stock": 140, "price": 1439.0, "bulk_qty": 15, "bulk_disc": 10.0, "img": "https://unsplash.com"},
    "23": {"name": "Himalayan Shilajit Treatment Bar", "cat": "Soaps", "stock": 90, "price": 1850.0, "bulk_qty": 50, "bulk_disc": 25.0, "img": "https://unsplash.com"},
    "24": {"name": "Bulgarian Rose & Goat Milk Pack", "cat": "Soaps", "stock": 110, "price": 2200.0, "bulk_qty": 20, "bulk_disc": 20.0, "img": "https://unsplash.com"},
    
    "25": {"name": "Maroon Flush Handwoven Pashmina", "cat": "Niche Luxury", "stock": 5, "price": 526335.0, "bulk_qty": 2, "bulk_disc": 20.0, "img": "https://unsplash.com"},
    "26": {"name": "Grey Black Reversible Jamawar", "cat": "Niche Luxury", "stock": 7, "price": 498995.0, "bulk_qty": 2, "bulk_disc": 10.0, "img": "https://unsplash.com"},
    "27": {"name": "Handloom Sozni Embroidered Shawl", "cat": "Niche Luxury", "stock": 8, "price": 355000.0, "bulk_qty": 2, "bulk_disc": 10.0, "img": "https://unsplash.com"},
    "28": {"name": "Kashmir Loom Oversize Brown Kani", "cat": "Niche Luxury", "stock": 4, "price": 370000.0, "bulk_qty": 2, "bulk_disc": 10.0, "img": "https://unsplash.com"},
    "29": {"name": "Ivory Certified Pure Pashmina", "cat": "Niche Luxury", "stock": 14, "price": 85000.0, "bulk_qty": 5, "bulk_disc": 15.0, "img": "https://unsplash.com"},
    "30": {"name": "Hand-Spun Pure Natural Toosh Scarf", "cat": "Niche Luxury", "stock": 3, "price": 110000.0, "bulk_qty": 3, "bulk_disc": 12.0, "img": "https://unsplash.com"}
}

finance = {"cash_balance": 25000000.0}

# 2. GLOBAL TELEMETRY ENGINE: Tracking Student Roaming vs. Classroom status via simulated IoT Node Sensors
def sample_iot_telemetry():
    first_names = ["Arjun", "Sai", "Divya", "Rahul", "Kavya", "Ananya"]
    last_names = ["Kumar", "Reddy", "Sharma", "Chowdary", "Patel", "Joshi"]
    depts = ["Computer Science", "Electronics & Comm", "Information Tech", "Mechanical Eng"]
    sensors = ["Gate 01 Main RFID Terminal", "Academic Block Alpha Router", "Central Canteen Node 4", "Library Entrance Scanner", "Sports Arena BLE Anchor"]
    activities = ["Verifying credential match", "Scanning dynamic packet entry", "Node authentication cycle", "Transitioning through checkpoint"]
    
    data = []
    for i in range(1, 7):
        assigned_sensor = random.choice(sensors)
        status = "Roaming Outside" if ("Canteen" in assigned_sensor or "Sports" in assigned_sensor or "Gate" in assigned_sensor) else "In Class"
        data.append({
            "id": f"2026-ROLL-0{i}",
            "name": f"{first_names[i-1]} {last_names[i-1]}",
            "dept": random.choice(depts),
            "sensor": assigned_sensor,
            "activity": random.choice(activities),
            "status": status
        })
    return data

@app.route('/api/market')
def get_market_tickers():
    return jsonify({
        "Gold Spot (22kt/10g)": f"₹{int(72450 * random.uniform(0.995, 1.005)):,}",
        "Silk Raw Material Index": f"₹{int(4250 * random.uniform(0.98, 1.02)):,}/Kg",
        "Premium Basmati Cotton": f"₹{int(94080 * random.uniform(0.99, 1.01)):,}/Ton"
    })

@app.route('/api/products')
def get_products():
    return jsonify(inventory)

@app.route('/api/traceability')
def get_traceability():
    return jsonify(sample_iot_telemetry())

@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json or {}
    prod_id = data.get("id")
    qty = int(data.get("qty", 1))
    client_name = data.get("client_name", "Walk-In Corporate Matrix Node")
    
    item = inventory.get(prod_id)
    if not item: 
        return jsonify({"error": "Product reference array mismatch."}), 400
    
    base_price = item["price"]
    discount = item["bulk_disc"] if qty >= item["bulk_qty"] else 0.0
    unit_price = base_price * (1 - discount / 100.0)
    subtotal = base_price * qty
    discount_val = subtotal * (discount / 100.0)
    total_cost = unit_price * qty
    
    pp_status = "Stock Level Verified Stable (MM Module)"
    if item["stock"] < qty:
        replenish = (qty - item["stock"]) + 15
        item["stock"] += replenish
        pp_status = f"PP Trigger Alert: Automatically manufactured {replenish} units via operational execution."
        
    item["stock"] -= qty
    finance["cash_balance"] += total_cost
    inv_number = f"GZ-INV-{int(time.time())}"
    
    return jsonify({
        "invoice_no": inv_number,
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "client": client_name,
        "product_name": item["name"],
        "qty": qty,
        "base_price": f"₹{base_price:,.2f}",
        "subtotal": f"₹{subtotal:,.2f}",
"discount_applied": f"₹{discount_val:,.2f} ({discount}%)",
        "total": f"₹{total_cost:,.2f}",
        "pp_info": pp_status,
        "ledger_log": f"DR Cash Operating A/c (+₹{total_cost:,.2f}) | CR Revenue Asset Control A/c"})
    @app.route('/')
    def dashboard():
        return render_template('index.html')
        if name == 'main':
            port = int(os.environ.get("PORT", 5000))
            app.run(host='0.0.0.0', port=port)
