# Quick Setup Guide

This guide will get you up and running in 10 minutes.

## What You Have

✅ **Complete Django API** - All files created  
✅ **YOLOv8 Integration** - Uses your `best.pt` model  
✅ **3 API Endpoints** - Inference, history, details  
✅ **Docker Ready** - Dockerfile for Railway  
✅ **Production Configured** - Gunicorn + settings  

## 5-Minute Local Setup

### 1. Install Dependencies (2 min)
```bash
pip install -r requirements.txt
```

### 2. Setup Database (1 min)
```bash
python manage.py migrate
```

### 3. Start Server (1 min)
```bash
python manage.py runserver
```

✅ API now running at: `http://localhost:8000/api/`

## Test It (2 minutes)

### Health Check
```bash
python test_api.py --health
```

### Test with Image
```bash
python test_api.py --image your-image.jpg
```

### cURL Test
```bash
curl -X POST http://localhost:8000/api/inference/ \
  -F "image=@your-image.jpg" \
  -F "confidence=0.5"
```

## Deploy to Railway (5 minutes)

### 1. Push to GitHub
```bash
git add .
git commit -m "Add YOLOv8 API"
git push origin main
```

### 2. Connect to Railway
- Go to https://railway.app/dashboard
- Click "New Project"
- Select "Deploy from GitHub"
- Select your repository
- Click "Deploy Now"

### 3. Add Environment Variables
In Railway Dashboard → Variables, add:
- `SECRET_KEY=` (generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG=False`
- `ALLOWED_HOSTS=your-app.railway.app`

### 4. Wait for Deploy
Watch the build logs. When green ✅, you're live!

### 5. Test Live API
```bash
curl https://your-app.railway.app/api/health/
```

## API Endpoints

### POST /api/inference/
Run inference on image.

```bash
curl -X POST http://localhost:8000/api/inference/ \
  -F "image=@image.jpg" \
  -F "confidence=0.5"
```

**Response:**
- `detections` - Array of detected objects
- `inference_time` - How long inference took
- `image_url` - URL to uploaded image
- `result_image_url` - URL to annotated result image

### GET /api/history/
Get inference history.

```bash
curl http://localhost:8000/api/history/?limit=10
```

### GET /api/inference/{id}/
Get specific inference.

```bash
curl http://localhost:8000/api/inference/1/
```

## File Structure

```
.
├── best.pt                    # Your YOLOv8 model
├── manage.py                  # Django CLI
├── requirements.txt           # Dependencies
├── Dockerfile                 # Docker image
├── config/
│   ├── settings.py           # Django config
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI app
├── apps/
│   └── ml_inference/         # ML API
│       ├── views.py          # API endpoints
│       ├── models.py         # Database models
│       └── inference_utils.py # Model loading
├── media/                    # Uploaded images
└── logs/                     # Application logs
```

## Configuration

Default settings work out of the box for local development.

For production (Railway), set these environment variables:

| Variable | Required | Example |
|----------|----------|---------|
| `SECRET_KEY` | Yes | (generated) |
| `DEBUG` | Yes | `False` |
| `ALLOWED_HOSTS` | Yes | `your-app.railway.app` |
| `DATABASE_URL` | No | (optional PostgreSQL) |
| `CORS_ALLOWED_ORIGINS` | No | `your-frontend.com` |
| `ML_MODEL_PATH` | No | `./best.pt` (optional custom model) |

**Note:** The API automatically downloads YOLOv8m model on first use. No need to commit large model files!

## Common Tasks

### Create Admin User
```bash
python manage.py createsuperuser
# Then access http://localhost:8000/admin/
```

### View Logs (Local)
```bash
tail -f logs/django.log
```

### Run Migrations
```bash
python manage.py migrate
```

### Test All Endpoints
```bash
python test_api.py --all --image test.jpg
```

## Troubleshooting

### "Model not found"
✅ Ensure `best.pt` is in the root directory

### "Port already in use"
Use different port:
```bash
python manage.py runserver 8001
```

### Import errors
Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### CORS errors
Update `CORS_ALLOWED_ORIGINS` in settings or `.env`

## Next Steps

1. ✅ **Setup locally** - Run `python manage.py runserver`
2. ✅ **Test API** - Run `python test_api.py --health`
3. ✅ **Deploy to Railway** - Follow Railway deployment steps above
4. ✅ **Share API** - Use your Railway URL with your frontend
5. ✅ **Monitor** - Watch logs in Railway Dashboard

## More Information

- **Full README:** See [README.md](README.md)
- **Railway Guide:** See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)
- **API Docs:** Check endpoint responses above

## You're All Set! 🚀

Your YOLOv8 API is ready. Pick one:

**Quick Test:**
```bash
python test_api.py --health
```

**Deploy Now:**
```bash
git push origin main
# Then connect to Railway
```

**Full Setup:**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Any questions? Check the [README.md](README.md) or [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)!
