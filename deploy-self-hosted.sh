#!/bin/bash
# Self-Hosted Deployment Script for AutoCDA
# Run this on your own server (Ubuntu/Debian)

echo "🚀 AutoCDA Self-Hosted Deployment"
echo "=================================="

# Update system
echo "📦 Updating system..."
sudo apt update
sudo apt upgrade -y

# Install Python
echo "🐍 Installing Python..."
sudo apt install -y python3 python3-pip python3-venv

# Install Node.js
echo "📦 Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Nginx
echo "🌐 Installing Nginx..."
sudo apt install -y nginx

# Clone repository (if not already cloned)
if [ ! -d "/var/www/autocda" ]; then
    echo "📥 Cloning repository..."
    sudo mkdir -p /var/www
    cd /var/www
    sudo git clone https://github.com/lochandwiraj/AutoCDA.git autocda
    sudo chown -R $USER:$USER /var/www/autocda
fi

cd /var/www/autocda

# Setup Python backend
echo "🔧 Setting up Python backend..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup environment variables
echo "🔐 Setting up environment variables..."
read -p "Enter your OpenRouter API Key: " api_key
echo "OPENROUTER_API_KEY=$api_key" > .env

# Build React frontend
echo "⚛️ Building React frontend..."
cd client
npm install
npm run build
cd ..

# Setup Gunicorn service
echo "🔧 Setting up Gunicorn service..."
sudo tee /etc/systemd/system/autocda-backend.service > /dev/null <<EOF
[Unit]
Description=AutoCDA Backend API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/var/www/autocda
Environment="PATH=/var/www/autocda/venv/bin"
EnvironmentFile=/var/www/autocda/.env
ExecStart=/var/www/autocda/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 backend.api:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Setup Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/autocda > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    # Serve React frontend
    location / {
        root /var/www/autocda/client/dist;
        try_files \$uri \$uri/ /index.html;
    }

    # Proxy API requests to backend
    location /api/ {
        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/autocda /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable autocda-backend
sudo systemctl start autocda-backend
sudo systemctl restart nginx

# Get server IP
SERVER_IP=$(curl -s ifconfig.me)

echo ""
echo "✅ Deployment Complete!"
echo "======================="
echo "Your app is now running at:"
echo "http://$SERVER_IP"
echo ""
echo "Useful commands:"
echo "  Check backend status: sudo systemctl status autocda-backend"
echo "  View backend logs: sudo journalctl -u autocda-backend -f"
echo "  Restart backend: sudo systemctl restart autocda-backend"
echo "  Check Nginx status: sudo systemctl status nginx"
echo ""
