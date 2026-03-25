FROM node:20-alpine

WORKDIR /app

# Otimizando cache do Docker
COPY package*.json ./
RUN npm install

# Copia todo o código React
COPY . .

EXPOSE 5173

# Starta o server apontando pra 0.0.0.0
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
