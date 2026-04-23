# Step 1: Create new file
# app/routes/pdf_routes.py
import os
from flask import Blueprint, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from app.services.db_service import get_db_connection
from app.utils.auth_decorator import token_required

pdf_bp = Blueprint("pdf", __name__)


@pdf_bp.route("/report/<int:report_id>/pdf")
@token_required
def download_report_pdf(report_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                issue,
                location,
                status,
                mobile,
                priority,
                confidence,
                assigned_to,
                created_at
            FROM reports
            WHERE id = ?
        """, (report_id,))

        report = cursor.fetchone()

        cursor.close()
        db.close()

        if not report:
            return {
                "status": "error",
                "message": "Report not found"
            }, 404

        filename = f"report_{report_id}.pdf"

        file_path = os.path.join(
            os.getcwd(),
            filename
        )

        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()
        elements = []

        title = Paragraph(
            "Complaint Report Details",
            styles["Title"]
        )

        elements.append(title)
        elements.append(Spacer(1, 20))

        fields = [
            f"Report ID: {report['id']}",
            f"Name: {report['name']}",
            f"Issue: {report['issue']}",
            f"Location: {report['location']}",
            f"Status: {report['status']}",
            f"Mobile: {report['mobile']}",
            f"Priority: {report['priority']}",
            f"Confidence: {report['confidence']}",
            f"Assigned To: {report['assigned_to']}",
            f"Created At: {report['created_at']}"
        ]

        for item in fields:
            elements.append(
                Paragraph(item, styles["Normal"])
            )
            elements.append(
                Spacer(1, 10)
            )

        doc.build(elements)

        return send_file(
            file_path,
            as_attachment=True
        )

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500