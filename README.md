# API Proxy Service

A FastAPI-based API proxy service that allows you to make HTTP requests through a centralized service.

## Prerequisites

- Python 3.13 or higher
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd api-proxy
```

2. Create and activate a virtual environment:

For Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

For Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Service

### Development Mode

For Windows:
```bash
uvicorn app:app --reload --port 3000
```

For Linux:
```bash
uvicorn app:app --reload --port 3000
```

The service will be available at `http://localhost:3000`

## Production Deployment

### Windows (Using Windows Service)

1. Install NSSM (Non-Sucking Service Manager):
   - Download from: https://nssm.cc/download
   - Extract and add to system PATH

2. Create a batch file `start_api_proxy.bat`:
```batch
@echo off
cd /d %~dp0
call .venv\Scripts\activate
uvicorn app:app --host 0.0.0.0 --port 3000
```

3. Install as Windows Service:
```bash
nssm install APIPROXY "%~dp0start_api_proxy.bat"
nssm set APIPROXY AppDirectory "%~dp0"
nssm set APIPROXY DisplayName "API Proxy Service"
nssm set APIPROXY Description "API Proxy Service for handling HTTP requests"
nssm set APIPROXY Start SERVICE_AUTO_START
```

4. Start the service:
```bash
nssm start APIPROXY
```

### Linux (Using Systemd)

1. Create a systemd service file `/etc/systemd/system/api-proxy.service`:
```ini
[Unit]
Description=API Proxy Service
After=network.target

[Service]
User=<your-username>
WorkingDirectory=/path/to/api-proxy
Environment="PATH=/path/to/api-proxy/.venv/bin"
ExecStart=/path/to/api-proxy/.venv/bin/uvicorn app:app --host 0.0.0.0 --port 3000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable api-proxy
sudo systemctl start api-proxy
```

3. Check service status:
```bash
sudo systemctl status api-proxy
```

## API Usage

The service exposes a single endpoint:

### POST /call-api

Make HTTP requests through the proxy.

Request body:
```json
{
    "url": "https://api.example.com/v1/resource",
    "method": "GET",
    "body": {"key": "value"},  // Optional
    "headers": {               // Optional
        "Authorization": "Bearer token"
    }
}
```

Response:
```json
{
    "status_code": 200,
    "headers": {},
    "body": "response content"
}
```

## Monitoring and Logs

### Windows
- View service logs: Event Viewer > Windows Logs > Application
- Check service status: `sc query APIPROXY`

### Linux
- View service logs: `journalctl -u api-proxy`
- Check service status: `systemctl status api-proxy`

## Troubleshooting

1. Service won't start:
   - Check if the port is already in use
   - Verify Python and virtual environment paths
   - Check service logs for errors

2. Connection refused:
   - Verify the service is running
   - Check firewall settings
   - Ensure correct port is being used

## Security Considerations

1. Always run the service behind a reverse proxy in production
2. Implement proper authentication and rate limiting
3. Keep dependencies updated
4. Use HTTPS in production environments