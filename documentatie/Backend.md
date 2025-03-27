## Manuel setup

1) dowload github repo

2) terminal in backend

**Vanaf hier in docker**
3)  - nodejs moet geinstalleerd zijn
    - npm moet geinstalleerd zijn

4) installeren dependencies
- npm install

5) runnen server
- npm start


--- 

Voorbeeld door chatgpt

# Use an official Node.js runtime as a base image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of your application code
COPY . .

# Expose the port the app runs on
EXPOSE 4000

# Start the application
CMD ["npm", "start"]

---