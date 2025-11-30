# Security configuration notes

- DEBUG = False for production.
- Cookie security enabled via CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE in production.
- CSP implemented via django-csp middleware (see settings).
- All forms include {% csrf_token %}.
- Views use Django forms and ORM to prevent SQL injection.
- Permissions enforced with @permission_required for sensitive endpoints.
- SECRET_KEY and other secrets stored in env vars.

# Security Enhancements Implemented

## HTTPS & Redirects
- SECURE_SSL_REDIRECT enabled to force HTTPS.
- HSTS configured with SECURE_HSTS_SECONDS, INCLUDE_SUBDOMAINS, and PRELOAD.

## Secure Cookies
- SESSION_COOKIE_SECURE set to True.
- CSRF_COOKIE_SECURE set to True.

## Secure Headers
- X_FRAME_OPTIONS = "DENY" prevents clickjacking.
- SECURE_CONTENT_TYPE_NOSNIFF prevents MIME sniffing.
- SECURE_BROWSER_XSS_FILTER improves protection against basic XSS attacks.

## Deployment Notes
To deploy securely:
1. Install SSL certificates (Let's Encrypt recommended).
2. Configure your web server (Nginx/Apache) to forward HTTPS traffic to Django.
3. Ensure DEBUG is False in production.

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";

    location / {
        proxy_pass http://127.0.0.1:8000;
        include proxy_params;
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}