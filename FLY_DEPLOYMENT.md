# Fly.io Deployment Guide

Fly.io is a modern hosting platform perfect for Docker applications. Free tier includes:
- ✅ 3 shared-cpu VMs (great for our API)
- ✅ 100 GB outbound data transfer per month
- ✅ Automatic HTTPS/SSL
- ✅ Global deployment
- ✅ Unlimited storage

## Prerequisites

1. **Fly.io Account:** https://fly.io/
2. **Flyctl CLI:** Download from https://fly.io/docs/hands-on/install-flyctl/
3. **GitHub Repository:** Already set up (rehanafzal779/lab4)

## Step 1: Install Flyctl

**Windows:**
```bash
choco install flyctl
# or download from https://fly.io/docs/hands-on/install-flyctl/
```

**Verify installation:**
```bash
flyctl version
```

## Step 2: Login to Fly.io

```bash
flyctl auth login
```

This opens your browser to authenticate. Complete the login process.

## Step 3: Create Fly.io App

```bash
cd "C:\Users\User\Desktop\New folder"
flyctl launch
```

When prompted:
- **App name:** neat-now-api (or choose your own)
- **Region:** Choose closest to you (e.g., sfo, lhr, syd)
- **PostgreSQL:** No (we'll use SQLite initially)
- **Upstash Redis:** No
- **Deploy now:** No (we'll configure first)

This creates/updates `fly.toml` with your app configuration.

## Step 4: Set Environment Variables

```bash
# Create secure SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Set environment variables in Fly.io:

```bash
flyctl secrets set SECRET_KEY="your-generated-key"
flyctl secrets set DEBUG="False"
flyctl secrets set ALLOWED_HOSTS="neat-now-api.fly.dev"
flyctl secrets set CORS_ALLOWED_ORIGINS="https://your-frontend.com"
```

Or set them in the Fly.io dashboard:
1. Go to https://fly.io/dashboard
2. Select your app
3. Click "Secrets" tab
4. Add each secret

## Step 5: Configure fly.toml (Optional)

The included `fly.toml` already has:
- ✅ Docker build configuration
- ✅ Health check endpoint
- ✅ Port 8000 exposed
- ✅ 512MB memory allocated
- ✅ Auto-scaling configured

To customize:
```toml
app = "neat-now-api"  # Change app name
primary_region = "sfo"  # Change region (lhr, syd, ams, etc.)

[[vm]]
  memory = "512mb"  # Increase if needed
  cpus = 1
```

## Step 6: Deploy!

```bash
flyctl deploy
```

Watch the deployment logs in real-time. The build will:
1. ✅ Build Docker image
2. ✅ Download YOLOv8 model (~50MB)
3. ✅ Run migrations
4. ✅ Start Gunicorn server

Expected output:
```
--> Pushing image to fly
--> Waiting for remote builder...
Consolidating cgroup2 controllers
Checking cgroup setup...
...
==> Creating release
Release v1 created and inprogress
...
```

## Step 7: Check Deployment Status

```bash
# View logs
flyctl logs

# Check app status
flyctl status

# Monitor in browser
flyctl open
```

## Step 8: Test Your API

**Health check:**
```bash
curl https://neat-now-api.fly.dev/api/health/
```

Expected response:
```json
{"status": "ok", "message": "API is running"}
```

**Run inference:**
```bash
curl -X POST https://neat-now-api.fly.dev/api/inference/ \
  -F "image=@image.jpg" \
  -F "confidence=0.5"
```

## Step 9: View Your App

```bash
# Open app in browser
flyctl open

# Open admin panel
flyctl open /admin
```

## Useful Commands

```bash
# View logs (real-time)
flyctl logs -f

# SSH into app
flyctl ssh console

# Scale to 2 instances
flyctl scale count 2

# View metrics
flyctl status

# Update environment variable
flyctl secrets set MY_VAR="new value"

# View all secrets
flyctl secrets list

# Delete app
flyctl destroy
```

## Regions Available

Choose the one closest to you or your users:

| Code | Location |
|------|----------|
| sfo | San Francisco |
| sea | Seattle |
| lax | Los Angeles |
| den | Denver |
| dfw | Dallas |
| ord | Chicago |
| jfk | New York |
| mia | Miami |
| bos | Boston |
| lhr | London |
| ams | Amsterdam |
| fra | Frankfurt |
| syd | Sydney |
| nrt | Tokyo |
| sin | Singapore |

Change region in `fly.toml`:
```toml
primary_region = "lhr"  # London
```

## Using a Custom Domain

1. Add domain in Fly.io dashboard
2. Point DNS to Fly.io nameservers
3. SSL certificate automatically created

```bash
# Add custom domain
flyctl certs add yourdomain.com

# View certificates
flyctl certs list
```

## Database (Production)

To add PostgreSQL database:

```bash
# Create PostgreSQL instance
flyctl postgres create

# Link to your app
flyctl postgres attach
```

This automatically sets `DATABASE_URL` environment variable.

## Troubleshooting

### App Won't Start
```bash
# Check logs
flyctl logs

# Look for errors in Python/Django output
```

### Model Download Takes Too Long
- First deployment is slower as it downloads YOLOv8m (~50MB)
- Subsequent deployments use cached layer
- Model is cached on the VM, no re-download needed

### Out of Memory
```bash
# Increase memory in fly.toml
[[vm]]
  memory = "1gb"

# Then redeploy
flyctl deploy
```

### Need to Clear Cache
```bash
# Restart app
flyctl restart

# Deploy with no cache
flyctl deploy --no-cache
```

## Monitoring

View in real-time dashboard:
```bash
# Open dashboard
flyctl dashboard
```

Monitor metrics:
- Request count
- Error rate
- Response time
- CPU/Memory usage

## Cost Estimate

**Free tier includes:**
- 3 shared-cpu-1x 256MB VMs = Enough for 1 app!
- 100GB outbound data/month
- Unlimited storage
- Free SSL/HTTPS

**If you need more:**
- Additional VM: $5/month
- Additional storage: Minimal cost

## Next Steps

1. ✅ Install Flyctl: `choco install flyctl`
2. ✅ Login: `flyctl auth login`
3. ✅ Deploy: `flyctl deploy`
4. ✅ Test: `curl https://your-app.fly.dev/api/health/`

---

**Ready to deploy?** Run `flyctl deploy` now! 🚀
