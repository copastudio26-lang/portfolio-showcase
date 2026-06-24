"""
Ajay's Personal Portfolio & Project Showcase
Flask Backend — app.py (Full API Integration)
"""

import os, json, uuid, requests as req_lib
from pathlib import Path
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, send_from_directory, abort, jsonify
)

# ══════════════════════════════════════════════════════════════
#   🔑 API KEYS — Replace these with your real keys
# ══════════════════════════════════════════════════════════════

import os
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'super-secret-key-ajay-2026')

# Configuration for API Services
EMAILJS_SERVICE_ID = "service_iwf9j7a"
EMAILJS_TEMPLATE_ID = "template_1frvmnc"
EMAILJS_PUBLIC_KEY = "3OKGIOOgYTW4pC-9O"
GITHUB_API_TOKEN = "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"
CLOUDINARY_CLOUD_NAME = "dvbpzyhuu"
CLOUDINARY_API_KEY = "671355172438532"
IPINFO_TOKEN = "149e98358432cb"

@app.route('/')
def index():
    return render_template('index.html', emailjs_key=EMAILJS_PUBLIC_KEY)

if __name__ == "__main__":
    app.run(debug=True)
    
# ══════════════════════════════════════════════════════════════
#   App Setup
# ══════════════════════════════════════════════════════════════

BASE_DIR   = Path(__file__).parent
DATA_FILE  = BASE_DIR / "instance" / "data.json"
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
ZIP_DIR    = UPLOAD_DIR / "zips"
THUMB_DIR  = UPLOAD_DIR / "thumbnails"

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ajay-portfolio-secret-2026")

ADMIN_USERNAME      = "ajay"
ADMIN_PASSWORD_HASH = generate_password_hash("admin123")  # Change this password!

ALLOWED_ZIP = {"zip", "tar", "gz"}
ALLOWED_IMG = {"png", "jpg", "jpeg", "gif", "webp", "svg"}

# ══════════════════════════════════════════════════════════════
#   Data Helpers
# ══════════════════════════════════════════════════════════════

def load_data() -> dict:
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"projects": [], "profile": _default_profile(), "visitors": []}

def save_data(data: dict):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def _default_profile():
    return {
        "name": "Ajay",
        "tagline": "Developer · Hacker · Builder",
        "bio": "I build tools, scripts, and projects — mostly in Python, C, and Bash. Passionate about cybersecurity, automation, and open-source.",
        "skills": ["Python", "C", "Bash", "Flask", "Termux", "Cybersecurity", "Linux"],
        "social": {
            "github":    "https://github.com/" + GITHUB_USERNAME,
            "youtube":   "https://youtube.com/@ajay",
            "instagram": "https://instagram.com/ajay",
            "facebook":  "https://facebook.com/ajay"
        },
        "avatar": ""
    }

def get_project(pid: str) -> dict | None:
    data = load_data()
    return next((p for p in data["projects"] if p["id"] == pid), None)

# ══════════════════════════════════════════════════════════════
#   Auth
# ══════════════════════════════════════════════════════════════

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated

# ══════════════════════════════════════════════════════════════
#   🐙 GITHUB API — Auto-fetch repos
# ══════════════════════════════════════════════════════════════

def fetch_github_repos():
    """Fetch all public repos from GitHub API"""
    try:
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        resp = req_lib.get(
            f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=20",
            headers=headers, timeout=8
        )
        if resp.status_code == 200:
            repos = resp.json()
            result = []
            for r in repos:
                result.append({
                    "id":          "gh_" + str(r["id"]),
                    "title":       r["name"],
                    "description": r.get("description") or "No description provided.",
                    "full_desc":   r.get("description") or "",
                    "tags":        [r["language"]] if r.get("language") else [],
                    "github_url":  r["html_url"],
                    "live_url":    r.get("homepage") or "",
                    "stars":       r["stargazers_count"],
                    "forks":       r["forks_count"],
                    "created_at":  r["created_at"],
                    "updated_at":  r["updated_at"],
                    "source":      "github",       # mark as github-sourced
                    "zip_file":    None,
                    "thumbnail":   None,
                    "downloads":   0,
                    "steps":       [],
                    "code_preview": "",
                    "youtube_url": ""
                })
            return result
    except Exception as e:
        print(f"[GitHub API Error] {e}")
    return []

# ══════════════════════════════════════════════════════════════
#   ☁️ CLOUDINARY API — Upload images & files
# ══════════════════════════════════════════════════════════════

def upload_to_cloudinary(file_path: str, resource_type: str = "image") -> str | None:
    """Upload a file to Cloudinary and return the secure URL"""
    import hashlib, hmac, time
    try:
        timestamp = str(int(time.time()))
        # Build signature
        params_to_sign = f"timestamp={timestamp}"
        sig = hmac.new(
            CLOUDINARY_SECRET.encode(),
            params_to_sign.encode(),
            hashlib.sha256
        ).hexdigest()

        url = f"https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD}/{resource_type}/upload"
        with open(file_path, "rb") as f:
            resp = req_lib.post(url, data={
                "api_key":   CLOUDINARY_API_KEY,
                "timestamp": timestamp,
                "signature": sig,
            }, files={"file": f}, timeout=30)

        if resp.status_code == 200:
            return resp.json().get("secure_url")
    except Exception as e:
        print(f"[Cloudinary Error] {e}")
    return None

def save_upload_cloudinary(file, resource_type="image") -> dict | None:
    """Save uploaded file — tries Cloudinary first, falls back to local"""
    if not file or not file.filename:
        return None

    # Save locally first
    ext  = secure_filename(file.filename).rsplit(".", 1)[-1].lower()
    fname = f"{uuid.uuid4().hex}.{ext}"
    local_dir = THUMB_DIR if resource_type == "image" else ZIP_DIR
    local_path = local_dir / fname
    file.save(local_path)

    # Try uploading to Cloudinary
    cloud_url = upload_to_cloudinary(str(local_path), resource_type)
    if cloud_url:
        return {"type": "cloudinary", "url": cloud_url, "local": fname}
    else:
        # Cloudinary failed — use local file
        return {"type": "local", "url": None, "local": fname}

# ══════════════════════════════════════════════════════════════
#   🌍 IPINFO API — Visitor location tracking
# ══════════════════════════════════════════════════════════════

def get_visitor_info(ip: str) -> dict:
    """Get visitor location from IPinfo"""
    try:
        if ip in ("127.0.0.1", "::1"):
            return {"city": "Localhost", "country": "Dev", "org": "Local"}
        resp = req_lib.get(
            f"https://ipinfo.io/{ip}?token={IPINFO_TOKEN}",
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            return {
                "city":    data.get("city", "Unknown"),
                "region":  data.get("region", ""),
                "country": data.get("country", ""),
                "org":     data.get("org", ""),
                "loc":     data.get("loc", "")
            }
    except Exception as e:
        print(f"[IPinfo Error] {e}")
    return {}

def log_visitor(page: str = "/"):
    """Log a visitor with IP info"""
    try:
        ip   = request.headers.get("X-Forwarded-For", request.remote_addr)
        ip   = ip.split(",")[0].strip()
        info = get_visitor_info(ip)

        data = load_data()
        if "visitors" not in data:
            data["visitors"] = []

        data["visitors"].append({
            "ip":        ip[:15],          # truncate for privacy
            "page":      page,
            "city":      info.get("city",""),
            "country":   info.get("country",""),
            "org":       info.get("org",""),
            "timestamp": datetime.utcnow().isoformat()
        })
        # Keep only last 500 visitors
        data["visitors"] = data["visitors"][-500:]
        save_data(data)
    except Exception as e:
        print(f"[Visitor Log Error] {e}")

# ══════════════════════════════════════════════════════════════
#   Public Routes
# ══════════════════════════════════════════════════════════════

@app.route("/")
def index():
    log_visitor("/")
    data     = load_data()
    projects = sorted(data["projects"], key=lambda p: p.get("created_at", ""), reverse=True)
    tags     = sorted({t for p in projects for t in p.get("tags", [])})
    return render_template("index.html", projects=projects, profile=data["profile"], tags=tags,
                           emailjs_key=EMAILJS_PUBLIC_KEY,
                           emailjs_service=EMAILJS_SERVICE_ID,
                           emailjs_template=EMAILJS_TEMPLATE_ID)

@app.route("/project/<pid>")
def project_detail(pid):
    log_visitor(f"/project/{pid}")
    project = get_project(pid)
    if not project:
        abort(404)
    return render_template("project_detail.html", project=project)

@app.route("/download/<pid>")
def download_zip(pid):
    project = get_project(pid)
    if not project or not project.get("zip_file"):
        abort(404)
    data = load_data()
    for p in data["projects"]:
        if p["id"] == pid:
            p["downloads"] = p.get("downloads", 0) + 1
    save_data(data)

    zip_info = project["zip_file"]
    # Support both old string format and new dict format
    if isinstance(zip_info, dict) and zip_info.get("type") == "cloudinary":
        return redirect(zip_info["url"])
    fname = zip_info if isinstance(zip_info, str) else zip_info.get("local")
    return send_from_directory(ZIP_DIR, fname, as_attachment=True,
                               download_name=f"{project['title']}.zip")

@app.route("/static/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

# ══════════════════════════════════════════════════════════════
#   🐙 GitHub Sync Route (Admin)
# ══════════════════════════════════════════════════════════════

@app.route("/admin/sync-github", methods=["POST"])
@login_required
def sync_github():
    """Sync projects from GitHub repos"""
    repos  = fetch_github_repos()
    data   = load_data()
    # Keep manually added projects, replace github-sourced ones
    manual = [p for p in data["projects"] if p.get("source") != "github"]
    data["projects"] = manual + repos
    save_data(data)
    flash(f"✅ Synced {len(repos)} repos from GitHub!", "success")
    return redirect(url_for("admin_dashboard"))

# ══════════════════════════════════════════════════════════════
#   Admin Auth
# ══════════════════════════════════════════════════════════════

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))
    error = None
    if request.method == "POST":
        uname = request.form.get("username", "").strip()
        pwd   = request.form.get("password", "")
        if uname == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, pwd):
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        error = "Invalid username or password."
    return render_template("admin/login.html", error=error)

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("index"))

# ══════════════════════════════════════════════════════════════
#   Admin Dashboard
# ══════════════════════════════════════════════════════════════

@app.route("/admin")
@login_required
def admin_dashboard():
    data      = load_data()
    projects  = sorted(data["projects"], key=lambda p: p.get("created_at",""), reverse=True)
    total_dl  = sum(p.get("downloads", 0) for p in projects)
    visitors  = data.get("visitors", [])
    # Top countries
    from collections import Counter
    countries = Counter(v["country"] for v in visitors if v.get("country"))
    return render_template("admin/dashboard.html",
                           projects=projects,
                           profile=data["profile"],
                           total_downloads=total_dl,
                           total_visitors=len(visitors),
                           top_countries=countries.most_common(5),
                           github_username=GITHUB_USERNAME)

# ══════════════════════════════════════════════════════════════
#   Admin: Add / Edit Project
# ══════════════════════════════════════════════════════════════

@app.route("/admin/project/new", methods=["GET", "POST"])
@login_required
def admin_new_project():
    if request.method == "POST":
        data = load_data()
        pid  = uuid.uuid4().hex[:12]

        zip_info   = save_upload_cloudinary(request.files.get("zip_file"),   "raw")
        thumb_info = save_upload_cloudinary(request.files.get("thumbnail"),  "image")

        tags  = [t.strip() for t in request.form.get("tags","").split(",")  if t.strip()]
        steps = [s.strip() for s in request.form.get("steps","").split("\n") if s.strip()]

        # Thumbnail URL: prefer Cloudinary URL, else local path
        thumb_url = None
        if thumb_info:
            thumb_url = thumb_info.get("url") or thumb_info.get("local")

        project = {
            "id":           pid,
            "title":        request.form.get("title","").strip(),
            "description":  request.form.get("description","").strip(),
            "full_desc":    request.form.get("full_desc","").strip(),
            "tags":         tags,
            "steps":        steps,
            "code_preview": request.form.get("code_preview","").strip(),
            "youtube_url":  request.form.get("youtube_url","").strip(),
            "github_url":   request.form.get("github_url","").strip(),
            "live_url":     request.form.get("live_url","").strip(),
            "zip_file":     zip_info,
            "thumbnail":    thumb_url,
            "thumbnail_raw": thumb_info,
            "downloads":    0,
            "source":       "manual",
            "created_at":   datetime.utcnow().isoformat(),
        }
        data["projects"].append(project)
        save_data(data)
        flash("Project added successfully! 🎉", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/project_form.html", project=None, action="Add")

@app.route("/admin/project/<pid>/edit", methods=["GET", "POST"])
@login_required
def admin_edit_project(pid):
    data    = load_data()
    project = next((p for p in data["projects"] if p["id"] == pid), None)
    if not project:
        abort(404)

    if request.method == "POST":
        tags  = [t.strip() for t in request.form.get("tags","").split(",")  if t.strip()]
        steps = [s.strip() for s in request.form.get("steps","").split("\n") if s.strip()]

        new_zip   = save_upload_cloudinary(request.files.get("zip_file"),  "raw")
        new_thumb = save_upload_cloudinary(request.files.get("thumbnail"), "image")

        thumb_url = None
        if new_thumb:
            thumb_url = new_thumb.get("url") or new_thumb.get("local")

        project.update({
            "title":        request.form.get("title","").strip(),
            "description":  request.form.get("description","").strip(),
            "full_desc":    request.form.get("full_desc","").strip(),
            "tags":         tags,
            "steps":        steps,
            "code_preview": request.form.get("code_preview","").strip(),
            "youtube_url":  request.form.get("youtube_url","").strip(),
            "github_url":   request.form.get("github_url","").strip(),
            "live_url":     request.form.get("live_url","").strip(),
            "zip_file":     new_zip   or project.get("zip_file"),
            "thumbnail":    thumb_url or project.get("thumbnail"),
            "updated_at":   datetime.utcnow().isoformat(),
        })
        save_data(data)
        flash("Project updated! ✅", "success")
        return redirect(url_for("admin_dashboard"))

    project["tags_str"]  = ", ".join(project.get("tags", []))
    project["steps_str"] = "\n".join(project.get("steps", []))
    return render_template("admin/project_form.html", project=project, action="Edit")

@app.route("/admin/project/<pid>/delete", methods=["POST"])
@login_required
def admin_delete_project(pid):
    data = load_data()
    data["projects"] = [p for p in data["projects"] if p["id"] != pid]
    save_data(data)
    flash("Project deleted.", "info")
    return redirect(url_for("admin_dashboard"))

# ══════════════════════════════════════════════════════════════
#   Admin: Profile
# ══════════════════════════════════════════════════════════════

@app.route("/admin/profile", methods=["GET", "POST"])
@login_required
def admin_profile():
    data = load_data()
    if request.method == "POST":
        skills = [s.strip() for s in request.form.get("skills","").split(",") if s.strip()]
        data["profile"].update({
            "name":    request.form.get("name","").strip(),
            "tagline": request.form.get("tagline","").strip(),
            "bio":     request.form.get("bio","").strip(),
            "skills":  skills,
            "social": {
                "github":    request.form.get("github","").strip(),
                "youtube":   request.form.get("youtube","").strip(),
                "instagram": request.form.get("instagram","").strip(),
                "facebook":  request.form.get("facebook","").strip(),
            }
        })
        save_data(data)
        flash("Profile updated! ✅", "success")
        return redirect(url_for("admin_profile"))
    profile = data["profile"]
    profile["skills_str"] = ", ".join(profile.get("skills", []))
    return render_template("admin/profile_form.html", profile=profile)

# ══════════════════════════════════════════════════════════════
#   Admin: Visitors Analytics
# ══════════════════════════════════════════════════════════════

@app.route("/admin/visitors")
@login_required
def admin_visitors():
    data     = load_data()
    visitors = list(reversed(data.get("visitors", [])))[:100]
    return render_template("admin/visitors.html", visitors=visitors,
                           total=len(data.get("visitors", [])))

# ══════════════════════════════════════════════════════════════
#   API: Contact via EmailJS (frontend handles this)
#   This route just validates server-side
# ══════════════════════════════════════════════════════════════

@app.route("/api/contact", methods=["POST"])
def api_contact():
    """EmailJS sends email directly from frontend — this is just a backup log"""
    body = request.get_json(silent=True) or {}
    name    = body.get("name","").strip()
    email   = body.get("email","").strip()
    message = body.get("message","").strip()
    if not all([name, email, message]):
        return jsonify({"ok": False, "error": "All fields required"}), 400
    # Log the contact attempt
    print(f"[Contact] {name} <{email}>: {message[:80]}")
    return jsonify({"ok": True})

# ══════════════════════════════════════════════════════════════
#   API: Projects (Search/Filter)
# ══════════════════════════════════════════════════════════════

@app.route("/api/projects")
def api_projects():
    tag = request.args.get("tag","").strip()
    q   = request.args.get("q","").strip().lower()
    data = load_data()
    projects = data["projects"]
    if tag:
        projects = [p for p in projects if tag in p.get("tags", [])]
    if q:
        projects = [p for p in projects if q in p["title"].lower() or q in p.get("description","").lower()]
    return jsonify(projects)

# ══════════════════════════════════════════════════════════════
#   Error Handlers
# ══════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    for d in [ZIP_DIR, THUMB_DIR, DATA_FILE.parent]:
        d.mkdir(parents=True, exist_ok=True)
    # Install requests if missing
    try:
        import requests
    except ImportError:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages", "-q"])
    app.run(debug=True, port=5000)
