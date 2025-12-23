# Base image
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy the rest of the code
COPY . .

# Expose dev port
EXPOSE 3000

# Run Next.js in development mode
CMD ["npm", "run", "dev"]
