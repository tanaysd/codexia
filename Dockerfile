FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
COPY packages ./packages
RUN npm install
RUN npm run typecheck
CMD ["node", "packages/backend/dist/index.js"]
