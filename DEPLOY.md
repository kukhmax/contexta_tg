# 🚀 Deployment Guide for Contexta

## Prerequisites
- A VPS (Ubuntu 22.04 recommended)
- Domain name pointed to your VPS IP
- Docker & Docker Compose installed

## 1. Clone & Setup
```bash
# Clone repository
git clone https://github.com/kukhmax/contexta_tg.git
cd contexta_tg

# Create production env file
cp .env .env.prod
nano .env.prod
# Update variables:
# - DOMAIN=yourdomain.com
# - DATABASE_URL=postgresql://user:pass@db:5432/contexta
# - REDIS_URL=redis://redis:6379/0
# - BOT_TOKEN=...
# - GROQ_API_KEY=...
```

## 2. Run in Production
```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build
```

## 3. SSL (HTTPS)
For Telegram Web Apps, **HTTPS is required**.
The easiest way is to use `certbot` on the host machine or use a reverse proxy like `Traefik`.

### Option A: Cloudflare (Easiest)
1. Point domain to Cloudflare.
2. Enable "Full" encryption in Cloudflare.
3. Your server listens on port 80 (handled by our Nginx), Cloudflare handles SSL.

### Option B: Certbot on Host
```bash
sudo apt install nginx certbot python3-certbot-nginx
# Configure host Nginx to proxy to localhost:80 (Docker)
# Run certbot --nginx
```

## 4. Updates
To update the app:
```bash
git pull
docker-compose -f docker-compose.prod.yml up -d --build
```
