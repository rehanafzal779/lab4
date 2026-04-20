# Render.com Deployment Guide

**Render is the best Heroku replacement!** It's free, reliable, and handles Docker apps perfectly.

## Why Render?
✅ **Free tier** - Works great for your app  
✅ **No 4GB limit** - Unlimited storage  
✅ **Docker support** - Uses your existing Dockerfile  
✅ **Auto-deploy** - Redeploys on git push  
✅ **HTTPS included** - Free SSL certificates  
✅ **Easy to use** - Simple dashboard  

---

## **Step 1: Create Render Account**

1. Go to https://render.com/
2. Click **"Sign Up"**
3. Use GitHub to sign up (recommended)
4. Authorize Render to access your GitHub

---

## **Step 2: Create New Service**

1. In Render Dashboard, click **"New +"**
2. Select **"Web Service"**
3. Choose **"Build and deploy from a Git repository"**
4. Click **"Connect account"** (authorize GitHub if needed)

---

## **Step 3: Select Your Repository**

1. Search for: `lab4`
2. Click to select your repo
3. Click **"Connect"**

---

## **Step 4: Configure Deployment**

Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | neat-now-api |
| **Environment** | Docker |
| **Branch** | main |
| **Build Command** | (leave empty) |
| **Start Command** | gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120 |

---

## **Step 5: Set Environment Variables**

Scroll down to **"Environment"** section and add:

1. Click **"Add Environment Variable"**
2. Add these one by one:

```
SECRET_KEY = [Generate from https://djecrety.ir/]
DEBUG = False
ALLOWED_HOSTS = neat-now-api.onrender.com
DATABASE_URL = (Leave empty for SQLite)
CORS_ALLOWED_ORIGINS = https://your-frontend.com
```

**To generate SECRET_KEY:**
- Go to https://djecrety.ir/
- Copy the long string
- Paste in SECRET_KEY field in Render dashboard

---

## **Step 6: Select Plan**

Choose **"Free"** plan at the bottom

---

## **Step 7: Deploy!**

Click **"Create Web Service"**

Render will:
1. ✅ Clone your repo
2. ✅ Build Docker image
3. ✅ Download YOLOv8 model (~50MB)
4. ✅ Run migrations
5. ✅ Start your API
6. ✅ Generate HTTPS certificate

**Deployment takes 5-10 minutes**

---

## **Step 8: Monitor Deployment**

1. Watch the **"Logs"** section
2. Look for green checkmark when done
3. Your API URL will be shown at the top

Example: `https://neat-now-api.onrender.com`

---

## **Step 9: Test Your API**

Once deployment is complete:

```bash
# Health check
curl https://neat-now-api.onrender.com/api/health/

# Run inference
curl -X POST https://neat-now-api.onrender.com/api/inference/ \
  -F "image=@image.jpg" \
  -F "confidence=0.5"
```

Expected response:
```json
{"status": "ok", "message": "API is running"}
```

---

## **Auto-Deploy on Git Push**

Once connected, every time you push to GitHub:
```bash
git push origin main
```

Render automatically:
- ✅ Pulls your changes
- ✅ Rebuilds Docker image
- ✅ Restarts your API
- ✅ Zero downtime

---

## **View Logs**

In Render dashboard:
1. Select your service
2. Click **"Logs"** tab
3. See real-time application logs

---

## **Useful Links**

- **Dashboard:** https://dashboard.render.com/
- **Your API:** https://neat-now-api.onrender.com/
- **Admin Panel:** https://neat-now-api.onrender.com/admin/
- **API Docs:** https://neat-now-api.onrender.com/api/

---

## **Troubleshooting**

### App Won't Start
1. Check **Logs** tab
2. Look for Python/Django errors
3. Verify all environment variables are set

### 502 Bad Gateway
- Usually means app is still starting
- Wait 5 minutes and refresh
- Check logs for errors

### Model Download Failed
- Check logs for urllib/network errors
- Render has good internet, usually works
- If fails, redeploy (click **"Manual Deploy"**)

### Database Issues
- For SQLite: Files stored in `/data` directory
- For PostgreSQL: Add from **"Create"** button

---

## **Free Tier Limits**

Render free tier includes:
- ✅ 1 active service
- ✅ 750 hours/month (always on)
- ✅ Unlimited outbound bandwidth
- ✅ Unlimited storage
- ✅ Automatic HTTPS

Perfect for your ML API!

---

## **Upgrade Later (Optional)**

If you need:
- Multiple services
- Always-on guarantee
- More resources

Click **"Settings"** → **"Plan"** to upgrade anytime.

---

## **That's It!** 🎉

Your API is now live on Render.com with:
✅ Unlimited storage (no 4GB limit!)  
✅ Auto-downloading YOLOv8 model  
✅ Auto-deploy on git push  
✅ Free HTTPS/SSL  
✅ Global CDN  
✅ 24/7 uptime  

**Your live API:** `https://neat-now-api.onrender.com`

Ready to deploy? Go to **https://render.com/** now! 🚀
