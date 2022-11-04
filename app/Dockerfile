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
# build app for production with minification
RUN npm run build
#RUN npm run dev
#CMD ["npm", "run", "serve"]

EXPOSE 8080
#CMD [ "http-server", "dist" ]
ENTRYPOINT [ "npm", "run", "dev" ]
