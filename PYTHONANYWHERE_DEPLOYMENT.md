# PythonAnywhere Deployment Guide

**PythonAnywhere is perfect for Django apps!** Simple web-based setup, no command line needed.

## Why PythonAnywhere?
✅ **Free tier** - 512MB storage included  
✅ **Python-optimized** - Built for Django  
✅ **Web interface** - No CLI needed  
✅ **Auto-HTTPS** - Free SSL certificates  
✅ **Easy setup** - 10 minutes to live  
✅ **Beginner-friendly** - Great UI  

---

## **Step 1: Create PythonAnywhere Account**

1. Go to https://www.pythonanywhere.com/
2. Click **"Sign Up"**
3. Choose **"Beginner"** account (Free)
4. Complete registration with email

---

## **Step 2: Set Up Web App**

After login:

1. Click **"Web"** tab at top
2. Click **"Add a new web app"**
3. Select **"Python 3.10"** (or latest)
4. Choose **"Django"** framework

---

## **Step 3: Clone Your Repository**

Go to **"Consoles"** tab:

1. Click **"Bash"** console
2. Run these commands one by one:

```bash
# Navigate to web apps folder
cd /home/yourusername

# Clone your GitHub repo
git clone https://github.com/rehanafzal779/lab4.git mysite

# Enter directory
cd mysite

# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 mysite

# Install requirements
pip install -r requirements.txt

# Create superuser (for admin)
python manage.py createsuperuser
```

---

## **Step 4: Configure WSGI File**

1. Click **"Web"** tab
2. Click **"WSGI configuration file"**
3. Replace with this:

```python
# ============ DJANGO ============
import os
import sys

# Add your project directory to sys.path
project_home = '/home/yourusername/mysite'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace `yourusername` with your PythonAnywhere username!**

---

## **Step 5: Set Environment Variables**

In **"Web"** tab, find **"Environment variables"** section:

Click **"Add a new environment variable"** and add:

| Variable | Value |
|----------|-------|
| SECRET_KEY | Generate from https://djecrety.ir/ |
| DEBUG | False |
| ALLOWED_HOSTS | yourusername.pythonanywhere.com |
| CORS_ALLOWED_ORIGINS | https://your-frontend.com |

---

## **Step 6: Configure Static/Media Files**

Still in **"Web"** tab, find **"Static files"** section:

Add these mappings:

| URL | Directory |
|-----|-----------|
| /static/ | /home/yourusername/mysite/static/ |
| /media/ | /home/yourusername/mysite/media/ |

---

## **Step 7: Reload Web App**

At top of **"Web"** tab, click **"Reload"** button

Green checkmark = App is live!

---

## **Step 8: Test Your API**

Once reloaded, test endpoints:

```bash
# Health check
curl https://yourusername.pythonanywhere.com/api/health/

# Run inference
curl -X POST https://yourusername.pythonanywhere.com/api/inference/ \
  -F "image=@image.jpg" \
  -F "confidence=0.5"
```

Expected response:
```json
{"status": "ok", "message": "API is running"}
```

---

## **Step 9: Admin Panel**

Access Django admin:

```
https://yourusername.pythonanywhere.com/admin/

Username: (your superuser)
Password: (your superuser password)
```

---

## **Step 10: Set Up Auto-Deploy**

To auto-deploy when you push to GitHub:

In **"Consoles"** → **"Bash"**:

```bash
cd /home/yourusername/mysite

# Create deploy script
cat > deploy.sh << 'EOF'
#!/bin/bash
cd /home/yourusername/mysite
git pull origin main
python manage.py migrate --noinput
python manage.py collectstatic --noinput
touch /var/www/yourusername_pythonanywhere_com_wsgi.py
EOF

chmod +x deploy.sh
```

Then use GitHub webhooks or manually run:
```bash
./deploy.sh
```

---

## **Update After Git Push**

To update your app after pushing changes:

1. Go to **"Consoles"** → **"Bash"**
2. Run:

```bash
cd /home/yourusername/mysite
git pull origin main
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

3. Go to **"Web"** tab
4. Click **"Reload"** button

---

## **Useful Commands**

In **"Consoles"** → **"Bash"**:

```bash
# Navigate to your app
cd /home/yourusername/mysite

# Activate virtual environment
workon mysite

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# View logs
tail -f /var/log/yourusername.pythonanywhere.com.log
```

---

## **View Logs**

1. Click **"Web"** tab
2. Scroll down to **"Log files"**
3. Click on:
   - **Server log** - Gunicorn/web server
   - **Error log** - Python errors
   - **Access log** - Request history

---

## **Troubleshooting**

### App Shows 502 Error
1. Check **"Error log"** in Web tab
2. Look for Python/Django errors
3. Common: Missing packages, wrong WSGI config
4. Click **"Reload"** after fixing

### Model Download Failed
- PythonAnywhere has internet access
- Model auto-downloads on first inference
- Check error log if fails
- Manually trigger inference to retry

### Database Issues
- SQLite works by default
- For PostgreSQL: Upgrade to paid account
- SQLite files in: `/home/yourusername/mysite/`

### Permission Denied Errors
- Make sure paths use your actual username
- Check directory permissions: `ls -la`

---

## **Free Tier Limits**

PythonAnywhere Free includes:
- ✅ 512MB storage
- ✅ 1 web app
- ✅ Python 3.10
- ✅ SQLite database
- ✅ HTTPS certificate
- ✅ 100 CPU seconds/day (enough for API)

Perfect for testing and demos!

---

## **Upgrade Later (Optional)**

If you need:
- More storage (1GB/2GB/5GB)
- PostgreSQL database
- Custom domain
- Always-on service

Click **"Account"** → **"Upgrade"** anytime.

---

## **That's It!** 🎉

Your API is now live on PythonAnywhere with:
✅ Simple web-based setup  
✅ Django-optimized hosting  
✅ Auto-downloading YOLOv8 model  
✅ Free HTTPS/SSL  
✅ Easy to update (git pull + reload)  
✅ Perfect for learning & demos  

**Your live API:** `https://yourusername.pythonanywhere.com/api/health/`

Ready? Go to **https://www.pythonanywhere.com/** now! 🚀
