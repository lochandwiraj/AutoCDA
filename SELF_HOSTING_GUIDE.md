# Self-Hosting Guide - No Third Party Required

## Quick Local Setup (Development)

**Already working!** Just run:

```bash
# Terminal 1 - Backend
set OPENROUTER_API_KEY=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
python backend/api.py

# Terminal 2 - Frontend  
cd client
npm run dev
```

Visit: http://localhost:5173

---

## Production Self-Hosting Options

### Option 1: Linux Server (Ubuntu/Debian)

**Requirements:**
- Ubuntu 20.04+ or Debian 11+
- Root/sudo access
- Public IP address

**One-Command Deploy:**
```bash
chmod +x deploy-self-hosted.sh
sudo ./deploy-self-hosted.sh
```

**What it does:**
- Installs Python, Node.js, Nginx
- Sets up backend as systemd service
- Builds and serves React frontend
- Configures Nginx as reverse proxy
- Auto-starts on server reboot

**Access:** http://your-server-ip

---

### Option 2: Windows Server

**Requirements:**
- Windows Server 2016+
- Administrator access
- IIS (optional, for production)

**Deploy:**
```bash
# Run as Administrator
deploy-windows-server.bat
```

**Manual Start:**
```bash
start-backend.bat
```

**Access:** http://localhost

---

### Option 3: Docker (Any OS)

**Create Dockerfile:**
```dockerfile
# Backend
FROM python:3.14-slim as backend
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend ./backend
COPY prompts ./prompts

# Frontend
FROM node:18 as frontend
WORKDIR /app
COPY client/package*.json ./
RUN npm install
COPY client .
RUN npm run build

# Final image
FROM python:3.14-slim
WORKDIR /app
COPY --from=backend /app /app
COPY --from=frontend /app/dist /app/client/dist
RUN pip install gunicorn
ENV OPENROUTER_API_KEY=""
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.api:app"]
```

**Run:**
```bash
docker build -t autocda .
docker run -p 80:5000 -e OPENROUTER_API_KEY=your-key autocda
```

---

### Option 4: Simple Production Build

**Build once, run anywhere:**

```bash
# 1. Build frontend
cd client
npm run build
cd ..

# 2. Serve with Python
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:80 backend.api:app
```

**Serve static files:**
Configure your backend to serve `client/dist` folder.

---

## Comparison

| Method | Difficulty | Best For |
|--------|-----------|----------|
| Local Dev | ⭐ Easy | Testing, development |
| Linux Server | ⭐⭐ Medium | Production, VPS hosting |
| Windows Server | ⭐⭐ Medium | Windows environments |
| Docker | ⭐⭐⭐ Advanced | Containerized deployments |
| Simple Build | ⭐ Easy | Quick production setup |

---

## Cost Comparison

**Self-Hosted:**
- VPS (DigitalOcean, Linode): $5-10/month
- AWS EC2 t2.micro: ~$8/month
- Home server: $0 (electricity only)

**vs Third-Party:**
- Vercel: Free tier available, $20/month Pro
- Heroku: $7/month minimum
- Railway: $5/month minimum

---

## Recommended: Linux VPS Setup

**Best value for self-hosting:**

1. **Get a VPS** ($5/month):
   - DigitalOcean Droplet
   - Linode Nanode
   - Vultr Cloud Compute
   - Hetzner Cloud

2. **Deploy:**
   ```bash
   ssh root@your-server-ip
   git clone https://github.com/lochandwiraj/AutoCDA.git
   cd AutoCDA
   chmod +x deploy-self-hosted.sh
   ./deploy-self-hosted.sh
   ```

3. **Done!** Access at: http://your-server-ip

**Optional - Add Domain:**
```bash
# Point your domain to server IP
# Update Nginx config:
sudo nano /etc/nginx/sites-available/autocda
# Change: server_name _;
# To: server_name yourdomain.com;
sudo systemctl restart nginx

# Add SSL (free):
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Monitoring & Maintenance

**Check backend status:**
```bash
sudo systemctl status autocda-backend
```

**View logs:**
```bash
sudo journalctl -u autocda-backend -f
```

**Restart services:**
```bash
sudo systemctl restart autocda-backend
sudo systemctl restart nginx
```

**Update app:**
```bash
cd /var/www/autocda
git pull
cd client && npm run build && cd ..
sudo systemctl restart autocda-backend
```

---

## Security Tips

1. **Firewall:**
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 22/tcp
   sudo ufw enable
   ```

2. **SSL Certificate:**
   ```bash
   sudo certbot --nginx
   ```

3. **Keep Updated:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

4. **Secure API Key:**
   - Never commit .env to git
   - Use environment variables
   - Rotate keys regularly

---

## Troubleshooting

**Backend won't start:**
```bash
sudo journalctl -u autocda-backend -n 50
```

**Nginx errors:**
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

**Port already in use:**
```bash
sudo lsof -i :5000
sudo kill -9 <PID>
```

**Permission issues:**
```bash
sudo chown -R $USER:$USER /var/www/autocda
```

---

## You're in Control! 🎉

With self-hosting, you have:
- ✅ Full control over your data
- ✅ No vendor lock-in
- ✅ Predictable costs
- ✅ Custom configurations
- ✅ No third-party dependencies

Choose the option that works best for you!
