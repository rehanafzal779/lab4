# Railway Deployment Guide

## Step-by-Step Railway Deployment

## Step-by-Step Railway Deployment

### Prerequisites
- Railway account: https://railway.app
- GitHub account with your code
- **No need for best.pt!** Model downloads automatically on deployment

### Step 1: Prepare Your Code

Copy environment template:
```bash
cp .env.example .env
```

Update `.env` with your settings:
```
SECRET_KEY=generate-with-django-command  # See below
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app
# Optional: ML_MODEL_PATH=./best.pt  # Only if you have custom model
```

**Note:** The API uses YOLOv8m by default, which auto-downloads (~49MB).
If you have a custom trained model, set `ML_MODEL_PATH=./best.pt` in Railway variables.

Generate SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 2: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit - YOLOv8 ML API"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

### Step 3: Connect Railway

1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Select your repository
5. Click "Deploy"

### Step 4: Configure Environment Variables

In Railway Dashboard:

1. Go to your project → Variables
2. Add these variables:

| Variable | Value | Required |
|----------|-------|----------|
| `SECRET_KEY` | Generate with command above | Yes |
| `DEBUG` | `False` | Yes |
| `ALLOWED_HOSTS` | `your-app.railway.app` | Yes |
| `ML_MODEL_PATH` | Leave empty for auto-download, or `./best.pt` | Optional |
| `DATABASE_URL` | Auto from PostgreSQL | Optional |
| `CORS_ALLOWED_ORIGINS` | Your frontend domain | No |

### Step 5: Add Database (Optional)

For production, add PostgreSQL:

1. Click "Create" in Railway Dashboard
2. Select "PostgreSQL"
3. Railway automatically sets `DATABASE_URL`
4. Click "Deploy"

For development, SQLite is used by default.

### Step 6: Deploy

Railway automatically detects `Dockerfile` and deploys.

Watch the deployment:
1. Go to "Deployments" tab
2. See real-time build logs
3. Once green, your app is live!

### Step 7: Verify Deployment

Test your API:

```bash
# Health check
curl https://your-app.railway.app/api/health/

# Or with browser
# https://your-app.railway.app/api/health/
```

Expected response:
```json
{"status": "ok", "message": "API is running"}
```

## Using Your API

### Run Inference

```bash
curl -X POST https://your-app.railway.app/api/inference/ \
  -F "image=@your-image.jpg" \
  -F "confidence=0.5"
```

### View History

```bash
curl https://your-app.railway.app/api/history/?limit=10
```

### Admin Panel

```
https://your-app.railway.app/admin/

Username: (your superuser)
Password: (your superuser password)
```

## Monitoring & Logs

### View Logs

In Railway Dashboard:
1. Select your project
2. Click "Logs" tab
3. See real-time application logs

### Monitor Metrics

Railway provides:
- CPU usage
- Memory usage
- Network I/O
- Request count

In Railway Dashboard → Metrics tab.

## Scaling & Performance

### Increase Workers

Edit `Dockerfile`:
```dockerfile
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "8"]
```

Default is 4 workers. Increase for more concurrency.

### Enable GPU (Optional)

For faster inference, use Railway GPU:
1. Go to Settings → Compute
2. Select GPU instance
3. Deploy

Note: GPU instances cost more but inference is ~10x faster.

### Use PostgreSQL (Recommended)

Add PostgreSQL service in Railway for:
- Better performance
- Better scalability
- Persistent data across restarts

## Troubleshooting

### 500 Error
Check logs in Railway Dashboard → Logs tab.

Common causes:
- Model file not found → Ensure `best.pt` in root
- DATABASE_URL not set → Add PostgreSQL or use SQLite
- Missing environment variable → Check .env settings

### Model Not Found
```
FileNotFoundError: Model not found at ./best.pt
```

Solution:
1. Ensure `best.pt` is in repository root
2. Commit and push to GitHub
3. Railway will rebuild and deploy

### Slow Inference
First inference loads the model (slow). Subsequent requests are faster.

For faster inference:
- Use GPU instance
- Use smaller model
- Process smaller images

### CORS Errors
Update `CORS_ALLOWED_ORIGINS` in Railway variables:
```
CORS_ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:3000
```

## Security Checklist

- [ ] Set `DEBUG=False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Set `CORS_ALLOWED_ORIGINS` for your frontend
- [ ] Use PostgreSQL in production
- [ ] Enable HTTPS (automatic on Railway)
- [ ] Create superuser for admin panel
- [ ] Set secure database password

## Environment Variables Reference

```bash
# Django
SECRET_KEY=your-secret-key-here          # REQUIRED
DEBUG=False                              # REQUIRED (False in production)
ALLOWED_HOSTS=your-app.railway.app       # REQUIRED

# Database
DATABASE_URL=postgresql://...            # Optional (defaults to SQLite)

# CORS
CORS_ALLOWED_ORIGINS=your-frontend.com   # Optional

# ML Model
ML_MODEL_PATH=./best.pt                  # Optional (default)

# Port
PORT=8000                                # Railway sets this automatically
```

## Advanced Configuration

### Custom Domain

1. Buy domain (GoDaddy, Namecheap, etc.)
2. In Railway → Settings → Domains
3. Add your domain
4. Update DNS records as instructed
5. HTTPS certificate auto-generated

### Database Backups

Railway auto-backups PostgreSQL. Access backups in:
Railway Dashboard → PostgreSQL → Backups

### CI/CD Pipeline

Railway auto-deploys on push to main branch.

For custom CI/CD:
1. Go to Settings → Build & Deploy
2. Configure deployment triggers
3. Set environment variables per branch

## Still Having Issues?

1. **Check Railway Logs:** Go to Logs tab for error messages
2. **Test Locally:** Run `python manage.py runserver` locally first
3. **Read Error Messages:** They often tell you what's wrong
4. **Check Model File:** `ls -la best.pt` confirms file exists
5. **Verify Variables:** Go to Variables tab and confirm all set

## Support Resources

- **Railway Docs:** https://docs.railway.app/
- **Django Docs:** https://docs.djangoproject.com/
- **YOLOv8 Docs:** https://docs.ultralytics.com/
- **GitHub Issues:** Post issues in repository

---

**Congratulations!** Your API is now live on Railway! 🎉

Next steps:
1. Share the API URL with your team
2. Integrate with your frontend
3. Monitor performance in Railway Dashboard
4. Scale as needed
