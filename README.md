# 🚀 Ajay Dev — Personal Portfolio & Project Showcase

> A full-stack personal portfolio website to showcase coding projects, scripts, and tools.  
> Built with **Flask (Python)** + **Tailwind CSS** | Deployed on **Render.com**

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?style=flat-square&logo=flask)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-38bdf8?style=flat-square&logo=tailwindcss)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📸 Features

### 🌐 Public Side
- Hero landing page with terminal-style skills card
- Projects grid with **live search** and **tag filter**
- Project detail page with:
  - Step-by-step installation guide
  - Code preview panel (with copy button)
  - YouTube video embed
  - One-click ZIP download
- Social media links (GitHub, YouTube, Instagram, Facebook)

### 🔐 Admin Panel (`/admin`)
- Secure password-protected login
- Add / Edit / Delete projects
- Upload ZIP source files + thumbnail images
- Edit public profile (bio, skills, social links)
- Dashboard with stats (total projects, downloads, top project)

---

## 📁 Project Structure

```
portfolio/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── Procfile                  # For Render/Heroku deployment
├── render.yaml               # Render.com auto-deploy config
├── .gitignore                # Git ignored files
├── .python-version           # Python version pin
├── instance/
│   └── data.json             # Auto-created: all project data (gitignored)
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── uploads/
│       ├── zips/             # Uploaded source ZIPs (gitignored)
│       └── thumbnails/       # Project thumbnails (gitignored)
└── templates/
    ├── base.html
    ├── index.html
    ├── project_detail.html
    ├── 404.html
    └── admin/
        ├── login.html
        ├── dashboard.html
        ├── project_form.html
        └── profile_form.html
```

---

## ⚡ Local Setup (PC / Laptop)

```bash
# Step 1: Clone the repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run the app
python app.py

# Step 4: Open in browser
# http://localhost:5000
```

**Admin Login:**
- URL: `http://localhost:5000/admin/login`
- Username: `ajay`
- Password: `admin123`

> ⚠️ Change password before deploying! (see Environment Variables below)

---

## 🌐 Deploy on Render.com (Free Hosting)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "first commit: portfolio project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2 — Connect to Render
1. Go to [render.com](https://render.com) and Sign Up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your portfolio repository
5. Fill in these settings:

| Setting | Value |
|---|---|
| **Name** | ajay-portfolio |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

### Step 3 — Set Environment Variables
In Render dashboard → **Environment** tab, add these:

| Key | Value |
|---|---|
| `SECRET_KEY` | any random long string (e.g. `ajay2026xyzSecretKey!`) |
| `ADMIN_USERNAME` | `ajay` |
| `ADMIN_PASSWORD` | your secure password |

### Step 4 — Add Persistent Disk (for file uploads)
In Render dashboard → **Disks** tab:
- **Name:** uploads
- **Mount Path:** `/opt/render/project/src/static/uploads`
- **Size:** 1 GB (free tier)

### Step 5 — Deploy!
Click **"Create Web Service"** — Render will build and deploy automatically.  
Your site will be live at: `https://ajay-portfolio.onrender.com`

---

## 🔐 Environment Variables Reference

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Flask session encryption key | `ajay-portfolio-secret-2026` |
| `ADMIN_USERNAME` | Admin panel username | `ajay` |
| `ADMIN_PASSWORD` | Admin panel password | `admin123` |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12 + Flask 3.0 |
| Frontend | HTML5 + Tailwind CSS (CDN) |
| Database | JSON file (no DB needed) |
| Auth | Flask Sessions + Werkzeug password hashing |
| Deployment | Render.com + Gunicorn |
| Fonts | JetBrains Mono + Inter (Google Fonts) |

---

## 📝 License

MIT License — free to use and modify.

---

> Made with ❤️ by Ajay
