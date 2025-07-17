# proxy/Dockerfile
FROM nginx:1.27-alpine

# Remove the default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built frontend assets from the builder stage
# The 'frontend' name comes from the service name in docker-compose.yml
COPY --from=frontend /dist /usr/share/nginx/html
