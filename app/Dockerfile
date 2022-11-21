# build off of the node:lts-alpine image
FROM node:lts-alpine

# bind your app to the gateway IP
ENV HOST=0.0.0.0

# install simple http server for serving static content
RUN npm install -g http-server

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json .

# install project dependencies
RUN npm install 

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .
# build app
RUN npm run build

# expose port for the server to communicate with the outside world
EXPOSE 8080

# enables live reload funcitonality for the server
ENTRYPOINT [ "npm", "run", "dev" ]
