pythonimport os
import json
import random
import time
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# 1. DATABASE STATE (In-Memory array of your 30 luxury products in INR)
inventory = {
    # SAREES
    "1": {"name": "Multicolor Zardosi Kanchipuram Silk Saree", "cat": "Sarees", "stock": 15, "price": 149900.0, "bulk_qty": 3, "bulk_disc": 10.0},
    "2": {"name": "Off White Zari Kanchipuram Silk Saree", "cat": "Sarees", "stock": 20, "price": 57000.0, "bulk_qty": 3, "bulk_disc": 10.0},
    "3": {"name": "Pure Handwoven Mulberry Saree", "cat": "Sarees", "stock": 45, "price": 12879.0, "bulk_qty": 5, "bulk_disc": 12.0},
    "4": {"name": "Handloom Chocolate Pink Kanjivaram", "cat": "Sarees", "stock": 30, "price": 13570.0, "bulk_qty": 5, "bulk_disc": 12.0},
    "5": {"name": "Emerald Katan Banarasi Silk Saree", "cat": "Sarees", "stock": 12, "price": 85000.0, "bulk_qty": 3, "bulk_disc": 12.0},
    "6": {"name": "Hand-Painted Pure Floral Organza Saree", "cat": "Sarees", "stock": 25, "price": 42000.0, "bulk_qty": 5, "bulk_disc": 15.0},
    # JEWELRY
    "7": {"name": "Festive 22kt Gold Bead Necklace", "cat": "Jewelry", "stock": 8, "price": 78333.0, "bulk_qty": 2, "bulk_disc": 5.0},
    "8": {"name": "Keya Nakshi 22kt Gold Masterpiece", "cat": "Jewelry", "stock": 3, "price": 794275.0, "bulk_qty": 2, "bulk_disc": 5.0},
    "9": {"name": "Leafy Sanai Engraved Gold Necklace", "cat": "Jewelry", "stock": 10, "price": 95811.0, "bulk_qty": 2, "bulk_disc": 5.0},
    "10": {"name": "Saanvi Royal 22kt Statement Collar", "cat": "Jewelry", "stock": 2, "price": 1002766.0, "bulk_qty": 2, "bulk_disc": 5.0},
    "11": {"name": "Uncut Polki Diamond Choker Set", "cat": "Jewelry", "stock": 4, "price": 650000.0, "bulk_qty": 2, "bulk_disc": 8.0},
    "12": {"name": "Antique Temple Gold Kada Pair", "cat": "Jewelry", "stock": 6, "price": 320000.0, "bulk_qty": 3, "bulk_disc": 5.0},
    # SCENTS
    "13": {"name": "Tom Ford Tobacco Oud EDP", "cat": "Scents", "stock": 40, "price": 76707.0, "bulk_qty": 5, "bulk_disc": 10.0},
    "14": {"name": "Neesh Luxe Aoud Extrait Premium", "cat": "Scents", "stock": 150, "price": 1750.0, "bulk_qty": 10, "bulk_disc": 20.0},
    "15": {"name": "Gissah Imperial Valley 200ml", "cat": "Scents", "stock": 85, "price": 10500.0, "bulk_qty": 5, "bulk_disc": 10.0},
    "16": {"name": "Robert Piguet Oud EDP Classic", "cat": "Scents", "stock": 60, "price": 11999.0, "bulk_qty": 5, "bulk_disc": 10.0},
    "17": {"name": "Royal Ambergris Infused Attar Oil", "cat": "Scents", "stock": 15, "price": 24500.0, "bulk_qty": 10, "bulk_disc": 18.0},
    "18": {"name": "Tuscan Leather & Saffron Intense", "cat": "Scents", "stock": 22, "price": 19000.0, "bulk_qty": 5, "bulk_disc": 10.0},
    # SOAPS
    "19": {"name": "Satjeevan Cold Pressed Oil 5-Pack", "cat": "Soaps", "stock": 200, "price": 900.0, "bulk_qty": 20, "bulk_disc": 15.0},
    "20": {"name": "Aaranyam French Pink Clay 4-Pack", "cat": "Soaps", "stock": 180, "price": 599.0, "bulk_qty": 20, "bulk_disc": 15.0},
    "21": {"name": "Thenpanai Vetiver Marikozhundhu Trio", "cat": "Soaps", "stock": 300, "price": 435.0, "bulk_qty": 30, "bulk_disc": 20.0},
    "22": {"name": "Coral and Sky Virgin Butter Suite", "cat": "Soaps", "stock": 140, "price": 1439.0, "bulk_qty": 15, "bulk_disc": 10.0},
    "23": {"name": "Himalayan Shilajit Treatment Bar", "cat": "Soaps", "stock": 90, "price": 1850.0, "bulk_qty": 50, "bulk_disc": 25.0},
    "24": {"name": "Bulgarian Rose & Goat Milk Pack", "cat": "Soaps", "stock": 110, "price": 2200.0, "bulk_qty": 20, "bulk_disc": 20.0},
    # LUXURY NICHE TEXTILES
    "25": {"name": "Maroon Flush Handwoven Kani Pashmina", "cat": "Niche Luxury", "stock": 5, "price": 526335.0, "bulk_qty": 2, "bulk_disc": 20.0},
    "26": {"name": "Grey Black Reversible Jamawar Shawl", "cat": "Niche Luxury", "stock": 7, "price": 498995.0, "bulk_qty": 2, "bulk_disc": 10.0},
    "27": {"name": "Handloom Sozni Embroidered Shawl", "cat": "Niche Luxury", "stock": 8, "price": 355000.0, "bulk_qty": 2, "bulk_disc": 10.0},
    "28": {"name": "Kashmir Loom Oversize Brown Kani", "cat": "Niche Luxury", "stock": 4, "price": 370000.0, "bulk_qty": 2, "bulk_disc": 10.0},
    "29": {"name": "Ivory Certified Pure Solid Pashmina", "cat": "Niche Luxury", "stock": 14, "price": 85000.0, "bulk_qty": 5, "bulk_disc": 15.0},
    "30": {"name": "Hand-Spun Pure Natural Toosh Scarf", "cat": "Niche Luxury", "stock": 3, "price": 110000.0, "bulk_qty": 3, "bulk_disc": 12.0}
}

finance = {"cash_balance": 25000000.0, "receivables": 0.0, "returns_paid": 0.0}
call_center_logs = []
returns_log = []

# 2. RUNNING LIVE MARKET TICKERS
@app.route('/api/market')
def get_market_tickers():
    return jsonify({
        "Copper Index": f"₹{int(1214300 * random.uniform(0.99, 1.01)):,}/Ton",
        "Steel Index": f"₹{int(60480 * random.uniform(0.98, 1.02)):,}/Ton",
        "Basmati Rice": f"₹{int(94080 * random.uniform(0.995, 1.005)):,}/Ton",
        "Raw Cotton": f"₹{int(154560 * random.uniform(0.97, 1.03)):,}/Ton"
    })

@app.route('/api/products')
def get_products():
    return jsonify(inventory)

# 3. UNIFIED TRANSACTION PIPELINE (SD -> MM -> PP -> FICO -> Payment)
@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json
    prod_id = data.get("id")
    qty = int(data.get("qty", 1))
    
    item = inventory.get(prod_id)
    if not item: return jsonify({"error": "Item mismatch"}), 400
    
    # Tiered Bulk Discount Engine
    base_price = item["price"]
    discount = item["bulk_disc"] if qty >= item["bulk_qty"] else 0.0
    unit_price = base_price * (1 - discount / 100.0)
    total_cost = unit_price * qty
    
    # PP Automated Manufacturing Replenishment Trigger
    pp_status = "Stock Verified (MM)"
    if item["stock"] < qty:
        produced_units = (qty - item["stock"]) + 10
        item["stock"] += produced_units
        pp_status = f"PP Alert: Auto-Manufactured {produced_units} units to prevent pipeline breakdown."
        
    # MM Inventory Adjustment
    item["stock"] -= qty
    
    # FICO Double-Entry Bookkeeping & Online Gateway Simulation
    finance["cash_balance"] += total_cost
    inv_number = f"INV-{int(time.time())}"
    
    return jsonify({
        "status": "PAID & POSTED",
        "invoice_no": inv_number,
        "amount_processed": f"₹{total_cost:,.2f}",
        "pp_info": pp_status,
        "fico_log": f"Debit: Online Cash A/c (+₹{total_cost:,.2f}) | Credit: Finished Goods Asset A/c"
    })

# 4. COMPACT INTEGRATED DASHBOARD LAYOUT
@app.route('/')
def dashboard():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live Integrated Rupee ERP</title>
        <link rel="stylesheet" href="https://jsdelivr.net">
        <script>
            async function fetchMarket() {
                let res = await fetch('/api/market');
                let tickers = await res.json();
                let html = '';
                for(let key in tickers) {
                    html += `<div class="col-md-3"><div class="p-3 bg-dark text-white rounded text-center">
                             <small class="text-warning">${key}</small><h4>${tickers[key]}</h4></div></div>`;
                }
                document.getElementById('ticker-row').innerHTML = html;
            }
            async function loadProducts() {
                let res = await fetch('/api/products');
                let prods = await res.json();
                let html = '';
                for(let id in prods) {
                    html += `<tr>
                        <td><b>${prods[id].name}</b><br><small class="text-muted">${prods[id].cat}</small></td>
                        <td>₹${prods[id].price.toLocaleString('en-IN')}</td>
                        <td>Buy ${prods[id].bulk_qty}+ get ${prods[id].bulk_disc}% off</td>
                        <td><span class="badge bg-info">${prods[id].stock} units</span></td>
                        <td>
                            <input type="number" id="qty-${id}" value="1" min="1" class="form-control d-inline-block w-25 me-2">
                            <button class="btn btn-success btn-sm" onclick="triggerOrder('${id}')">Execute Pay & Order</button>
                        </td>
                    </tr>`;
                }
                document.getElementById('product-table').innerHTML = html;
            }
            async function triggerOrder(id) {
                let qty = document.getElementById('qty-'+id).value;
                let res = await fetch('/api/order', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({id: id, qty: qty})
                });
                let output = await res.json();
                alert(`[ERP INTEGRATION INVOICE GENERATED]\\nInvoice No: ${output.invoice_no}\\nFICO Settlement: ${output.amount_processed}\\nManufacturing Log: ${output.pp_info}\\nLedger: ${output.fico_log}`);
                loadProducts();
            }
            setInterval(fetchMarket, 3000);
            window.onload = function() { fetchMarket(); loadProducts(); };
        </script>
    </head>
    <body class="bg-light p-4">
        <div class="container-fluid">
            <h2 class="mb-4">🇮🇳 Enterprise Integrated Rupee ERP Architecture</h2>
            <div id="ticker-row" class="row g-3 mb-4"></div>
            <div class="card p-3 shadow-sm border-0">
                <h5 class="mb-3">Live Inventory Engine (30 Affluent Market Focus Products)</h5>
                <table class="table align-middle">
                    <thead class="table-dark"><tr><th>Product Mapping</th><th>Base Pricing</th><th>Tiered Bulk Rules</th><th>MM Status</th><th>Execution Gateway</th></tr></thead>
                    <tbody id="product-table"></tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
if name == 'main':app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
