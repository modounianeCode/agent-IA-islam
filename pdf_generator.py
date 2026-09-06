from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import os
from datetime import datetime


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data", "pdf")


def _ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def _get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitleCustom",
        parent=styles["Title"],
        fontSize=20,
        spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        name="InfoStyle",
        parent=styles["Normal"],
        fontSize=11,
        spaceAfter=5
    ))
    return styles


def generate_receipt_pdf(receipt):
    _ensure_output_dir()
    filename = f"recu_{receipt['id']}_{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = _get_styles()
    story = []

    story.append(Paragraph("RECU / QUITTANCE", styles["TitleCustom"]))
    story.append(Spacer(1, 0.5*cm))

    info_data = [
        ["Numero :", f"REC-{receipt['id']:04d}"],
        ["Date :", receipt.get("created_at", "")],
        ["Client :", receipt.get("client_name", "")],
        ["Telephone :", receipt.get("client_phone", "")],
        ["Adresse :", receipt.get("client_address", "")],
    ]
    info_table = Table(info_data, colWidths=[4*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph("<b>Details du paiement :</b>", styles["InfoStyle"]))
    story.append(Spacer(1, 0.3*cm))

    items = receipt.get("items", [])
    table_data = [["Description", "Qte", "Prix Unitaire", "Total"]]
    total = 0
    for item in items:
        qty = item.get("quantity", 1)
        price = item.get("unit_price", 0)
        line_total = qty * price
        total += line_total
        table_data.append([
            item.get("description", ""),
            str(qty),
            f"{price:,.2f} FCFA",
            f"{line_total:,.2f} FCFA"
        ])

    table_data.append(["", "", "TOTAL :", f"{total:,.2f} FCFA"])

    items_table = Table(table_data, colWidths=[7*cm, 2*cm, 3.5*cm, 3.5*cm])
    items_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ALIGN", (-1, -1), (-1, -1), "RIGHT"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph(f"<b>Motif :</b> {receipt.get('motif', 'Paiement recu')}", styles["InfoStyle"]))
    story.append(Spacer(1, 1*cm))

    signature_data = [
        ["Signature du client :", "Signature du vendeur :"],
        ["", ""],
        ["_________________________", "_________________________"]
    ]
    sig_table = Table(signature_data, colWidths=[8*cm, 8*cm])
    sig_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(sig_table)

    doc.build(story)
    return filepath


def generate_delivery_pdf(delivery):
    _ensure_output_dir()
    filename = f"bon_livraison_{delivery['id']}_{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = _get_styles()
    story = []

    story.append(Paragraph("BON DE LIVRAISON", styles["TitleCustom"]))
    story.append(Spacer(1, 0.5*cm))

    info_data = [
        ["Numero :", f"BL-{delivery['id']:04d}"],
        ["Date :", delivery.get("created_at", "")],
        ["Client :", delivery.get("client_name", "")],
        ["Telephone :", delivery.get("client_phone", "")],
        ["Adresse livraison :", delivery.get("delivery_address", "")],
        ["Date livraison prevue :", delivery.get("expected_date", "")],
    ]
    info_table = Table(info_data, colWidths=[5*cm, 11*cm])
    info_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph("<b>Articles a livrer :</b>", styles["InfoStyle"]))
    story.append(Spacer(1, 0.3*cm))

    items = delivery.get("items", [])
    table_data = [["Description", "Qte", "Poids/Volume", "Observations"]]
    for item in items:
        table_data.append([
            item.get("description", ""),
            str(item.get("quantity", 1)),
            item.get("weight", ""),
            item.get("notes", "")
        ])

    items_table = Table(table_data, colWidths=[5*cm, 2*cm, 3*cm, 6*cm])
    items_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph(f"<b>Remarques :</b> {delivery.get('remarks', 'Aucune')}", styles["InfoStyle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"<b>Livre par :</b> {delivery.get('carrier', 'Non renseigne')}", styles["InfoStyle"]))
    story.append(Spacer(1, 1.5*cm))

    sign_data = [
        ["Signature du receveur :", "Signature du livreur :"],
        ["", ""],
        ["_________________________", "_________________________"]
    ]
    sig_table = Table(sign_data, colWidths=[8*cm, 8*cm])
    sig_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(sig_table)

    doc.build(story)
    return filepath
