# Dockerfile References: https://docs.docker.com/engine/reference/builder/

# Start from python:3.8-alpine base image
#FROM python:3.10-alpine
FROM python:3.10
#FROM selenium/node-chrome:dev
#FROM python:3.7.2-alpine3.8
#FROM nickgryg/alpine-pandas:3.9.12 as base



# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable


# RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_73.0.3683.68_amd64.deb \
#   && apt install -y /tmp/chrome.deb \
#   && rm /tmp/chrome.deb

# ARG CHROME_VERSION="65.0.3325.181-0ubuntu1"
# RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
#   && apt install -y /tmp/chrome.deb \
#   && rm /tmp/chrome.deb


# Installing Unzip
RUN apt-get install -yqq unzip

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` \
    curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE \
    `/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99



# RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" > /etc/apk/repositories && \
#     echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

# The latest alpine images don't have some tools like (`git` and `bash`).
# Adding git, bash and openssh to the image
# RUN apk update && apk upgrade && \
#     apk add --no-cache bash git openssh libstdc++ chromium chromium-chromedriver

# ENV CHROME_BIN=/usr/bin/chromium-browser \
#     CHROME_PATH=/usr/lib/chromium/
    
# Make dir app
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip3 install -U --extra-index-url https://alpine-wheels.github.io/index -r requirements.txt
#RUN pip3 install -r requirements.txt

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

# ENV PATH="/usr/bin/chromedriver:${PATH}"

# Expose port 5000 to the outside world
EXPOSE 5000
#CMD ["flask", "run", "--host", "0.0.0.0"]

# Run the executable
CMD ["python", "main.py"]