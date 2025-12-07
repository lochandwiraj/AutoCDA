# Hybrid Deployment Solution

## Problem
Vercel has a 250 MB limit for serverless functions, and SKiDL + dependencies exceed this.

## Solution: Split Deployment

### Frontend on Vercel (Free)
### Backend on Railway/Render (Free tier available)

---

## Option 1: Railway (Recommended)

### Deploy Backend to Railway:

1. **Go to:** https://railway.app/
2. **Sign up** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Select:** `lochandwiraj/AutoCDA`
5. **Add Environment Variable:**
   - `OPENROUTER_API_KEY` = your key
6. **Settings:**
   - Root Directory: `/`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT backend.api:app`
7. **Deploy!**

Railway will give you a URL like: `https://autocda-production.up.railway.app`

### Deploy Frontend to Vercel:

1. Update `client/.env.production`:
   ```
   VITE_API_URL=https://your-railway-url.railway.app
   ```

2. Push to GitHub:
   ```bash
   git add .
   git commit -m "Update API URL for Railway backend"
   git push
   ```

3. Deploy on Vercel (frontend only - will work now!)

---

## Option 2: Render

### Deploy Backend to Render:

1. **Go to:** https://render.com/
2. **Sign up** with GitHub
3. **New** → **Web Service**
4. **Connect:** `lochandwiraj/AutoCDA`
5. **Settings:**
   - Name: `autocda-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT backend.api:app`
6. **Environment Variables:**
   - `OPENROUTER_API_KEY` = your key
7. **Create Web Service**

Render will give you: `https://autocda-backend.onrender.com`

### Deploy Frontend to Vercel:

Same as above, update the API URL to your Render URL.

---

## Option 3: Keep Backend Local (Simplest for Now)

### Deploy only Frontend to Vercel:

The current `vercel.json` is configured for frontend-only.

1. **Push changes:**
   ```bash
   git add .
   git commit -m "Frontend-only Vercel deployment"
   git push
   ```

2. **Deploy on Vercel** - will work now!

3. **Run backend locally:**
   ```bash
   set OPENROUTER_API_KEY=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
   python backend/api.py
   ```

4. **Use ngrok to expose local backend:**
   ```bash
   ngrok http 5000
   ```
   
   Update `client/.env.production` with ngrok URL.

---

## Comparison

| Option | Frontend | Backend | Cost | Complexity |
|--------|----------|---------|------|------------|
| Railway | Vercel | Railway | Free | ⭐⭐ Medium |
| Render | Vercel | Render | Free | ⭐⭐ Medium |
| Local + ngrok | Vercel | Local | Free | ⭐ Easy |
| Self-hosted | VPS | VPS | $5/mo | ⭐⭐⭐ Hard |

---

## My Recommendation

**Use Railway for backend + Vercel for frontend**

Why:
- ✅ Both have free tiers
- ✅ Railway handles Python dependencies well
- ✅ Vercel is perfect for React
- ✅ Professional setup
- ✅ Auto-deploys on git push
- ✅ HTTPS included

---

## Quick Start with Railway

```bash
# 1. Update API URL
echo "VITE_API_URL=https://your-app.up.railway.app" > client/.env.production

# 2. Create railway.json
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn -w 4 -b 0.0.0.0:$PORT backend.api:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

# 3. Push to GitHub
git add .
git commit -m "Add Railway configuration"
git push

# 4. Deploy on Railway (follow steps above)
# 5. Deploy on Vercel (frontend only)
```

Done! 🚀
