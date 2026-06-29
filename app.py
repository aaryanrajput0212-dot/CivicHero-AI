"""
CivicHero AI - Main Flask Application
Google for Developers x Coding Ninjas Vibe2Ship Hackathon
"""

import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv
from database.db import (
    init_db, get_all_issues, get_issue_by_id, add_issue,
    upvote_issue, update_issue_status, get_stats, add_comment, get_comments,
    get_leaderboard, search_issues, get_issues_by_category, get_monthly_trends,
    # Auth functions
    create_user, get_user_by_email, get_user_by_id, update_user_password,
    create_reset_token, verify_reset_token, mark_token_used
)
from ai.gemini_service import analyze_issue_with_gemini, get_ai_citywide_insights, chat_with_gemini

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "civichero-2026-secret-key-xyz")

# Custom Jinja2 filters
app.jinja_env.filters['from_json'] = json.loads

# ── Upload Config ──────────────────────────────────
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "mp4", "mov", "webm"}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Auth Decorators ────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated


def get_current_user():
    if "user_id" in session:
        return get_user_by_id(session["user_id"])
    return None


# Inject current_user into all templates
@app.context_processor
def inject_user():
    return {"current_user": get_current_user()}


# ── Init DB on startup ─────────────────────────────
with app.app_context():
    init_db()


# ══════════════════════════════════════════════════
#  AUTH — REGISTER
# ══════════════════════════════════════════════════
@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        # Validation
        if not name or not email or not password:
            flash("All fields are required.", "error")
            return render_template("auth/register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("auth/register.html")

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("auth/register.html")

        if get_user_by_email(email):
            flash("An account with this email already exists.", "error")
            return render_template("auth/register.html")

        hashed = generate_password_hash(password)
        user_id = create_user(name, email, hashed)

        if user_id:
            session["user_id"]   = user_id
            session["user_name"] = name
            session["user_email"]= email
            flash(f"🎉 Welcome to CivicHero AI, {name}! Let's make the city better.", "success")
            return redirect(url_for("index"))
        else:
            flash("Registration failed. Please try again.", "error")

    return render_template("auth/register.html")


# ══════════════════════════════════════════════════
#  AUTH — LOGIN
# ══════════════════════════════════════════════════
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember")

        user = get_user_by_email(email)

        if not user or not check_password_hash(dict(user)["password_hash"], password):
            flash("Invalid email or password.", "error")
            return render_template("auth/login.html", email=email)

        u = dict(user)
        session["user_id"]   = u["id"]
        session["user_name"] = u["name"]
        session["user_email"]= u["email"]

        if remember:
            session.permanent = True

        flash(f"👋 Welcome back, {u['name']}!", "success")
        next_url = request.args.get("next") or url_for("index")
        return redirect(next_url)

    return render_template("auth/login.html", email="")


# ══════════════════════════════════════════════════
#  AUTH — LOGOUT
# ══════════════════════════════════════════════════
@app.route("/logout")
def logout():
    name = session.get("user_name", "")
    session.clear()
    flash(f"👋 Goodbye, {name}! You've been logged out.", "success")
    return redirect(url_for("login"))


# ══════════════════════════════════════════════════
#  AUTH — FORGOT PASSWORD
# ══════════════════════════════════════════════════
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user  = get_user_by_email(email)

        if user:
            token = create_reset_token(dict(user)["id"])
            reset_link = url_for("reset_password", token=token, _external=True)
            # In production: send email. For demo, show the link in flash.
            flash(f"✅ Password reset link generated! (Demo mode — copy this link): {reset_link}", "info")
        else:
            # Security: don't reveal if email exists
            flash("If that email is registered, you'll receive reset instructions.", "success")

        return redirect(url_for("forgot_password"))

    return render_template("auth/forgot_password.html")


# ══════════════════════════════════════════════════
#  AUTH — RESET PASSWORD
# ══════════════════════════════════════════════════
@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user_id = verify_reset_token(token)
    if not user_id:
        flash("This reset link is invalid or has expired (valid for 1 hour).", "error")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("auth/reset_password.html", token=token)

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("auth/reset_password.html", token=token)

        hashed = generate_password_hash(password)
        update_user_password(user_id, hashed)
        mark_token_used(token)

        flash("✅ Password reset successfully! Please log in with your new password.", "success")
        return redirect(url_for("login"))

    return render_template("auth/reset_password.html", token=token)


# ══════════════════════════════════════════════════
#  AUTH — PROFILE
# ══════════════════════════════════════════════════
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        action = request.form.get("action")

        if action == "change_password":
            current  = request.form.get("current_password", "")
            new_pass = request.form.get("new_password", "")
            confirm  = request.form.get("confirm_password", "")
            u = dict(user)

            if not check_password_hash(u["password_hash"], current):
                flash("Current password is incorrect.", "error")
            elif len(new_pass) < 6:
                flash("New password must be at least 6 characters.", "error")
            elif new_pass != confirm:
                flash("New passwords do not match.", "error")
            else:
                update_user_password(u["id"], generate_password_hash(new_pass))
                flash("✅ Password changed successfully!", "success")

        return redirect(url_for("profile"))

    stats = get_stats()
    return render_template("auth/profile.html", user=dict(user), stats=stats, active_page="profile")


# ══════════════════════════════════════════════════
#  HOME
# ══════════════════════════════════════════════════
@app.route("/")
def index():
    stats          = get_stats()
    recent_issues  = get_all_issues(limit=6)
    ai_insight     = get_ai_citywide_insights()
    leaderboard    = get_leaderboard(limit=5)
    all_issues_json = json.dumps([dict(i) for i in get_all_issues(limit=50)])
    return render_template(
        "index.html",
        stats=stats,
        recent_issues=recent_issues,
        ai_insight=ai_insight,
        leaderboard=leaderboard,
        all_issues_json=all_issues_json,
        active_page="home"
    )


# ══════════════════════════════════════════════════
#  ISSUES LIST
# ══════════════════════════════════════════════════
@app.route("/issues")
def issues():
    category = request.args.get("category", "")
    status   = request.args.get("status", "")
    q        = request.args.get("q", "")
    page     = int(request.args.get("page", 1))

    if q:
        all_issues = search_issues(q)
    elif category:
        all_issues = get_issues_by_category(category)
    else:
        all_issues = get_all_issues()

    if status:
        all_issues = [i for i in all_issues if dict(i).get("status") == status]

    per_page   = 9
    total      = len(all_issues)
    total_pages = max(1, (total + per_page - 1) // per_page)
    start      = (page - 1) * per_page
    paginated  = all_issues[start:start + per_page]
    stats      = get_stats()

    return render_template(
        "issues.html",
        issues=paginated, stats=stats,
        category=category, status=status, q=q,
        page=page, total_pages=total_pages, total=total,
        active_page="issues"
    )


# ══════════════════════════════════════════════════
#  REPORT ISSUE  ← FIXED
# ══════════════════════════════════════════════════
@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    if request.method == "POST":
        title       = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category    = request.form.get("category", "Other").strip() or "Other"
        location    = request.form.get("location", "").strip()
        lat         = request.form.get("lat", "0").strip() or "0"
        lng         = request.form.get("lng", "0").strip() or "0"
        priority    = request.form.get("priority", "medium").strip()
        reporter    = session.get("user_name", "Anonymous")

        # Validation
        errors = []
        if not title:        errors.append("Issue title is required.")
        if not description:  errors.append("Description is required.")
        if not location:     errors.append("Location is required.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("report.html", active_page="report",
                                   form_data=request.form)

        # Image upload
        image_path = None
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename and allowed_file(file.filename):
                filename  = secure_filename(file.filename)
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(save_path)
                image_path = filename

        # Video upload
        video_path = None
        if "video" in request.files:
            vfile = request.files["video"]
            if vfile and vfile.filename and allowed_file(vfile.filename):
                vname  = secure_filename(vfile.filename)
                vsave  = os.path.join(app.config["UPLOAD_FOLDER"], vname)
                vfile.save(vsave)
                video_path = vname

        # Gemini AI analysis (graceful fallback)
        try:
            ai_result = analyze_issue_with_gemini(title, description, category, image_path)
        except Exception:
            ai_result = {}

        try:
            lat_f = float(lat)
            lng_f = float(lng)
        except ValueError:
            lat_f = lng_f = 0.0

        issue_id = add_issue(
            title=title,
            description=description,
            category=ai_result.get("category", category),
            location=location,
            lat=lat_f,
            lng=lng_f,
            priority=ai_result.get("priority", priority),
            reporter=reporter,
            image_path=image_path,
            video_path=video_path,
            ai_summary=ai_result.get("summary", ""),
            ai_severity=ai_result.get("severity", priority),
            ai_department=ai_result.get("department", "Municipal Corporation"),
            ai_action=ai_result.get("recommended_action", ""),
            ai_eta=ai_result.get("estimated_resolution", "3-5 days"),
            ai_confidence=int(ai_result.get("confidence", 85)),
            status="open"
        )

        flash(f"✅ Issue #{issue_id} reported successfully! AI has analyzed and routed it.", "success")
        return redirect(url_for("issue_detail", issue_id=issue_id))

    return render_template("report.html", active_page="report",
                           here_api_key=os.getenv("HERE_API_KEY", ""),
                           form_data={})


# ══════════════════════════════════════════════════
#  ISSUE DETAIL
# ══════════════════════════════════════════════════
@app.route("/issue/<int:issue_id>")
def issue_detail(issue_id):
    data = get_issue_by_id(issue_id)
    if not data:
        flash("Issue not found.", "error")
        return redirect(url_for("issues"))
    comments = get_comments(issue_id)
    return render_template(
        "issue_details.html",
        issue=data["issue"], timeline=data["timeline"],
        comments=comments,
        here_api_key=os.getenv("HERE_API_KEY", ""),
        active_page="issues"
    )


# ══════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════
@app.route("/dashboard")
def dashboard():
    stats       = get_stats()
    monthly     = get_monthly_trends()
    all_issues  = get_all_issues()
    ai_insight  = get_ai_citywide_insights()
    leaderboard = get_leaderboard(limit=5)
    issues_json = json.dumps([dict(i) for i in all_issues])
    return render_template(
        "dashboard.html",
        stats=stats, monthly=monthly, issues_json=issues_json,
        ai_insight=ai_insight, leaderboard=leaderboard,
        active_page="dashboard"
    )


# ══════════════════════════════════════════════════
#  LIVE MAP
# ══════════════════════════════════════════════════
@app.route("/map")
def live_map():
    all_issues  = get_all_issues()
    issues_json = json.dumps([dict(i) for i in all_issues])
    return render_template("map.html", issues_json=issues_json,
                           here_api_key=os.getenv("HERE_API_KEY", ""),
                           active_page="map")


# ══════════════════════════════════════════════════
#  COMMUNITY
# ══════════════════════════════════════════════════
@app.route("/community")
def community():
    leaderboard = get_leaderboard(limit=10)
    stats       = get_stats()
    return render_template("community.html", leaderboard=leaderboard,
                           stats=stats, active_page="community")


# ══════════════════════════════════════════════════
#  ANALYTICS
# ══════════════════════════════════════════════════
@app.route("/analytics")
def analytics():
    stats   = get_stats()
    monthly = get_monthly_trends()
    return render_template("analytics.html", stats=stats, monthly=monthly,
                           active_page="analytics")


# ══════════════════════════════════════════════════
#  API ENDPOINTS
# ══════════════════════════════════════════════════
# ══════════════════════════════════════════════════
# API ENDPOINTS
# ══════════════════════════════════════════════════

@app.route("/api/issues")
def api_issues():
    return jsonify([dict(i) for i in get_all_issues()])


@app.route("/api/stats")
def api_stats():
    return jsonify(get_stats())


@app.route("/api/upvote/<int:issue_id>", methods=["POST"])
def api_upvote(issue_id):
    return jsonify({
        "success": True,
        "upvotes": upvote_issue(issue_id)
    })


@app.route("/api/status/<int:issue_id>", methods=["POST"])
def api_update_status(issue_id):
    new_status = request.json.get("status")

    if new_status in ["open", "in_progress", "resolved", "closed"]:
        update_issue_status(issue_id, new_status)
        return jsonify({"success": True})

    return jsonify({"success": False}), 400


@app.route("/api/comment/<int:issue_id>", methods=["POST"])
def api_comment(issue_id):
    data = request.json or {}

    author = session.get(
        "user_name",
        data.get("author", "Anonymous")
    )

    comment = data.get("comment", "").strip()

    if not comment:
        return jsonify({"success": False}), 400

    add_comment(issue_id, author, comment)

    return jsonify({"success": True})


@app.route("/api/monthly-trends")
def api_monthly():
    return jsonify(get_monthly_trends())


@app.route("/api/search")
def api_search():
    q = request.args.get("q", "")

    if not q:
        return jsonify([])

    return jsonify([dict(i) for i in search_issues(q)])


# ══════════════════════════════════════════════════
# CHATBOT API
# ══════════════════════════════════════════════════

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json or {}

    message = data.get("message", "").strip()
    history = data.get("history", [])

    if not message:
        return jsonify({
            "reply": "Please ask me something!"
        }), 400

    try:
        reply = chat_with_gemini(message, history)

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        print("Chat API Error:", e)

        return jsonify({
            "reply": "Sorry, I couldn't connect to Gemini."
        }), 500


# ══════════════════════════════════════════════════
# ERROR HANDLERS
# ══════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(413)
def too_large(e):
    flash("File too large. Maximum 50MB allowed.", "error")
    return redirect(url_for("report"))


# ══════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False
    )