# Vercel Deployment Checklist ✅

## Pre-Deployment

- [x] **vercel.json** - Configured for both frontend and backend
- [x] **Environment Variables** - Using `VITE_API_URL` for dynamic API endpoint
- [x] **client/.env.production** - Sets API URL to `/api` for production
- [x] **client/.env.development** - Sets API URL to `localhost:5000` for dev
- [x] **package.json** - Added `vercel-build` script
- [x] **requirements.txt** - All Python dependencies listed
- [x] **CORS** - Flask-CORS enabled in backend/api.py
- [x] **.gitignore** - Excludes .env files and build artifacts

## Required Actions Before Deploy

### 1. Get OpenRouter API Key
- Sign up at https://openrouter.ai/
- Copy your API key

### 2. Push to Git
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push
```

### 3. Deploy on Vercel
- Go to https://vercel.com/new
- Import your repository
- Add environment variable: `OPENROUTER_API_KEY`
- Click Deploy

## Post-Deployment Testing

### Test Backend
```bash
curl https://your-app.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Test Frontend
- Visit: `https://your-app.vercel.app`
- Should see landing page with animations
- Click "Get Started"
- Try generating a circuit

### Test Full Flow
1. Enter: "Design a low-pass RC filter with 1kHz cutoff"
2. Click "Generate Circuit"
3. Wait ~5-10 seconds
4. Should see explanation with calculations
5. Download should work

## Known Limitations on Vercel

1. **10-second timeout** - Complex circuits might timeout
2. **Ephemeral storage** - Files in `/tmp` are deleted after response
3. **Cold starts** - First request might be slow (~2-3 seconds)
4. **No persistent file storage** - Downloads work but files don't persist

## Recommended Vercel Settings

- **Framework:** Other
- **Build Command:** (handled by vercel.json)
- **Output Directory:** (handled by vercel.json)
- **Install Command:** (handled by vercel.json)
- **Node Version:** 18.x or higher
- **Python Version:** 3.9 (Vercel default)

## Environment Variables to Set

| Variable | Value | Required |
|----------|-------|----------|
| `OPENROUTER_API_KEY` | Your API key | ✅ Yes |

## Files Modified for Vercel

1. `vercel.json` - Deployment configuration
2. `client/src/App.jsx` - Dynamic API URL
3. `client/.env.production` - Production API endpoint
4. `client/.env.development` - Development API endpoint
5. `client/package.json` - Added vercel-build script

## Ready to Deploy! 🚀

Everything is configured. Just:
1. Push to Git
2. Import to Vercel
3. Add API key
4. Deploy!
