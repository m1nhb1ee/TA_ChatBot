# ============================================================
# Dockerfile — TA ChatBot Frontend (Nginx)
# ============================================================

FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy frontend files
COPY . /usr/share/nginx/html

# Create healthcheck script
RUN echo '#!/bin/sh\nwget --quiet --tries=1 --spider http://localhost:80/index.html || exit 1' \
    > /tmp/healthcheck.sh && chmod +x /tmp/healthcheck.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD /tmp/healthcheck.sh

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
