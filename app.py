import os
import random
import time
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

GST_RATES = {
    "Sarees": 5.0, "Jewelry": 3.0, "Scents": 18.0, "Soaps": 18.0, "Niche Luxury": 12.0,
}
AD_GST_RATE = 18.0  # advertising services

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
for pid, item in inventory.items():
    item["images"] = [
        f"https://picsum.photos/seed/genzsmart{pid}a/500/400",
        f"https://picsum.photos/seed/genzsmart{pid}b/500/400",
        f"https://picsum.photos/seed/genzsmart{pid}c/500/400",
    ]
    item["img"] = item["images"][0]  # kept for backward compatibility
    item["gst_rate"] = GST_RATES.get(item["cat"], 18.0)

# ---------------------------------------------------------------------------
# FICO state
# ---------------------------------------------------------------------------
finance = {"cash_balance": 25000000.0}
gl_entries = []
customer_ledger = {}
QUOTES = {}

# ---------------------------------------------------------------------------
# SD/MM/PP: delivery tracking
# ---------------------------------------------------------------------------
ORDERS = []
DELIVERY_STAGES = ["Processing", "Shipped", "Out for Delivery", "Delivered"]

# ---------------------------------------------------------------------------
# Ad slot marketplace
# ---------------------------------------------------------------------------
AD_SLOTS = {
    "slot1": {"name": "Homepage Banner — Top", "price_per_week": 5000.0, "status": "vacant", "title": None, "contact": None, "expires_at": None},
    "slot2": {"name": "Category Page Sidebar", "price_per_week": 2500.0, "status": "vacant", "title": None, "contact": None, "expires_at": None},
    "slot3": {"name": "Footer Spotlight", "price_per_week": 1500.0, "status": "vacant", "title": None, "contact": None, "expires_at": None},
    "slot4": {"name": "Checkout Confirmation Banner", "price_per_week": 3500.0, "status": "vacant", "title": None, "contact": None, "expires_at": None},
}
AD_QUOTES = {}

commodities = {
    "Gold Spot (22kt/10g)": 72450.0, "Silver Spot (1kg)": 88200.0,
    "Silk Raw Material Index (per Kg)": 4250.0, "Premium Basmati Cotton (per Ton)": 94080.0,
    "Oud Oil (per Tola)": 21500.0, "Rose Absolute (per Kg)": 385000.0,
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
        data.append({"id": f"2026-ROLL-0{i}", "name": f"{first_names[i-1]} {last_names[i-1]}", "dept": random.choice(depts),
                      "sensor": assigned_sensor, "activity": random.choice(activities), "status": status})
    return data


def _release_expired_ads():
    now = time.time()
    for s in AD_SLOTS.values():
        if s["status"] == "booked" and s["expires_at"] and s["expires_at"] < now:
            s.update({"status": "vacant", "title": None, "contact": None, "expires_at": None})


@app.route('/')
def dashboard():
    return render_template('index.html')


@app.route('/api/market')
def get_market_tickers():
    out = []
    for name, base in commodities.items():
        drift = random.uniform(-0.015, 0.015)
        commodities[name] = round(base * (1 + drift), 2)
        out.append({"name": name, "price": f"₹{commodities[name]:,.2f}", "change_pct": round(drift * 100, 2)})
    return jsonify(out)


@app.route('/api/products')
def get_products():
    return jsonify(inventory)


@app.route('/api/traceability')
def get_traceability():
    return jsonify(sample_iot_telemetry())


@app.route('/api/ledger')
def get_gl():
    return jsonify(gl_entries)


@app.route('/api/fico/summary')
def fico_summary():
    """FICO: trial balance (net per account) + headline totals."""
    totals = {}
    for e in gl_entries:
        t = totals.setdefault(e["account"], {"debit": 0.0, "credit": 0.0})
        t["debit"] += e["debit"]
        t["credit"] += e["credit"]
    trial_balance = [
        {"account": k, "debit": round(v["debit"], 2), "credit": round(v["credit"], 2), "net": round(v["debit"] - v["credit"], 2)}
        for k, v in totals.items()
    ]
    total_revenue = sum(v["credit"] for k, v in totals.items() if "Revenue" in k)
    total_gst = sum(v["credit"] for k, v in totals.items() if "Payable" in k)
    return jsonify({
        "cash_balance": round(finance["cash_balance"], 2),
        "total_revenue": round(total_revenue, 2),
        "total_gst_collected": round(total_gst, 2),
        "trial_balance": trial_balance,
    })


@app.route('/api/customer/<name>')
def get_customer_ledger(name):
    record = customer_ledger.get(name)
    if not record:
        return jsonify({"error": "No account history for this customer yet."}), 404
    return jsonify(record)


def _price_breakdown(item, qty, state):
    base_price = item["price"]
    discount_pct = item["bulk_disc"] if qty >= item["bulk_qty"] else 0.0
    unit_price = base_price * (1 - discount_pct / 100.0)
    subtotal = base_price * qty
    discount_val = subtotal * (discount_pct / 100.0)
    taxable_value = unit_price * qty
    gst_rate = item["gst_rate"]
    gst_amount = taxable_value * (gst_rate / 100.0)
    if state == "other":
        igst, cgst, sgst = round(gst_amount, 2), 0.0, 0.0
    else:
        igst = 0.0
        cgst = sgst = round(gst_amount / 2, 2)
    return {
        "base_price": round(base_price, 2), "discount_pct": discount_pct, "discount_value": round(discount_val, 2),
        "taxable_value": round(taxable_value, 2), "gst_rate": gst_rate, "cgst": cgst, "sgst": sgst, "igst": igst,
        "total": round(taxable_value + gst_amount, 2),
    }


@app.route('/api/quote', methods=['POST'])
def create_quote():
    data = request.json or {}
    prod_id = data.get("id")
    qty = int(data.get("qty", 1))
    client_name = (data.get("client_name") or "").strip() or "Walk-In Corporate Matrix Node"
    state = data.get("state", "same")
    item = inventory.get(prod_id)
    if not item:
        return jsonify({"error": "Product reference array mismatch."}), 400
    if qty < 1:
        return jsonify({"error": "Quantity must be at least 1."}), 400
    breakdown = _price_breakdown(item, qty, state)
    quote_id = f"QT-{int(time.time()*1000)}-{random.randint(1000,9999)}"
    QUOTES[quote_id] = {"product_id": prod_id, "qty": qty, "client_name": client_name, "state": state,
                         "product_name": item["name"], "category": item["cat"], **breakdown}
    return jsonify({"quote_id": quote_id, **QUOTES[quote_id]})


@app.route('/api/pay', methods=['POST'])
def pay_quote():
    """Dummy payment gateway — always succeeds. Swap for a real gateway
    (e.g. Razorpay) before accepting real money."""
    data = request.json or {}
    quote_id = data.get("quote_id")
    method = data.get("method", "card")
    quote = QUOTES.pop(quote_id, None)
    if not quote:
        return jsonify({"error": "This quote has expired or was already paid. Please start the order again."}), 400
    item = inventory.get(quote["product_id"])
    if not item:
        return jsonify({"error": "Product no longer available."}), 400

    qty = quote["qty"]
    pp_status = "Stock Level Verified Stable (MM Module)"
    if item["stock"] < qty:
        replenish = (qty - item["stock"]) + 15
        item["stock"] += replenish
        pp_status = f"PP Trigger Alert: Automatically manufactured {replenish} units via operational execution."
    item["stock"] -= qty

    total_cost = quote["total"]
    taxable_value = quote["taxable_value"]
    gst_amount = round(total_cost - taxable_value, 2)
    finance["cash_balance"] += total_cost

    inv_number = f"GZ-INV-{int(time.time())}"
    payment_id = f"PAY-{int(time.time())}-{random.randint(100,999)}"
    date_str = time.strftime("%Y-%m-%d %H:%M:%S")
    client_name = quote["client_name"]

    gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Cash / Customer Receivable A/c", "debit": total_cost, "credit": 0.0})
    gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Sales Revenue A/c", "debit": 0.0, "credit": taxable_value})
    if quote["cgst"]:
        gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Output CGST Payable A/c", "debit": 0.0, "credit": quote["cgst"]})
        gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Output SGST Payable A/c", "debit": 0.0, "credit": quote["sgst"]})
    else:
        gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Output IGST Payable A/c", "debit": 0.0, "credit": quote["igst"]})

    record = customer_ledger.setdefault(client_name, {"balance": 0.0, "entries": []})
    record["balance"] = round(record["balance"] + total_cost, 2)
    record["entries"].append({"date": date_str, "invoice_no": inv_number, "product": quote["product_name"],
                               "qty": qty, "total": total_cost, "running_balance": record["balance"]})

    # --- SD/MM: create a delivery-tracked order ---
    order_id = f"ORD-{int(time.time()*1000)}-{random.randint(1000,9999)}"
    tracking_id = f"TRK-{random.randint(100000,999999)}"
    ORDERS.append({"order_id": order_id, "invoice_no": inv_number, "product_name": quote["product_name"],
                    "qty": qty, "client_name": client_name, "status": DELIVERY_STAGES[0],
                    "tracking_id": tracking_id, "date": date_str})

    invoice = {
        "invoice_no": inv_number, "date": date_str, "client": client_name,
        "product_name": quote["product_name"], "category": quote["category"], "qty": qty,
        "base_price": quote["base_price"], "discount_pct": quote["discount_pct"], "discount_value": quote["discount_value"],
        "taxable_value": taxable_value, "gst_rate": quote["gst_rate"], "cgst": quote["cgst"], "sgst": quote["sgst"], "igst": quote["igst"],
        "total": total_cost, "pp_info": pp_status, "payment_id": payment_id, "payment_method": method,
        "order_id": order_id, "tracking_id": tracking_id,
        "ledger_log": f"DR Cash/Receivable A/c (+₹{total_cost:,.2f}) | CR Sales Revenue A/c (₹{taxable_value:,.2f}) | CR GST Payable A/c (₹{gst_amount:,.2f})",
    }
    return jsonify(invoice)


@app.route('/api/orders')
def list_orders():
    return jsonify(ORDERS)


@app.route('/api/orders/<order_id>/advance', methods=['POST'])
def advance_order(order_id):
    """MM/SD: move an order to the next delivery stage."""
    order = next((o for o in ORDERS if o["order_id"] == order_id), None)
    if not order:
        return jsonify({"error": "Order not found."}), 404
    idx = DELIVERY_STAGES.index(order["status"])
    if idx < len(DELIVERY_STAGES) - 1:
        order["status"] = DELIVERY_STAGES[idx + 1]
    return jsonify(order)


# ---------------------------------------------------------------------------
# Ad slot marketplace — vendors/customers rent a slot by the week
# ---------------------------------------------------------------------------
@app.route('/api/ads')
def list_ad_slots():
    _release_expired_ads()
    return jsonify(AD_SLOTS)


@app.route('/api/ads/quote', methods=['POST'])
def quote_ad():
    _release_expired_ads()
    data = request.json or {}
    slot_id = data.get("slot_id")
    weeks = int(data.get("weeks", 1))
    title = (data.get("title") or "").strip()
    contact = (data.get("contact") or "").strip()

    slot = AD_SLOTS.get(slot_id)
    if not slot:
        return jsonify({"error": "Slot not found."}), 400
    if slot["status"] == "booked":
        return jsonify({"error": "This slot is currently booked. Try another slot or check back later."}), 400
    if not title:
        return jsonify({"error": "Ad title is required."}), 400
    if not contact:
        return jsonify({"error": "A contact (email or phone) is required."}), 400
    if weeks < 1:
        return jsonify({"error": "Minimum booking is 1 week."}), 400

    base = slot["price_per_week"] * weeks
    gst_amount = base * (AD_GST_RATE / 100.0)
    total = round(base + gst_amount, 2)
    quote_id = f"ADQ-{int(time.time()*1000)}-{random.randint(1000,9999)}"
    AD_QUOTES[quote_id] = {"slot_id": slot_id, "slot_name": slot["name"], "weeks": weeks, "title": title,
                            "contact": contact, "base": round(base, 2), "gst": round(gst_amount, 2), "total": total}
    return jsonify({"quote_id": quote_id, **AD_QUOTES[quote_id]})


@app.route('/api/ads/pay', methods=['POST'])
def pay_ad():
    data = request.json or {}
    quote_id = data.get("quote_id")
    method = data.get("method", "card")
    quote = AD_QUOTES.pop(quote_id, None)
    if not quote:
        return jsonify({"error": "This ad quote has expired. Please try again."}), 400
    slot = AD_SLOTS.get(quote["slot_id"])
    if not slot or slot["status"] == "booked":
        return jsonify({"error": "Slot no longer available."}), 400

    expires_at = time.time() + quote["weeks"] * 7 * 24 * 3600
    slot.update({"status": "booked", "title": quote["title"], "contact": quote["contact"], "expires_at": expires_at})
    finance["cash_balance"] += quote["total"]

    inv_number = f"GZ-AD-{int(time.time())}"
    payment_id = f"PAY-{int(time.time())}-{random.randint(100,999)}"
    date_str = time.strftime("%Y-%m-%d %H:%M:%S")

    gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Cash / Advertiser Receivable A/c", "debit": quote["total"], "credit": 0.0})
    gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Advertising Revenue A/c", "debit": 0.0, "credit": quote["base"]})
    gl_entries.append({"date": date_str, "invoice_no": inv_number, "account": "Output GST Payable A/c (Ads)", "debit": 0.0, "credit": quote["gst"]})

    return jsonify({
        "invoice_no": inv_number, "date": date_str, "slot_name": quote["slot_name"], "title": quote["title"],
        "weeks": quote["weeks"], "base": quote["base"], "gst": quote["gst"], "total": quote["total"],
        "payment_id": payment_id, "payment_method": method,
        "expires_on": time.strftime("%Y-%m-%d", time.localtime(expires_at)),
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
