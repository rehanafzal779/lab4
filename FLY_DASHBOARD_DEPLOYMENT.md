# Deploy via Fly.io Web Dashboard (No CLI Required)

## **Step 1: Create Fly.io Account**
1. Go to https://fly.io/
2. Click **"Sign Up"**
3. Use GitHub to sign up (recommended) - just authorize
4. Complete setup

## **Step 2: Create New App from Git**
1. In Fly.io Dashboard, click **"Create an app"**
2. Click **"Deploy from GitHub"**
3. Search for your repo: `lab4`
4. Click to select it
5. Click **"Deploy"**

## **Step 3: Configure Environment Variables**
1. Go to your app → **Settings** → **Secrets**
2. Add these secrets:

```
SECRET_KEY = [Generate one: https://bit.ly/django-secret-key]
DEBUG = False
ALLOWED_HOSTS = your-app-name.fly.dev
```

To generate SECRET_KEY online:
- Go to: https://djecrety.ir/
- Copy the generated key
- Paste into SECRET_KEY in Fly.io dashboard

## **Step 4: Add Postgres (Optional)**
If you want database persistence:
1. Click **"Create"** in dashboard
2. Select **"PostgreSQL"**
3. Select same region as your app
4. Click **"Create & Attach"**
5. Fly.io automatically sets `DATABASE_URL`

## **Step 5: Deploy!**
1. Click **"Deploy"** button
2. Watch the build logs
3. When green, your app is live!

## **Step 6: Test Your API**
```bash
# Replace with your app name
curl https://your-app-name.fly.dev/api/health/
```

Should return:
```json
{"status": "ok", "message": "API is running"}
```

## **View Logs**
1. Go to **Logs** tab in dashboard
2. Watch real-time deployment logs

## **Check Status**
1. Go to **Monitoring** tab
2. See CPU, Memory, Requests metrics

---

## That's It! 🎉

Your API is now live on Fly.io's free tier with:
✅ Unlimited storage
✅ Auto-downloaded YOLOv8 model
✅ Global deployment
✅ HTTPS/SSL included
✅ Health monitoring

**Your API URL:** `https://your-app-name.fly.dev`

