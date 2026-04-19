# HuggingFace Spaces Deployment Guide

**HuggingFace Spaces = Free ML hosting with NO CREDIT CARD!**

## Why HuggingFace Spaces?
✅ **NO credit card needed** - Completely free  
✅ **Unlimited storage** - No size limits  
✅ **24/7 uptime** - Always running  
✅ **Perfect for ML** - Made for models like YOLOv8  
✅ **Easy setup** - Just connect GitHub  
✅ **Web interface** - No command line needed  

---

## **Step 1: Create HuggingFace Account**

1. Go to https://huggingface.co/
2. Click **"Sign Up"**
3. Use GitHub to sign up (easiest - NO credit card!)
4. Verify your email

---

## **Step 2: Create New Space**

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in:
   - **Space name:** neat-now-api
   - **License:** OpenRAIL (default)
   - **Space SDK:** Docker
   - **Visibility:** Public

4. Click **"Create Space"**

---

## **Step 3: Connect Your GitHub Repository**

HuggingFace will show you options:

**Option A - Automatic (Recommended):**
1. Click **"Import from GitHub"**
2. Authorize HuggingFace to access your GitHub
3. Select repo: `lab4`
4. Click **"Create Space"**

HuggingFace automatically:
- ✅ Clones your repo
- ✅ Reads your Dockerfile
- ✅ Builds and deploys
- ✅ Creates live URL

---

## **Option B - Manual (If automatic doesn't work):**

1. Click **"Files"** tab
2. Click **"Add file"** → **"Upload files"**
3. Upload your files from: `C:\Users\User\Desktop\New folder`

Essential files to upload:
- `Dockerfile`
- `manage.py`
- `requirements.txt`
- `config/` (settings, urls, wsgi)
- `apps/` (ml_inference, accounts)
- `.env.example`

---

## **Step 4: Set Environment Variables**

In your Space:

1. Click **"Settings"** (gear icon)
2. Scroll to **"Repository secrets"**
3. Click **"Add a secret"**
4. Add these one by one:

```
SECRET_KEY = [generate from https://djecrety.ir/]
DEBUG = False
ALLOWED_HOSTS = huggingface.co
CORS_ALLOWED_ORIGINS = https://huggingface.co
```

---

## **Step 5: Wait for Deployment**

HuggingFace will:
1. Build your Docker image
2. Download YOLOv8 model (~50MB)
3. Run migrations
4. Start your API

Takes 5-10 minutes.

Watch the **"Build logs"** tab to see progress.

---

## **Step 6: Get Your Live URL**

Once deployed (green checkmark), you'll have a URL like:

```
https://huggingface.co/spaces/yourusername/neat-now-api
```

Your API endpoint:
```
https://yourusername-neat-now-api.hf.space/api/health/
```

---

## **Step 7: Test Your API**

```bash
# Health check
curl https://yourusername-neat-now-api.hf.space/api/health/

# Run inference
curl -X POST https://yourusername-neat-now-api.hf.space/api/inference/ \
  -F "image=@image.jpg" \
  -F "confidence=0.5"
```

Expected response:
```json
{"status": "ok", "message": "API is running"}
```

---

## **Admin Panel**

Create superuser in HuggingFace terminal:

1. Click **"App"** tab
2. Click **"Terminal"** button
3. Run:

```bash
python manage.py createsuperuser
```

Then visit:
```
https://yourusername-neat-now-api.hf.space/admin/

Username: admin
Password: (your password)
```

---

## **Update Your Code**

After pushing to GitHub:

1. In HuggingFace Space, click **"Settings"**
2. Scroll to **"Repository"**
3. Click **"Sync with main branch"**

Space automatically redeploys!

Or push directly:

```bash
# In your local terminal
cd "C:\Users\User\Desktop\New folder"
git push origin main
```

HuggingFace syncs automatically every few minutes.

---

## **View Logs**

In your Space:

1. Click **"Build logs"** - See Docker build progress
2. Click **"App"** - See running logs
3. Click **"Terminal"** - Run commands

---

## **Troubleshooting**

### Build Fails
- Check **"Build logs"** tab
- Usually missing dependencies
- Fix and commit to GitHub
- Space auto-rebuilds

### App Won't Start
- Check **"App"** logs tab
- Common: Missing environment variables
- Add to **"Repository secrets"**

### Model Download Fails
- HuggingFace has good internet
- Usually retries automatically
- Check logs for details

### 502 Bad Gateway
- App still starting
- Wait 5 minutes
- Refresh page

---

## **Limitations**

HuggingFace Spaces free tier:

| Resource | Limit |
|----------|-------|
| RAM | 16GB |
| Disk | 50GB |
| CPU | 2 cores |
| Duration | Always on |

Perfect for your ML API!

---

## **Upgrade (Optional)**

If you need more resources:

1. Click **"Settings"**
2. Find **"Hardware"** section
3. Upgrade to:
   - **GPU** - $13/month
   - **More RAM** - Extra cost
   - **Better CPU** - Extra cost

But free tier is plenty for your needs!

---

## **That's It!** 🎉

Your API is now live on HuggingFace Spaces with:
✅ **NO credit card needed**  
✅ Unlimited storage  
✅ 24/7 uptime  
✅ Auto-downloading YOLOv8 model  
✅ Auto-deploy on git push  
✅ Free forever  
✅ Perfect for ML  

**Your live API:** `https://yourusername-neat-now-api.hf.space/api/health/`

**Ready?** Go to **https://huggingface.co/spaces** now! 🚀

---

## **Quick Summary**

| Step | What to Do |
|------|-----------|
| 1 | Sign up at HuggingFace (no credit card!) |
| 2 | Click "Create new Space" |
| 3 | Select "Docker" SDK |
| 4 | Import your GitHub repo |
| 5 | Add environment secrets |
| 6 | Wait for deployment (5 min) |
| 7 | Get your live URL |
| 8 | Test at `/api/health/` |

Done! 🎉
