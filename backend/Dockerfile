#Contents of Dockerfile
#Dockerfile to build an image which supports webscraping that uses selenium and others
FROM ubuntu:latest

#set timezone
ENV TZ=America/Regina

# setting environment variable to set the dev frontend to noninteractive
ENV DEBIAN_FRONTEND noninteractive

# Essential tools installing
RUN apt-get update && apt-get install -yqq \
    software-properties-common \
    unzip \
    curl \
    xvfb \
    gnupg2 \
    wget \
# python
    python3 \
    python3-setuptools \
    python3-pip \
    python3-tk



# Chrome browser to run the tests
RUN curl https://dl-ssl.google.com/linux/linux_signing_key.pub -o /tmp/google.pub \
    && cat /tmp/google.pub | apt-key add -; rm /tmp/google.pub \
    && echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list \
    && mkdir -p /usr/share/desktop-directories \
    && apt-get -y update && apt-get install -y google-chrome-stable
# Disable the SUID sandbox so that chrome can launch without being in a privileged container
RUN dpkg-divert --add --rename --divert /opt/google/chrome/google-chrome.real /opt/google/chrome/google-chrome \
    && echo "#!/bin/bash\nexec /opt/google/chrome/google-chrome.real --no-sandbox --disable-setuid-sandbox \"\$@\"" > /opt/google/chrome/google-chrome \
    && chmod 755 /opt/google/chrome/google-chrome
 
# Chrome Driver
RUN mkdir -p /opt/selenium \
    && curl http://chromedriver.storage.googleapis.com/2.45/chromedriver_linux64.zip -o /opt/selenium/chromedriver_linux64.zip \
    && cd /opt/selenium; unzip /opt/selenium/chromedriver_linux64.zip; rm -rf chromedriver_linux64.zip; ln -fs /opt/selenium/chromedriver /usr/local/bin/chromedriver;

# Firefox browser to run the tests
RUN apt-get install -yqq firefox
 
# Gecko Driver
ENV GECKODRIVER_VERSION 0.23.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION \
  && chmod 755 /opt/geckodriver-$GECKODRIVER_VERSION \
  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/geckodriver \
  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/wires


#create symbolic link between python3 and python so you can use 
# them interchangeably to run python files
RUN ln -s /usr/bin/python3 /usr/bin/python

# display
RUN export DISPLAY=:20
RUN Xvfb :20 -screen 0 1366x768x16 &

# Make dir app
RUN mkdir /app
#set working directory
WORKDIR /app
#copy requirements over
COPY requirements.txt requirements.txt
# make sure pip is up to date
RUN pip3 install --upgrade pip

#install all python dependencies
RUN pip3 install -U --extra-index-url https://alpine-wheels.github.io/index -r requirements.txt

# Copy the source from the current directory to the Working Directory inside the container
COPY . .


# Expose port 5000 to the outside world for flask to use
EXPOSE 5000


# Run the main executable to start flask
#CMD ["python", "main.py"]
CMD ["./wait-for-it.sh", "bolt://cmpt370-db:7687","-t", "40", "--", "python", "main.py"]
