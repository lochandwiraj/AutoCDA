# Vercel Deployment Guide

## Prerequisites

1. Vercel account ([sign up](https://vercel.com/signup))
2. OpenRouter API key ([get one](https://openrouter.ai/))

## Deployment Steps

### 1. Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

### 2. Deploy via Vercel Dashboard (Recommended)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your Git repository
3. Configure project:
   - **Framework Preset:** Other
   - **Root Directory:** ./
   - **Build Command:** (leave empty, handled by vercel.json)
   - **Output Directory:** (leave empty, handled by vercel.json)

4. Add Environment Variable:
   - Key: `OPENROUTER_API_KEY`
   - Value: Your OpenRouter API key
   - Scope: Production, Preview, Development

5. Click **Deploy**

### 3. Deploy via CLI (Alternative)

```bash
# Login to Vercel
vercel login

# Deploy
vercel

# Add environment variable
vercel env add OPENROUTER_API_KEY

# Deploy to production
vercel --prod
```

## Configuration Files

### vercel.json
- Configures both frontend (React) and backend (Python Flask)
- Routes `/api/*` to backend
- Routes everything else to frontend

### client/.env.production
- Sets `VITE_API_URL=/api` for production
- Automatically used during build

### client/.env.development
- Sets `VITE_API_URL=http://localhost:5000` for local dev
- Used when running `npm run dev`

## Post-Deployment

1. Visit your deployment URL
2. Test the health endpoint: `https://your-app.vercel.app/api/health`
3. Try generating a circuit

## Troubleshooting

### Backend not responding
- Check environment variable is set: `OPENROUTER_API_KEY`
- Check Vercel function logs in dashboard

### Frontend shows "Backend Offline"
- Verify `/api/health` endpoint works
- Check browser console for CORS errors

### Build fails
- Ensure all dependencies are in `requirements.txt` and `package.json`
- Check build logs in Vercel dashboard

## Local Testing

Test production build locally:

```bash
# Build frontend
cd client
npm run build
npm run preview

# Start backend
cd ..
python backend/api.py
```

## Important Notes

- Vercel has a 10-second timeout for serverless functions
- Large circuit generations might timeout (consider upgrading plan)
- Output files are stored in `/tmp` on Vercel (ephemeral)
- For persistent storage, consider using Vercel Blob or S3

## Monitoring

- View logs: Vercel Dashboard → Your Project → Logs
- View analytics: Vercel Dashboard → Your Project → Analytics
- Set up alerts for errors and downtime
