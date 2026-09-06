from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from storage import add_document, load_documents, get_document, delete_document, export_to_csv
from pdf_generator import generate_receipt_pdf, generate_delivery_pdf

app = Flask(__name__)
app.secret_key = "facturation_app_secret_key_2024"


@app.route("/")
def index():
    receipts = load_documents("receipts")
    deliveries = load_documents("deliveries")
    return render_template("index.html", receipts=receipts, deliveries=deliveries)


@app.route("/recu/nouveau", methods=["GET", "POST"])
def new_receipt():
    if request.method == "POST":
        items = []
        descriptions = request.form.getlist("item_description[]")
        quantities = request.form.getlist("item_quantity[]")
        prices = request.form.getlist("item_price[]")

        for i in range(len(descriptions)):
            if descriptions[i].strip():
                items.append({
                    "description": descriptions[i].strip(),
                    "quantity": int(quantities[i]) if quantities[i] else 1,
                    "unit_price": float(prices[i]) if prices[i] else 0
                })

        receipt = {
            "client_name": request.form.get("client_name", "").strip(),
            "client_phone": request.form.get("client_phone", "").strip(),
            "client_address": request.form.get("client_address", "").strip(),
            "motif": request.form.get("motif", "").strip(),
            "items": items
        }

        add_document("receipts", receipt)
        flash("Recu cree avec succes !", "success")
        return redirect(url_for("list_receipts"))

    return render_template("receipt_form.html")


@app.route("/recus")
def list_receipts():
    receipts = load_documents("receipts")
    return render_template("receipts.html", receipts=receipts)


@app.route("/recu/<int:doc_id>")
def view_receipt(doc_id):
    receipt = get_document("receipts", doc_id)
    if not receipt:
        flash("Recu non trouve.", "error")
        return redirect(url_for("list_receipts"))
    return render_template("receipt_view.html", receipt=receipt)


@app.route("/recu/<int:doc_id>/pdf")
def receipt_pdf(doc_id):
    receipt = get_document("receipts", doc_id)
    if not receipt:
        flash("Recu non trouve.", "error")
        return redirect(url_for("list_receipts"))
    filepath = generate_receipt_pdf(receipt)
    return send_file(filepath, as_attachment=True)


@app.route("/recu/<int:doc_id>/supprimer", methods=["POST"])
def delete_receipt(doc_id):
    delete_document("receipts", doc_id)
    flash("Recu supprime.", "success")
    return redirect(url_for("list_receipts"))


@app.route("/bon-livraison/nouveau", methods=["GET", "POST"])
def new_delivery():
    if request.method == "POST":
        items = []
        descriptions = request.form.getlist("item_description[]")
        quantities = request.form.getlist("item_quantity[]")
        weights = request.form.getlist("item_weight[]")
        notes = request.form.getlist("item_notes[]")

        for i in range(len(descriptions)):
            if descriptions[i].strip():
                items.append({
                    "description": descriptions[i].strip(),
                    "quantity": int(quantities[i]) if quantities[i] else 1,
                    "weight": weights[i].strip() if i < len(weights) else "",
                    "notes": notes[i].strip() if i < len(notes) else ""
                })

        delivery = {
            "client_name": request.form.get("client_name", "").strip(),
            "client_phone": request.form.get("client_phone", "").strip(),
            "delivery_address": request.form.get("delivery_address", "").strip(),
            "expected_date": request.form.get("expected_date", ""),
            "carrier": request.form.get("carrier", "").strip(),
            "remarks": request.form.get("remarks", "").strip(),
            "items": items
        }

        add_document("deliveries", delivery)
        flash("Bon de livraison cree avec succes !", "success")
        return redirect(url_for("list_deliveries"))

    return render_template("delivery_form.html")


@app.route("/bons-livraison")
def list_deliveries():
    deliveries = load_documents("deliveries")
    return render_template("deliveries.html", deliveries=deliveries)


@app.route("/bon-livraison/<int:doc_id>")
def view_delivery(doc_id):
    delivery = get_document("deliveries", doc_id)
    if not delivery:
        flash("Bon de livraison non trouve.", "error")
        return redirect(url_for("list_deliveries"))
    return render_template("delivery_view.html", delivery=delivery)


@app.route("/bon-livraison/<int:doc_id>/pdf")
def delivery_pdf(doc_id):
    delivery = get_document("deliveries", doc_id)
    if not delivery:
        flash("Bon de livraison non trouve.", "error")
        return redirect(url_for("list_deliveries"))
    filepath = generate_delivery_pdf(delivery)
    return send_file(filepath, as_attachment=True)


@app.route("/bon-livraison/<int:doc_id>/supprimer", methods=["POST"])
def delete_delivery(doc_id):
    delete_document("deliveries", doc_id)
    flash("Bon de livraison supprime.", "success")
    return redirect(url_for("list_deliveries"))


@app.route("/export/<doc_type>")
def export_csv(doc_type):
    if doc_type not in ("receipts", "deliveries"):
        flash("Type de document invalide.", "error")
        return redirect(url_for("index"))
    filepath = export_to_csv(doc_type)
    if filepath:
        return send_file(filepath, as_attachment=True)
    flash("Aucune donnee a exporter.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
