# Replit Deployment Guide

**Replit is perfect for this project!** Your app already has `replit.nix` configured.

## Why Replit?
✅ **Unlimited storage** - No size limits  
✅ **Always-on** - Project runs 24/7  
✅ **Paid tier** - $7/month (very cheap)  
✅ **Free tier** - Works but need to keep tab open  
✅ **Easy setup** - Just connect GitHub  
✅ **Web editor** - Code in browser  

---

## **Step 1: Create Replit Account**

1. Go to https://replit.com/
2. Click **"Sign Up"**
3. Use GitHub to sign up (easiest)

---

## **Step 2: Import Your Project**

1. In Replit, click **"Create Repl"**
2. Click **"Import from GitHub"**
3. Paste repo URL: `https://github.com/rehanafzal779/lab4`
4. Click **"Import"**

Replit automatically detects:
- ✅ Python project
- ✅ `replit.nix` configuration
- ✅ Requirements installation

---

## **Step 3: Wait for Setup**

Replit will:
1. Clone your repo
2. Read `replit.nix`
3. Install Python 3.11
4. Install all dependencies (pip install -r requirements.txt)
5. Show "Run" button

Takes 2-5 minutes.

---

## **Step 4: Configure Environment Variables**

Click **"Secrets"** button (lock icon on left):

Add these:

```
SECRET_KEY=generate-from-https://djecrety.ir/
DEBUG=False
ALLOWED_HOSTS=*.replit.dev
CORS_ALLOWED_ORIGINS=https://your-frontend.com
```

---

## **Step 5: Create Superuser (Admin)**

Click **"Run"** button to start app:

```bash
python manage.py createsuperuser
```

When asked:
- **Username:** admin (or your choice)
- **Email:** your email
- **Password:** your password

---

## **Step 6: Start Your API**

In Replit console, run:

```bash
python manage.py runserver 0.0.0.0:8000
```

Replit will show a URL like:
```
https://lab4.rehanafzal779.repl.co
```

---

## **Step 7: Test Your API**

Click the URL provided by Replit, then:

```
https://lab4.rehanafzal779.repl.co/api/health/
```

Should return: `{"status": "ok", "message": "API is running"}`

---

## **Step 8: Go Production (Optional - $7/month)**

To keep your app **always running**:

1. Click **"Upgrade to Paid"** in Replit
2. Choose **"Hacker"** plan ($7/month)
3. Your app runs 24/7 without stopping

---

## **Admin Panel**

```
https://lab4.rehanafzal779.repl.co/admin/

Username: admin
Password: (your superuser password)
```

---

## **Update Your Code**

To push new code:

1. **In your local terminal:**
   ```bash
   git push origin main
   ```

2. **In Replit:**
   - Click **"Version Control"** (git icon)
   - Click **"Pull"** to get latest changes
   - Click **"Run"** to restart

---

## **View Logs**

In Replit:
1. Click **"Output"** tab
2. See real-time console output
3. Check for errors

---

## **Troubleshooting**

### App Won't Start
- Check console for errors
- Make sure all env variables are set
- Click "Run" again

### Import Fails
- Make sure GitHub repo is public
- Or authorize Replit to access private repos

### Too Slow on Free Tier
- Switch to Paid tier ($7/month)
- Always-on ensures fast response

---

## **Storage Comparison**

| Platform | Free Storage | Cost for Unlimited |
|----------|--------------|-------------------|
| PythonAnywhere | 512MB | $5/month |
| Replit | Unlimited | $0 (free) or $7/month |
| Render | Unlimited | $0 (free) |

---

## **Free Replit Setup**

Works perfectly for:
- ✅ Learning & development
- ✅ Testing your API
- ✅ Demos

Just keep your browser tab open!

---

## **That's It!** 🎉

Your API is now live on Replit with:
✅ Unlimited storage  
✅ Auto-downloaded YOLOv8 model  
✅ Zero setup complexity  
✅ Easy to update (git pull)  
✅ Free forever (or upgrade to always-on)  

**Your live API:** `https://lab4.YOUR-USERNAME.repl.co/api/health/`

Ready? Go to **https://replit.com/** now! 🚀
