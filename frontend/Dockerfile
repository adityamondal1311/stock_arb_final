FROM node:18-alpine

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install

COPY . .

RUN adduser -D appuser && chown -R appuser /app
USER appuser

EXPOSE 5173
CMD ["npm", "run", "dev"]
