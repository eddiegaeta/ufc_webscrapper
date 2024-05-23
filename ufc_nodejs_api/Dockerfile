# Use an official Node.js runtime as a base image
FROM node:14

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install the application dependencies
RUN npm install

# Install nodemon globally
RUN npm install nodemon -g

# Install additional dependencies
RUN npm install express mysql dotenv ejs

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port that the app will run on
EXPOSE 3000

# Define the command to run your application using nodemon
CMD ["npm", "run", "dev"]

##Test webhook