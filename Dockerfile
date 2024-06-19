FROM node:20-slim

# Create app directory and set the node user as owner
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app

# Set working directory
WORKDIR /home/node/app

# Switch to 'node' user
USER node

# Copy package.json and package-lock.json (if available)
COPY --chown=node:node package*.json ./

# Install app dependencies
RUN npm install

# Copy the rest of the app source code
COPY --chown=node:node proxy.mjs .

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the app
CMD [ "node", "proxy.mjs" ]
