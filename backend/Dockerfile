# ---- Node.js Backend (Express + MongoDB) ----
FROM node:20-alpine

WORKDIR /app

# Install dependencies first (better layer caching)
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# Copy application code
COPY server.js .
COPY routes/ ./routes/
COPY models/ ./models/
COPY middleware/ ./middleware/

# Expose the backend port
EXPOSE 5000

ENV PORT=5000

CMD ["node", "server.js"]
