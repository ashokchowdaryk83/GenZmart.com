import os
import random
import time
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# GST rates by category (simplified flat slab per category for this demo —
# real GST law has multiple slabs within a category depending on price/HSN
# code; adjust GST_RATES if you need exact statutory slabs).
# ---------------------------------------------------------------------------
GST_RATES = {
    "Sarees": 5.0,
    "Jewelry": 3.0,
    "Scents": 18.0,
    "Soaps": 18.0,
    "Niche Luxury": 12.0,
}

# 1. CATALOG: 30 products. img uses a stable placeholder photo per product —
# replace with your real product photo URLs (or an /static/ path) when ready.
inventory = {
    "1": {"name": "Multicolor Zardosi Kanchipuram Silk", "cat": "Sarees", "stock": 15, "price": 149900.0, "bulk_qty": 3, "bulk_disc": 10.0},
    "2": {"name": "Off White Zari Kanchipuram Silk", "cat": "Sarees", "stock": 20, "price": 57000.0, "bulk_qty": 3, "bulk_disc": 10.0},
    "3": {"name": "Pure Handwoven Mulberry Saree", "cat": "Sarees", "stock": 45, "price": 12879.0, "bulk_qty": 5, "bulk_disc": 12.0},
    "4": {"name": "Handloom Chocolate Pink Kanjivaram", "cat": "Sarees", "stock": 30, "price": 13570.0, "bulk_qty": 5, "bulk_disc": 12.0},
    "5": {"name": "Emerald Katan Banarasi Silk Saree", "cat": "Sarees", "stock": 12, "price": 85000.0, "bulk_qty": 3, "bulk_disc": 12.0},
    "6": {"name": "Hand-Painted Pure Floral Organza", "cat": "Sarees", "stock": 25, "price": 42000.0, "bulk_qty": 5, "bulk_disc": 15.0},

    "7": {"name": "Festive 22kt Gold Bead Necklace", "cat": "Jewelry", "stock": 8, "price": 78333.0, "bulk_qty": 2, "bulk_disc": 5.0},
    "8": {"name": "Keya Nakshi 22kt Gold Masterpiece", "cat": "Jewelry", "stock": 3, "price": 794275.0, "bulk_qty": 2, "bulk_disc": 5.0},
    "9": {"name": "Leafy Sanai Engraved Gold Choker", "cat": "Jewelry", "stock": 10, "price": 95811.0, "bulk_qty": 2, "bulk_disc": 5.0},
    "10": {"name": "Saanvi Royal 22kt Collar Matrix", "cat": "Jewelry", "stock": 2, "price": 1002766.0, "bulk_qty": 2, "bulk_disc": 5.0},
    "11": {"name": "Uncut Polki Diamond Luxury Choker", "cat": "Jewelry", "stock": 4, "price": 650000.0, "bulk_qty": 2, "bulk_disc": 8.0},
    "12": {"name": "Antique Temple Gold Kada Pair", "cat": "Jewelry", "stock": 6, "price": 320000.0, "bulk_qty": 3, "bulk_disc": 5.0},

    "13": {"name": "Tom Ford Tobacco Oud EDP", "cat": "Scents", "stock": 40, "price": 76707.0, "bulk_qty": 5, "bulk_disc": 10.0},
    "14": {"name": "Neesh Luxe Aoud Extrait Premium", "cat": "Scents", "stock": 150, "price": 1750.0, "bulk_qty": 10, "bulk_disc": 20.0},
    "15": {"name": "Gissah Imperial Valley 200ml", "cat": "Scents", "stock": 85, "price": 10500.0, "bulk_qty": 5, "bulk_disc": 10.0},
    "16": {"name": "Robert Piguet Oud EDP Classic", "cat": "Scents", "stock": 60, "price": 11999.0, "bulk_qty": 5, "bulk_disc": 10.0},
    "17": {"name": "Royal Ambergris Attar Oil Core", "cat": "Scents", "stock": 15, "price": 24500.0, "bulk_qty": 10, "bulk_disc": 18.0},
    "18": {"name": "Tuscan Leather & Saffron Intense", "cat": "Scents", "stock": 22, "price": 19000.0, "bulk_qty": 5, "bulk_disc": 10.0},

    "19": {"name": "Satjeevan Cold Pressed Oil 5-Pack", "cat": "Soaps", "stock": 200, "price": 900.0, "bulk_qty": 20, "bulk_disc": 15.0},
    "20": {"name": "Aaranyam French Pink Clay 4-Pack", "cat": "Soaps", "stock": 180, "price": 599.0, "bulk_qty": 20, "bulk_disc": 15.0},
    "21": {"name": "Thenpanai Vetiver Marikozhundhu Trio", "cat": "Soaps", "stock": 300, "price": 435.0, "bulk_qty": 30, "bulk_disc": 20.0},
    "22": {"name": "Coral and Sky Virgin Butter Suite", "cat": "Soaps", "stock": 140, "price": 1439.0, "bulk_qty": 15, "bulk_disc": 10.0},
    "23": {"name": "Himalayan Shilajit Treatment Bar", "cat": "Soaps", "stock": 90, "price": 1850.0, "bulk_qty": 50, "bulk_disc": 25.0},
    "24": {"name": "Bulgarian Rose & Goat Milk Pack", "cat": "Soaps", "stock": 110, "price": 2200.0, "bulk_qty": 20, "bulk_disc": 20.0},

    "25": {"name": "Maroon Flush Handwoven Pashmina", "cat": "Niche Luxury", "stock": 5, "price": 526335.0, "bulk_qty": 2, "bulk_disc": 20.0},
    "26": {"name": "Grey Black Reversible Jamawar", "cat": "Niche Luxury", "stock": 7, "price": 498995.0, "bulk_qty": 2, "bulk_disc": 10.0},
    "27": {"name": "Handloom Sozni Embroidered Shawl", "cat": "Niche Luxury", "stock": 8, "price": 355000.0, "bulk_qty": 2, "bulk_disc": 10.0},
    "28": {"name": "Kashmir Loom Oversize Brown Kani", "cat": "Niche Luxury", "stock": 4, "price": 370000.0, "bulk_qty": 2, "bulk_disc": 10.0},
    "29": {"name": "Ivory Certified Pure Pashmina", "cat": "Niche Luxury", "stock": 14, "price": 85000.0, "bulk_qty": 5, "bulk_disc": 15.0},
    "30": {"name": "Hand-Spun Pure Natural Toosh Scarf", "cat": "Niche Luxury", "stock": 3, "price": 110000.0, "bulk_qty": 3, "bulk_disc": 12.0},
}

# Attach a stable placeholder photo + GST rate to every product at startup
for pid, item in inventory.items():
    item["img"] = f"https://picsum.photos/seed/genzsmart{pid}/500/400"
    item["gst_rate"] = GST_RATES.get(item["cat"], 18.0)

# ---------------------------------------------------------------------------
# FICO: finance state, general ledger (journal entries), customer account book
# ---------------------------------------------------------------------------
finance = {"cash_balance": 25000000.0}
gl_entries = []           # company-wide journal (FICO view)
customer_ledger = {}      # {customer_name: {"balance": float, "entries": [...]}}

# ---------------------------------------------------------------------------
# Live commodity ticker (MM / market data feed) — random-walk simulation
# ---------------------------------------------------------------------------
commodities = {
    "Gold Spot (22kt/10g)": 72450.0,
    "Silver Spot (1kg)": 88200.0,
    "Silk Raw Material Index (per Kg)": 4250.0,
    "Premium Basmati Cotton (per Ton)": 94080.0,
    "Oud Oil (per Tola)": 21500.0,
    "Rose Absolute (per Kg)": 385000.0,
}


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
            "status": status,
        })
    return data


@app.route('/')
def dashboard():
    return render_template('index.html')


@app.route('/api/market')
def get_market_tickers():
    out = []
    for name, base in commodities.items():
        drift = random.uniform(-0.015, 0.015)
        commodities[name] = round(base * (1 + drift), 2)
        change_pct = drift * 100
        out.append({
            "name": name,
            "price": f"₹{commodities[name]:,.2f}",
            "change_pct": round(change_pct, 2),
        })
    return jsonify(out)


@app.route('/api/products')
def get_products():
    return jsonify(inventory)


@app.route('/api/traceability')
def get_traceability():
    return jsonify(sample_iot_telemetry())


@app.route('/api/ledger')
def get_gl():
    """FICO: full company general ledger / journal view."""
    return jsonify(gl_entries)


@app.route('/api/customer/<name>')
def get_customer_ledger(name):
    """FICO/SD: one customer's account book (statement)."""
    record = customer_ledger.get(name)
    if not record:
        return jsonify({"error": "No account history for this customer yet."}), 404
    return jsonify(record)


@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json or {}
    prod_id = data.get("id")
    qty = int(data.get("qty", 1))
    client_name = data.get("client_name", "Walk-In Corporate Matrix Node").strip() or "Walk-In Corporate Matrix Node"
    state = data.get("state", "same")  # "same" = intra-state (CGST+SGST), "other" = inter-state (IGST)

    item = inventory.get(prod_id)
    if not item:
        return jsonify({"error": "Product reference array mismatch."}), 400
    if qty < 1:
        return jsonify({"error": "Quantity must be at least 1."}), 400

    # --- SD: pricing & discount ---
    base_price = item["price"]
    discount_pct = item["bulk_disc"] if qty >= item["bulk_qty"] else 0.0
    unit_price = base_price * (1 - discount_pct / 100.0)
    subtotal = base_price * qty
    discount_val = subtotal * (discount_pct / 100.0)
    taxable_value = unit_price * qty

    # --- FICO: GST computation ---
    gst_rate = item["gst_rate"]
    gst_amount = taxable_value * (gst_rate / 100.0)
    if state == "other":
        igst = round(gst_amount, 2)
        cgst = sgst = 0.0
    else:
        igst = 0.0
        cgst = sgst = round(gst_amount / 2, 2)
    total_cost = round(taxable_value + gst_amount, 2)

    # --- MM: stock check / auto-replenish, PP: production trigger ---
    pp_status = "Stock Level Verified Stable (MM Module)"
    if item["stock"] < qty:
        replenish = (qty - item["stock"]) + 15
        item["stock"] += replenish
        pp_status = f"PP Trigger Alert: Automatically manufactured {replenish} units via operational execution."
    item["stock"] -= qty

    # --- FICO: post to general ledger (simplified double entry) ---
    finance["cash_balance"] += total_cost
    inv_number = f"GZ-INV-{int(time.time())}"
    date_str = time.strftime("%Y-%m-%d %H:%M:%S")

    gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Cash / Customer Receivable A/c", "debit": round(total_cost, 2), "credit": 0.0})
    gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Sales Revenue A/c", "debit": 0.0, "credit": round(taxable_value, 2)})
    if cgst:
        gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Output CGST Payable A/c", "debit": 0.0, "credit": cgst})
        gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Output SGST Payable A/c", "debit": 0.0, "credit": sgst})
    else:
        gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Output IGST Payable A/c", "debit": 0.0, "credit": igst})

    # --- FICO: customer account book (running statement) ---
    record = customer_ledger.setdefault(client_name, {"balance": 0.0, "entries": []})
    record["balance"] = round(record["balance"] + total_cost, 2)
    record["entries"].append({
        "date": date_str,
        "invoice_no": inv_number,
        "product": item["name"],
        "qty": qty,
        "total": round(total_cost, 2),
        "running_balance": record["balance"],
    })

    invoice = {
        "invoice_no": inv_number,
        "date": date_str,
        "client": client_name,
        "product_name": item["name"],
        "category": item["cat"],
        "qty": qty,
        "base_price": round(base_price, 2),
        "discount_pct": discount_pct,
        "discount_value": round(discount_val, 2),
        "taxable_value": round(taxable_value, 2),
        "gst_rate": gst_rate,
        "cgst": cgst,
        "sgst": sgst,
        "igst": igst,
        "total": round(total_cost, 2),
        "pp_info": pp_status,
        "ledger_log": f"DR Cash/Receivable A/c (+₹{total_cost:,.2f}) | CR Sales Revenue A/c (₹{taxable_value:,.2f}) | CR GST Payable A/c (₹{gst_amount:,.2f})",
    }
    return jsonify(invoice)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
