# Frontend/Dockerfile (Development)
FROM node:20-alpine
WORKDIR /app

ENV NODE_ENV=development

# Install dependencies
COPY package.json bun.lockb* ./
RUN bun install

# Copy source code
COPY . .

# Expose Vite port and run dev server
EXPOSE 5173
CMD ["bun", "run", "dev", "--host"]
