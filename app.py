from flask import (
    Flask,
    request,
    redirect,
    url_for,
    session,
    send_from_directory,
    render_template,
    abort
)
import os
from flask_wtf.csrf import CSRFProtect

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from pathlib import Path
import uuid
import mysql.connector


# =============================
# APP CONFIGURATION
# =============================

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    static_folder=str(BASE_DIR),
    static_url_path="/static"
)

#secret key
app.config["SECRET_KEY"] = os.environ.get("CAMPUSFIX_SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError(
        "CAMPUSFIX_SECRET_KEY environment variable is not set."
    )

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

csrf = CSRFProtect(app)


# =============================
# UPLOAD CONFIGURATION
# =============================

UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp",
    "mp4",
    "webm",
    "mov"
}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

# =============================
# DATABASE CONNECTION
# =============================
import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "campusfix"),
        port=int(os.getenv("DB_PORT", "3306"))
    )
# =============================
# COMMON STYLED ERROR PAGE
# =============================

def show_error(title, message, status_code=400, back_url="/login",
               back_text="Back to Login"):

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">
        <title>{title} | CampusFix</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>

    <body>
        <div class="header">CampusFix</div>

        <div class="login-container">
            <h2>{title}</h2>
            <p>{message}</p>
            <a href="{back_url}">{back_text}</a>
        </div>
    </body>
    </html>
    """, status_code
# =============================
# HOME PAGE
# =============================

@app.route("/")
def index():
    return render_template("index.html")


# =============================
# COMPLAINT PAGE
# =============================

@app.route("/complaint")
def complaint_page():
    return render_template("complaint.html")


# =============================
# ABOUT PAGE
# =============================

@app.route("/about")
def about():
    return render_template("about.html")


# =============================
# REGISTER PAGE
# =============================

@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


# =============================
# STUDENT REGISTRATION
# =============================

@app.route("/register", methods=["POST"])
def register_student():

    name = request.form.get("fullName", "").strip()
    student_id = request.form.get("studentId", "").strip()
    department = request.form.get("department", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirmPassword", "")

    if not all([
        name,
        student_id,
        department,
        email,
        password,
        confirm_password
    ]):
        return "Please fill in all required fields.", 400

    if password != confirm_password:
        return "Passwords do not match. Please try again.", 400

    if len(password) < 8:
        return "Password must be at least 8 characters long.", 400

    hashed_password = generate_password_hash(password)

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check duplicate email or Student ID
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s OR student_id = %s
            """,
            (email, student_id)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            return (
                "An account with this email or Student ID already exists.",
                409
            )

        cursor.execute(
            """
            INSERT INTO users
            (name, student_id, department, email, password)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                name,
                student_id,
                department,
                email,
                hashed_password
            )
        )

        conn.commit()

        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">
            <title>Registration Successful | CampusFix</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body class="registration-success">
            <div class="header">CampusFix</div>
            <div class="login-container">
                <h2>Registration Successful!</h2>
                <p>Your CampusFix account has been created.</p>
                <a href="/login">Go to Login</a>
            </div>
        </body>
        </html>
        """, 201

    except mysql.connector.Error as e:
        if conn:
            conn.rollback()

        print("Registration database error:", e)

        return "Registration failed. Check the VS Code terminal.", 500

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# =============================
# STUDENT LOGIN
# =============================

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")

    login_id = request.form.get("loginId", "").strip()
    password = request.form.get("password", "")

    if not login_id or not password:
        return "Please enter Student ID/email and password.", 400

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, student_id, email, password
            FROM users
            WHERE student_id = %s OR email = %s
            """,
            (login_id, login_id.lower())
        )

        user = cursor.fetchone()

        if user and check_password_hash(
            user["password"],
            password
        ):
            session.clear()
            session["user_id"] = user["id"]
            session["student_name"] = user["name"]

            return redirect(url_for("my_complaints"))

        if not login_id or not password:
            return show_error(
        "Missing Login Details",
        "Please enter your Student ID/email and password.",
        400
    )
        if not login_id or not password:
            return show_error(
        "Missing Login Details",
        "Please enter your Student ID/email and password.",
        400
    )

       

    except mysql.connector.Error as e:
        print("Login database error:", e)

        return "Login failed. Check the VS Code terminal.", 500

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# =============================
# MY COMPLAINTS
# =============================

@app.route("/my-complaints")
def my_complaints():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                title,
                description,
                category,
                location,
                priority,
                status,
                created_at
            FROM complaints
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (session["user_id"],)
        )

        complaints = cursor.fetchall()

        return render_template(
            "my_complaints.html",
            complaints=complaints,
            student_name=session.get(
                "student_name",
                "Student"
            )
        )

    except mysql.connector.Error as e:
        print("My complaints error:", e)

        return (
            "Could not load your complaints. "
            "Check the VS Code terminal.",
            500
        )

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# =============================
# SUBMIT COMPLAINT
# =============================

@app.route("/submit-complaint", methods=["POST"])
def submit_complaint():

    # Student must be logged in
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()
    location = request.form.get("location", "").strip()
    other_location = request.form.get("otherLocation", "").strip()
    priority = request.form.get("priority", "").strip()

    if not all([
        title,
        category,
        description,
        location,
        priority
    ]):
        return "Please fill in all required fields.", 400

    if location == "Other":
        location = other_location

        if not location:
            return "Please specify the location.", 400

    # Get optional uploaded file
    uploaded_file = request.files.get("evidence")
    saved_filename = None
    saved_path = None

    if uploaded_file and uploaded_file.filename:

        original_filename = secure_filename(
            uploaded_file.filename
        )

        if not original_filename:
            return "Invalid filename.", 400

        if not allowed_file(original_filename):
            return (
                "Unsupported file type. "
                "Please upload an image or video.",
                400
            )

        extension = original_filename.rsplit(".", 1)[1].lower()

        # Generate a unique filename
        saved_filename = f"{uuid.uuid4().hex}.{extension}"
        saved_path = UPLOAD_FOLDER / saved_filename

        try:
            uploaded_file.save(saved_path)

        except OSError as e:
            print("File save error:", e)
            return "Could not save the uploaded file.", 500

    user_id = session["user_id"]

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO complaints
            (
                user_id,
                title,
                description,
                category,
                location,
                priority,
                image
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user_id,
                title,
                description,
                category,
                location,
                priority,
                saved_filename
            )
        )

        conn.commit()

        complaint_id = cursor.lastrowid

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">
            <title>Complaint Submitted | CampusFix</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div class="header">CampusFix</div>
            <div class="login-container">
                <h2>Complaint Submitted Successfully!</h2>
                <p>Complaint ID: {complaint_id}</p>
                <p>Status: Pending</p>
                <p>Your complaint has been recorded.</p>

                <a href="/complaint">
                    Submit Another Complaint
                </a>

                <br><br>

                <a href="/my-complaints">
                    View My Complaints
                </a>

                <br><br>

                <a href="/">
                    Back to Home
                </a>
            </div>
        </body>
        </html>
        """

    except mysql.connector.Error as e:
        if conn:
            conn.rollback()

        # Remove saved file if database insertion failed
        if saved_path and saved_path.exists():
            saved_path.unlink()

        print("Complaint submission error:", e)

        return (
            "Could not submit complaint. "
            "Check the VS Code terminal.",
            500
        )

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# =============================
# ADMIN-ONLY UPLOADED FILE VIEW
# =============================

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):

    # Only logged-in admin can view evidence
    if "admin_id" not in session:
        abort(403)

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# =============================
# ADMIN LOGIN
# =============================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "GET":
        return render_template("admin_login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not email or not password:
        return "Please enter email and password.", 400

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, password
            FROM admins
            WHERE email = %s
            """,
            (email,)
        )

        admin = cursor.fetchone()

        if admin and check_password_hash(
            admin["password"],
            password
        ):
            session.clear()
            session["admin_id"] = admin["id"]
            session["admin_name"] = admin["name"]

            return redirect(url_for("admin_dashboard"))


            return show_error(
        "Invalid Admin Email or Password",
    "Please check your details and try again.",
    401,
    "/admin/login",
    "Try Again"
)

    

    except mysql.connector.Error as e:
        print("Admin login error:", e)

        return "Admin login failed. Check terminal.", 500

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()



# =============================
# ADMIN DASHBOARD
# =============================

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    # Read search and filter values from URL
    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "").strip()
    category_filter = request.args.get("category", "").strip()

    allowed_statuses = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch complaints with student details
        # Apply search, status and category filters
        query = """
            SELECT
                c.id,
                c.title,
                c.description,
                c.category,
                c.location,
                c.priority,
                c.status,
                c.image,
                c.created_at,
                u.name AS student_name,
                u.student_id,
                u.email AS student_email
            FROM complaints c
            LEFT JOIN users u
                ON c.user_id = u.id
            WHERE 1=1
        """

        params = []

        if search:
            query += """
                AND (
                    c.title LIKE %s
                    OR u.name LIKE %s
                    OR u.student_id LIKE %s
                    OR c.description LIKE %s
                )
            """
            search_value = f"%{search}%"
            params.extend([
                search_value,
                search_value,
                search_value,
                search_value
            ])

        if status_filter in allowed_statuses:
            query += " AND c.status = %s"
            params.append(status_filter)

        if category_filter:
            query += " AND c.category = %s"
            params.append(category_filter)

        query += " ORDER BY c.created_at DESC"

        cursor.execute(query, tuple(params))
        complaints = cursor.fetchall()

        # Dashboard statistics (always show all complaints)
        cursor.execute(
            "SELECT COUNT(*) AS total FROM complaints"
        )
        total = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM complaints
            WHERE status = 'Pending'
        """)
        pending = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM complaints
            WHERE status = 'In Progress'
        """)
        in_progress = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM complaints
            WHERE status = 'Resolved'
        """)
        resolved = cursor.fetchone()["total"]

        # Get available categories for dropdown
        cursor.execute("""
            SELECT DISTINCT category
            FROM complaints
            WHERE category IS NOT NULL
              AND category != ''
            ORDER BY category
        """)
        categories = [
            row["category"]
            for row in cursor.fetchall()
        ]

        return render_template(
            "admin_dashboard.html",
            complaints=complaints,
            admin_name=session.get("admin_name", "Admin"),
            total=total,
            pending=pending,
            in_progress=in_progress,
            resolved=resolved,
            categories=categories,
            search=search,
            status_filter=status_filter,
            category_filter=category_filter
        )

    except mysql.connector.Error as e:
        print("Admin dashboard error:", e)
        return (
            "Could not load dashboard. Check terminal.",
            500
        )

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

@app.route(
    "/admin/update-status/<int:complaint_id>",
    methods=["POST"]
)
def update_complaint_status(complaint_id):

    # Only logged-in admin can update status
    if "admin_id" not in session:
        abort(403)

    new_status = request.form.get("status", "").strip()

    allowed_statuses = {
        "Pending",
        "In Progress",
        "Resolved"
    }

    if new_status not in allowed_statuses:
        return "Invalid complaint status.", 400

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE complaints
            SET status = %s
            WHERE id = %s
            """,
            (new_status, complaint_id)
        )

        if cursor.rowcount == 0:
            conn.rollback()
            return "Complaint not found.", 404

        conn.commit()

        return redirect(url_for("admin_dashboard"))

    except mysql.connector.Error as e:
        if conn:
            conn.rollback()

        print("Status update error:", e)
        return "Could not update complaint status.", 500

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

# =============================
# ADMIN LOGOUT
# =============================

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_id", None)
    session.pop("admin_name", None)

    return redirect(url_for("admin_login"))


# =============================
# STUDENT LOGOUT
# =============================

@app.route("/logout")
def student_logout():

    session.clear()

    return redirect(url_for("login_page"))


# =============================
# FILE SIZE ERROR
# =============================

@app.errorhandler(413)
def file_too_large(error):
    return (
        "File is too large. Please upload a file under 20 MB.",
        413
    )


# =============================
# RUN SERVER
# =============================

if __name__ == "__main__":
    app.run(debug=False)