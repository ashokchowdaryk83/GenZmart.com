import os
import random
import time
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

inventory = {
    "1": {"name": "Multicolor Zardosi Kanchipuram Silk Saree", "cat": "Sarees", "stock": 15, "price": 149900.0, "bulk_qty": 3, "bulk_disc": 10.0},
    "2": {"name": "Off White Zari Kanchipuram Silk Saree", "cat": "Sarees", "stock": 20, "price": 57000.0, "bulk_qty": 3, "bulk_disc": 10.0},
    "3": {"name": "Pure Handwoven Mulberry Saree", "cat": "Sarees", "stock": 45, "price": 12879.0, "bulk_qty": 5, "bulk_disc": 12.0},
    "4": {"name": "Handloom Chocolate Pink Kanjivaram", "cat": "Sarees", "stock": 30, "price": 13570.0, "bulk_qty": 5, "bulk_disc": 12.0},
    "5": {"name": "Emerald Katan Banarasi Silk Saree", "cat": "Sarees", "stock": 12, "price": 85000.0, "bulk_qty": 3, "bulk_disc": 12.0},
    "6": {"name": "Hand-Painted Pure Floral Organza Saree", "cat": "Sarees", "stock": 25, "price": 42000.0, "bulk_qty": 5, "bulk_disc": 15.0},
    "7": {"name": "Festive 22kt Gold Bead Necklace", "cat": "Jewelry", "stock": 8, "price": 78333.0, "bulk_qty": 2, "bulk_disc": 5.0},
    "8": {"name": "Keya Nakshi 22kt Gold Masterpiece", "cat": "Jewelry", "stock": 3, "price": 794275.0, "bulk_qty": 2, "bulk_disc": 5.0},
    "9": {"name": "Leafy Sanai Engraved Gold Necklace", "cat": "Jewelry", "stock": 10, "price": 95811.0, "bulk_qty": 2, "bulk_disc": 5.0},
    "10": {"name": "Saanvi Royal 22kt Statement Collar", "cat": "Jewelry", "stock": 2, "price": 1002766.0, "bulk_qty": 2, "bulk_disc": 5.0},
    "11": {"name": "Uncut Polki Diamond Choker Set", "cat": "Jewelry", "stock": 4, "price": 650000.0, "bulk_qty": 2, "bulk_disc": 8.0},
    "12": {"name": "Antique Temple Gold Kada Pair", "cat": "Jewelry", "stock": 6, "price": 320000.0, "bulk_qty": 3, "bulk_disc": 5.0},
    "13": {"name": "Tom Ford Tobacco Oud EDP", "cat": "Scents", "stock": 40, "price": 76707.0, "bulk_qty": 5, "bulk_disc": 10.0},
    "14": {"name": "Neesh Luxe Aoud Extrait Premium", "cat": "Scents", "stock": 150, "price": 1750.0, "bulk_qty": 10, "bulk_disc": 20.0},
    "15": {"name": "Gissah Imperial Valley 200ml", "cat": "Scents", "stock": 85, "price": 10500.0, "bulk_qty": 5, "bulk_disc": 10.0},
    "16": {"name": "Robert Piguet Oud EDP Classic", "cat": "Scents", "stock": 60, "price": 11999.0, "bulk_qty": 5, "bulk_disc": 10.0},
    "17": {"name": "Royal Ambergris Infused Attar Oil", "cat": "Scents", "stock": 15, "price": 24500.0, "bulk_qty": 10, "bulk_disc": 18.0},
    "18": {"name": "Tuscan Leather & Saffron Intense", "cat": "Scents", "stock": 22, "price": 19000.0, "bulk_qty": 5, "bulk_disc": 10.0},
    "19": {"name": "Satjeevan Cold Pressed Oil 5-Pack", "cat": "Soaps", "stock": 200, "price": 900.0, "bulk_qty": 20, "bulk_disc": 15.0},
    "20": {"name": "Aaranyam French Pink Clay 4-Pack", "cat": "Soaps", "stock": 180, "price": 599.0, "bulk_qty": 20, "bulk_disc": 15.0},
    "21": {"name": "Thenpanai Vetiver Marikozhundhu Trio", "cat": "Soaps", "stock": 300, "price": 435.0, "bulk_qty": 30, "bulk_disc": 20.0},
    "22": {"name": "Coral and Sky Virgin Butter Suite", "cat": "Soaps", "stock": 140, "price": 1439.0, "bulk_qty": 15, "bulk_disc": 10.0},
    "23": {"name": "Himalayan Shilajit Treatment Bar", "cat": "Soaps", "stock": 90, "price": 1850.0, "bulk_qty": 50, "bulk_disc": 25.0},
    "24": {"name": "Bulgarian Rose & Goat Milk Pack", "cat": "Soaps", "stock": 110, "price": 2200.0, "bulk_qty": 20, "bulk_disc": 20.0},
    "25": {"name": "Maroon Flush Handwoven Kani Pashmina", "cat": "Niche Luxury", "stock": 5, "price": 526335.0, "bulk_qty": 2, "bulk_disc": 20.0},
    "26": {"name": "Grey Black Reversible Jamawar Shawl", "cat": "Niche Luxury", "stock": 7, "price": 498995.0, "bulk_qty": 2, "bulk_disc": 10.0},
    "27": {"name": "Handloom Sozni Embroidered Shawl", "cat": "Niche Luxury", "stock": 8, "price": 355000.0, "bulk_qty": 2, "bulk_disc": 10.0},
    "28": {"name": "Kashmir Loom Oversize Brown Kani", "cat": "Niche Luxury", "stock": 4, "price": 370000.0, "bulk_qty": 2, "bulk_disc": 10.0},
    "29": {"name": "Ivory Certified Pure Solid Pashmina", "cat": "Niche Luxury", "stock": 14, "price": 85000.0, "bulk_qty": 5, "bulk_disc": 15.0},
    "30": {"name": "Hand-Spun Pure Natural Toosh Scarf", "cat": "Niche Luxury", "stock": 3, "price": 110000.0, "bulk_qty": 3, "bulk_disc": 12.0}
}

finance = {"cash_balance": 25000000.0, "receivables": 0.0}

@app.route('/api/market')
def get_market_tickers():
    return jsonify({
        "Copper Index": f"Rupees {int(1214300 * random.uniform(0.99, 1.01)):,}/Ton",
        "Steel Index": f"Rupees {int(60480 * random.uniform(0.98, 1.02)):,}/Ton",
        "Basmati Rice": f"Rupees {int(94080 * random.uniform(0.995, 1.005)):,}/Ton",
        "Raw Cotton": f"Rupees {int(154560 * random.uniform(0.97, 1.03)):,}/Ton"
    })

@app.route('/api/products')
def get_products():
    return jsonify(inventory)

@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json or {}
    prod_id = data.get("id")
    qty = int(data.get("qty", 1))
    item = inventory.get(prod_id)
    if not item: 
        return jsonify({"error": "Item mismatch"}), 400
    
    base_price = item["price"]
    discount = item["bulk_disc"] if qty >= item["bulk_qty"] else 0.0
    unit_price = base_price * (1 - discount / 100.0)
    total_cost = unit_price * qty
    
    pp_status = "Stock Verified (MM)"
    if item["stock"] < qty:
        produced_units = (qty - item["stock"]) + 10
        item["stock"] += produced_units
        pp_status = f"PP Alert: Auto-Manufactured {produced_units} units to prevent pipeline breakdown."
        
    item["stock"] -= qty
    finance["cash_balance"] += total_cost
    inv_number = f"INV-{int(time.time())}"
    
    return jsonify({
        "status": "PAID & POSTED",
        "invoice_no": inv_number,
        "amount_processed": f"Rupees {total_cost:,.2f}",
        "pp_info": pp_status,
        "fico_log": f"Debit: Online Cash A/c (+Rupees {total_cost:,.2f}) | Credit: Finished Goods Asset A/c"
    })

@app.route('/')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
