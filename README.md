# YOLOv8 ML Inference API

Complete REST API for running YOLOv8 waste detection on your **best.pt** model. Ready to deploy on Railway.

## ✨ Features

✅ **ML Inference** - POST image and get detections  
✅ **Bounding Boxes** - Annotated images with predictions  
✅ **History Tracking** - Database records of all inferences  
✅ **Admin Dashboard** - Manage inferences via Django admin  
✅ **Production Ready** - Dockerfile + Gunicorn configured  
✅ **Railway Optimized** - Deploy in minutes  

## 🚀 Quick Start

### 1. Local Setup (5 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver 0.0.0.0:8000
```

API running at: `http://localhost:8000/api/`

### 2. Test the API

```bash
# Health check
python test_api.py --health

# Run inference on image
python test_api.py --image path/to/your/image.jpg

# Test all endpoints
python test_api.py --all --image test.jpg
```

Or use cURL:
```bash
# Inference
curl -X POST http://localhost:8000/api/inference/ \
  -F "image=@image.jpg" \
  -F "confidence=0.5"

# History
curl http://localhost:8000/api/history/?limit=10
```

### 3. Deploy to Railway (5 minutes)

```bash
# 1. Push to GitHub
git add .
git commit -m "Add YOLOv8 API"
git push origin main

# 2. Go to Railway Dashboard
# 3. Create new project → Connect GitHub repo
# 4. Add environment variables from .env.example
# 5. Railway auto-deploys!
```

Verify deployment:
```bash
curl https://your-app.railway.app/api/health/
```

## 📡 API Endpoints

### POST /api/inference/
Run inference on an image.

**Request:**
```bash
curl -X POST http://localhost:8000/api/inference/ \
  -F "image=@image.jpg" \
  -F "confidence=0.5" \
  -F "save_result=true"
```

**Response:**
```json
{
  "status": "success",
  "request_id": 1,
  "detections": [
    {
      "class": 0,
      "class_name": "waste",
      "confidence": 0.95,
      "bbox": {"x1": 100, "y1": 100, "x2": 200, "y2": 200}
    }
  ],
  "image_url": "http://...",
  "result_image_url": "http://...",
  "inference_time": 0.234,
  "message": "Found 1 objects"
}
```

### GET /api/history/
Get inference history.

```bash
curl http://localhost:8000/api/history/?limit=10
```

**Response:**
```json
{
  "status": "success",
  "count": 2,
  "results": [...]
}
```

### GET /api/inference/{id}/
Get specific inference details.

```bash
curl http://localhost:8000/api/inference/1/
```

### GET /api/health/
Health check endpoint.

```bash
curl http://localhost:8000/api/health/
```

## 🔧 Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Update settings:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,your-domain.com
DATABASE_URL=postgresql://user:pass@host:5432/db
ML_MODEL_PATH=./best.pt
```

## 📦 Model File

The API **automatically downloads** the YOLOv8m model on first use.

**Models used:**
- **Default:** YOLOv8m (medium) - Balanced speed and accuracy (~49 MB)
- **Custom:** Place `best.pt` in root for custom trained models

To use a different pre-trained model, set:
```bash
# Use nano model (fastest, smallest)
python manage_model.py --download yolov8n

# Or use via environment
export ML_MODEL_PATH=./custom_best.pt
```

**Note:** Model file is NOT stored in git due to Railway's 4GB limit.

## 🐳 Docker & Railway

### Build Locally
```bash
docker build -t ml-api .
docker run -p 8000:8000 ml-api
```

### Deploy to Railway

1. **Connect GitHub repo** to Railway
2. **Add environment variables:**
   - `SECRET_KEY` - Generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app.railway.app`
3. **Add PostgreSQL service** (optional, defaults to SQLite)
4. **Deploy** - Railway auto-builds and deploys

## 📊 Database

Default: **SQLite** (db.sqlite3)

For production on Railway, set `DATABASE_URL` to use **PostgreSQL**:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

## 🔑 Admin Panel

Access Django admin at: `http://localhost:8000/admin/`

Create superuser:
```bash
python manage.py createsuperuser
```

View all inference requests, filter by date/confidence, and manage data.

## 📚 Project Structure

```
.
├── manage.py                 # Django CLI
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container image
├── Procfile                  # Railway startup
├── railway.json              # Railway config
├── best.pt                   # Your YOLOv8 model
├── config/
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI app
│   └── asgi.py              # ASGI app
├── apps/
│   ├── ml_inference/        # ML API app
│   │   ├── models.py        # InferenceRequest model
│   │   ├── views.py         # API endpoints
│   │   ├── inference_utils.py # Model utils
│   │   └── urls.py
│   └── accounts/            # Auth app
├── media/                   # User uploads
│   ├── uploads/             # Input images
│   └── results/             # Output images
└── logs/                    # Application logs
```

## 🛠️ Development

### Create Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### Run Tests
```bash
python test_api.py --all --image test.jpg
```

## 📝 API Examples

### Python
```python
import requests

with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/inference/',
        files={'image': f},
        data={'confidence': 0.5}
    )
    result = response.json()
    print(f"Found {len(result['detections'])} objects")
```

### JavaScript
```javascript
const formData = new FormData();
formData.append('image', imageFile);
formData.append('confidence', 0.5);

const response = await fetch('http://localhost:8000/api/inference/', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(`Found ${result.detections.length} objects`);
```

### cURL
```bash
curl -X POST http://localhost:8000/api/inference/ \
  -F "image=@image.jpg" \
  -F "confidence=0.5"
```

## ⚙️ Performance Tips

1. **Model Caching** - Model loaded once, then cached in memory
2. **GPU Support** - Works on Railway GPU instances
3. **Smaller Images** - Faster inference with smaller images
4. **Confidence Threshold** - Higher values = fewer detections = faster

## 🐛 Troubleshooting

### Model Not Found
```
FileNotFoundError: Model not found at ./best.pt
```
**Solution:** Ensure `best.pt` is in the root directory.

### CORS Errors
**Solution:** Update `CORS_ALLOWED_ORIGINS` in `.env`

### Out of Memory
**Solution:** Use Railway GPU instance or process smaller images.

### Slow Inference
**Solution:** First request loads model (normal). Subsequent requests are faster.

## 📞 Support

- **Django Docs:** https://docs.djangoproject.com/
- **DRF Docs:** https://www.django-rest-framework.org/
- **YOLOv8 Docs:** https://docs.ultralytics.com/
- **Railway Docs:** https://docs.railway.app/

## 📄 License

MIT License - feel free to use and modify.

---

**Ready to deploy?** Follow the Quick Start above! 🚀
