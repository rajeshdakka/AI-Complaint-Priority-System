
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, render_template, current_app
from app.services.db_service import get_db_connection
from app.services.ml_service import predict_priority
from app.utils.auth_decorator import token_required
report_bp = Blueprint("report", __name__)


# -----------------------------------
# Report Form Page
# -----------------------------------
@report_bp.route("/report-form")
@token_required
def report_form():
    return render_template("report.html")


# -----------------------------------
# Submit Complaint
# -----------------------------------
@report_bp.route("/report", methods=["POST"])
@token_required
def submit_report():
    try:
        name = request.form["name"]
        issue = request.form["issue"]
        location = request.form["location"]
        mobile = request.form["mobile"]

        # File Upload Handling

        uploaded_file = request.files.get("proof_file")
        filename = None

        print("FILES:", request.files)
        print("UPLOADED FILE:", uploaded_file)

        if uploaded_file and uploaded_file.filename != "":
            print("ORIGINAL FILENAME:", uploaded_file.filename)
            filename = secure_filename(
                uploaded_file.filename
            )

            print("SAVED FILENAME:", filename)
            
            file_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )

            uploaded_file.save(file_path)

        # ML Prediction
        priority, confidence = predict_priority(issue)

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO reports
            (
                name,
                issue,
                location,
                status,
                users_id,
                mobile,
                priority,
                confidence,
                proof_file
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            issue,
            location,
            "pending",
            request.user_id,
            mobile,
            priority,
            confidence,
            filename
        ))

        db.commit()
        cursor.close()
        db.close()

        return {
            "status": "success",
            "priority": priority,
            "confidence": round(confidence, 2),
            "uploaded_file": filename
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500
# -----------------------------------
# View Reports
# -----------------------------------

@report_bp.route("/reports")
@token_required
def get_reports():
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Search + Filter Inputs
        search = request.args.get("search", "")
        priority_filter = request.args.get("priority", "")
        status_filter = request.args.get("status", "")

        base_query = """
            SELECT
                id,
                name,
                issue,
                location,
                status,
                created_at,
                mobile,
                priority,
                confidence,
                proof_file
            FROM reports
            WHERE 1=1
        """

        params = []

        # User-specific access
        if request.role != "admin":
            base_query += " AND users_id=?"
            params.append(request.user_id)

        # Search by name / issue / location
        if search:
            base_query += """
                AND (
                    name LIKE ?
                    OR issue LIKE ?
                    OR location LIKE ?
                )
            """
            search_value = f"%{search}%"
            params.extend([
                search_value,
                search_value,
                search_value
            ])

        # Priority filter
        if priority_filter:
            base_query += " AND priority=?"
            params.append(priority_filter)

        # Status filter
        if status_filter:
            base_query += " AND status=?"
            params.append(status_filter)

        cursor.execute(base_query, tuple(params))
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
                "created_at": str(row["created_at"]),
                "mobile": row["mobile"],
                "priority": row["priority"],
                "proof_file": row["proof_file"],
                "confidence": round(row["confidence"], 2)
                if row["confidence"] else None
                
            })

        return render_template(
            "reports.html",
            reports=reports,
            role=request.role,
            search=search,
            priority_filter=priority_filter,
            status_filter=status_filter
        )

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500

# -----------------------------------
# Report Detail
# -----------------------------------
@report_bp.route("/report/<int:report_id>")
@token_required
def report_detail(report_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        if request.role == "admin":
            cursor.execute("""
                SELECT *
                FROM reports
                WHERE id=?
            """, (report_id,))
        else:
            cursor.execute("""
                SELECT *
                FROM reports
                WHERE id=? AND users_id=?
            """, (
                report_id,
                request.user_id
            ))

        report = cursor.fetchone()

        cursor.close()
        db.close()

        if not report:
            return "Report not found", 404

        return render_template(
            "report_detail.html",
            report=report
        )

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500