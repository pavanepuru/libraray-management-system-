# 🚀 Step-by-Step Guide: Deploying Mayura LMS on Render

Render ([render.com](https://render.com)) allows you to host your Python Flask web application online for **FREE** with automatic HTTPS and a live public `.onrender.com` URL.

---

## 📦 What We Have Prepared for Render

Your project is already configured with all required Render deployment files:
1. `requirements.txt` — Specifies `Flask` and production WSGI server `gunicorn`.
2. `Procfile` — Configured with `web: gunicorn app:app`.
3. `render.yaml` — Render Blueprint specification for free-tier auto-deployment.
4. `database.py` & `app.py` — Auto-seeds all 31 students and binds to `0.0.0.0:$PORT`.
5. `peacock-lms-render-deploy.zip` — Ready-to-upload ZIP package containing all project files.

---

## ⚡ Step 1: Upload Project to GitHub (2 Minutes)

Render connects directly to GitHub. 

1. Go to [github.com](https://github.com) and log in (or sign up free).
2. Click the **`+`** icon in the top right corner and click **"New repository"**.
3. Name your repository: `peacock-library-system`.
4. Choose **Public** and click **"Create repository"**.
5. On the new repository page, click the link that says **"uploading an existing file"** (or drag & drop):
   - You can unzip `peacock-lms-render-deploy.zip` and drag all files into GitHub, OR drag the files from your folder:
     * `app.py`
     * `database.py`
     * `Procfile`
     * `render.yaml`
     * `requirements.txt`
     * `templates/` (folder)
     * `static/` (folder)
     * `README.md`
6. Click **"Commit changes"**.

---

## 🌐 Step 2: Deploy on Render (1 Minute)

1. Go to [dashboard.render.com](https://dashboard.render.com) and sign in with your GitHub account.
2. In the Render Dashboard, click the blue **"New +"** button in the top right.
3. Select **"Web Service"**.
4. Choose **"Build and deploy from a Git repository"** and click **Next**.
5. Connect your GitHub account and select your repository: **`peacock-library-system`**.
6. Render will automatically configure the settings from `render.yaml`. Verify the following:
   * **Name**: `mayura-peacock-lms` (or any custom name)
   * **Language**: `Python 3`
   * **Branch**: `main`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:app`
   * **Instance Type**: **Free**
7. Click the green button: **"Deploy Web Service"** (or "Create Web Service").

---

## 🎉 Step 3: Access Your Live Application

1. Render will start the build log:
   * It installs `Flask` and `gunicorn`.
   * It initializes SQLite and seeds all 31 students.
   * In approximately 60–90 seconds, you will see `Your service is live 🎉`.
2. Look at the top left of the Render page: your live URL will be displayed, e.g.:
   ```
   https://mayura-peacock-lms.onrender.com
   ```
3. Click your live URL to view and share your **Mayura Peacock Library Management System** with your faculty, evaluators, and friends from any phone, laptop, or tablet!
