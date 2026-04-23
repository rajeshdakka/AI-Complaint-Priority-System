# app/routes/admin_routes.py

from flask import Blueprint, request, redirect
from app.services.db_service import get_db_connection
from app.utils.auth_decorator import token_required
from flask import render_template

admin_bp = Blueprint("admin", __name__)


# -----------------------------------
# Assign Report to Officer
# -----------------------------------
@admin_bp.route("/report/<int:report_id>/assign", methods=["POST"])
@token_required
def assign_report(report_id):

    if request.role != "admin":
        return {
            "status": "error",
            "message": "Admin access only"
        }, 403

    try:
        assigned_to = request.form["assigned_to"]

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            UPDATE reports
            SET assigned_to=?
            WHERE id=?
        """, (
            assigned_to,
            report_id
        ))

        db.commit()
        cursor.close()
        db.close()

        return redirect(f"/report/{report_id}")

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500


# -----------------------------------
# Update Report Status
# -----------------------------------
@admin_bp.route("/report/<int:report_id>/status", methods=["POST"])
@token_required
def update_status(report_id):

    if request.role != "admin":
        return {
            "status": "error",
            "message": "Admin access only"
        }, 403

    try:
        new_status = request.form["status"]

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            UPDATE reports
            SET status=?
            WHERE id=?
        """, (
            new_status,
            report_id
        ))

        db.commit()
        cursor.close()
        db.close()

        return redirect(f"/report/{report_id}")

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500


# -----------------------------------
# Admin Pending Reports
# -----------------------------------
@admin_bp.route("/admin/reports/pending")
@token_required
def admin_pending_reports():

    if request.role != "admin":
        return {
            "status": "error",
            "message": "Admin access only"
        }, 403

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
                created_at
            FROM reports
            WHERE status='pending'
        """)

        rows = cursor.fetchall()

        cursor.close()
        db.close()

        reports = []

        for row in rows:
            reports.append({
                "id": row["id"],
                "name": row["name"],
                "issue": row["issue"],
                "location": row["location"],
                "status": row["status"],
                "created_at": str(row["created_at"])
            })

        return reports

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500

@admin_bp.route("/admin/dashboard")
@token_required
def admin_dashboard():

    if request.role != "admin":
        return {
            "status": "error",
            "message": "Admin access only"
        }, 403

    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Total reports
        cursor.execute("SELECT COUNT(*) FROM reports")
        total_reports = cursor.fetchone()[0]

        # Pending reports
        cursor.execute("SELECT COUNT(*) FROM reports WHERE status='pending'")
        pending_reports = cursor.fetchone()[0]

        # In Progress
        cursor.execute("SELECT COUNT(*) FROM reports WHERE status='in_progress'")
        in_progress_reports = cursor.fetchone()[0]

        # Resolved
        cursor.execute("SELECT COUNT(*) FROM reports WHERE status='resolved'")
        resolved_reports = cursor.fetchone()[0]

        # High priority
        cursor.execute("SELECT COUNT(*) FROM reports WHERE priority='High'")
        high_priority = cursor.fetchone()[0]

        # Medium priority
        cursor.execute("SELECT COUNT(*) FROM reports WHERE priority='Medium'")
        medium_priority = cursor.fetchone()[0]

        # Low priority
        cursor.execute("SELECT COUNT(*) FROM reports WHERE priority='Low'")
        low_priority = cursor.fetchone()[0]

        cursor.close()
        db.close()

        return render_template(
            "admin_dashboard.html",
            total_reports=total_reports,
            pending_reports=pending_reports,
            in_progress_reports=in_progress_reports,
            resolved_reports=resolved_reports,
            high_priority=high_priority,
            medium_priority=medium_priority,
            low_priority=low_priority
        )

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500