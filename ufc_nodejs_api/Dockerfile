# Use an official Node.js runtime as a base image for building the React app
FROM node:18 AS build

# Set the working directory in the container for the React build
WORKDIR /usr/src/app/client

# Copy package.json and package-lock.json of the React app to the working directory
COPY client/package*.json ./

# Install React application dependencies
RUN npm install

# Copy the rest of the React application code to the working directory
COPY client/ ./

# Build the React application
RUN npm run build

# Use a new stage for the Node.js API to avoid conflicts with the React build
FROM node:18

# Set the working directory in the container for the Node.js API
WORKDIR /usr/src/app

# Copy package.json and package-lock.json of the API to the working directory
COPY package*.json ./

# Install application dependencies and nodemon globally in one step to reduce layers
RUN npm install && npm install -g nodemon && npm install moment && npm install moment-timezone

# Copy the rest of the application code to the working directory
COPY . .

# Copy the React build from the previous stage
COPY --from=build /usr/src/app/client/build ./client/build

# Expose the port that the app will run on
EXPOSE 3000

# Define the command to run your application using nodemon
CMD ["npm", "run", "dev"]