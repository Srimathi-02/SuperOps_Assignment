#!/bin/bash
set -e

# Log everything to a file for debugging
exec > >(tee -a /var/log/startup-script.log) 2>&1
echo "$(date): Starting startup script"

# Wait for network to be ready
echo "$(date): Waiting for network connectivity..."
for i in {1..30}; do
    if ping -c 1 google.com >/dev/null 2>&1; then
        echo "$(date): Network is ready"
        break
    fi
    echo "$(date): Waiting for network... attempt $i"
    sleep 2
done

# Update package list
echo "$(date): Updating package list..."
apt-get update -y

# Install nginx
echo "$(date): Installing nginx..."
apt-get install -y nginx

# Create custom index.html with server identification
echo "$(date): Creating custom index.html..."
HOSTNAME=$(hostname)
INTERNAL_IP=$(hostname -I | awk '{print $1}')

cat > /var/www/html/index.html << HTML
<!DOCTYPE html>
<html>
<head>
    <title>Hello World - Load Balancer Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f0f0f0;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #333; }
        .info { 
            background-color: #e7f3ff; 
            padding: 10px; 
            border-left: 4px solid #2196F3; 
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello World!</h1>
        <div class="info">
            <p><strong>Served by:</strong> $HOSTNAME</p>
            <p><strong>Server IP:</strong> $INTERNAL_IP</p>
            <p><strong>Timestamp:</strong> $(date)</p>
            <p><strong>Port:</strong> ${health_check_port}</p>
        </div>
        <p>This server is running nginx and is part of a load-balanced setup.</p>
    </div>
</body>
</html>
HTML

# Configure nginx to listen on the specified port
if [ "${health_check_port}" != "80" ]; then
    echo "$(date): Configuring nginx to listen on port ${health_check_port}..."
    sed -i "s/listen 80/listen ${health_check_port}/" /etc/nginx/sites-available/default
    sed -i "s/listen \[::\]:80/listen \[::\]:${health_check_port}/" /etc/nginx/sites-available/default
fi

# Enable and start nginx
echo "$(date): Starting and enabling nginx..."
systemctl enable nginx
systemctl restart nginx

# Verify nginx is running
echo "$(date): Verifying nginx status..."
systemctl status nginx --no-pager

# Test if nginx is responding
echo "$(date): Testing nginx response..."
if curl -s http://localhost:${health_check_port}/ > /dev/null; then
    echo "$(date): Nginx is responding correctly on port ${health_check_port}"
else
    echo "$(date): ERROR: Nginx is not responding on port ${health_check_port}"
fi

echo "$(date): Startup script completed successfully"
