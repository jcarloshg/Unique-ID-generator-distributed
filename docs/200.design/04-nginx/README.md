# Phase 204 — Nginx Configuration

## Overview
Design the nginx load balancing configuration for distributing requests across generator instances.

## Objectives
- Configure upstream block with 3 generators
- Set up health checks
- Define timeout values
- Configure error handling

## Deliverables

### Core Documents
- `nginx.conf` — Main nginx configuration
- `upstream.conf` — Upstream block configuration
- `health-check-design.md` — Health check strategy
- `timeout-settings.md` — Timeout budget design

## Configuration

```nginx
upstream generators {
    least_conn;
    
    server generator-1:5001 check;
    server generator-2:5002 check;
    server generator-3:5003 check;
}

server {
    location / {
        proxy_pass http://generators;
        proxy_connect_timeout 5s;
        proxy_read_timeout 10s;
    }
    
    location /health {
        proxy_pass http://generators;
        health_check;
    }
}
```

## Status
- [ ] Initiated
- [ ] In progress
- [ ] Complete
