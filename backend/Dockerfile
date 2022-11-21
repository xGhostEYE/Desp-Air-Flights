#Contents of Dockerfile
#Dockerfile to build an image which supports testing our Qxf2 Page Object Model.
FROM ubuntu:latest
#MAINTAINER Qxf2 Services

ENV TZ=America/Regina

ENV DEBIAN_FRONTEND noninteractive 
# Essential tools and xvfb
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

# python
# RUN apt-get update && apt-get install -yqq \
#     python3 \
#     python3-setuptools \
#     python3-pip \
#     python3-tk

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


    
RUN ln -s /usr/bin/python3 /usr/bin/python

# display
RUN export DISPLAY=:20
RUN Xvfb :20 -screen 0 1366x768x16 &

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
# ENV PATH=”$PATH:/usr/local/bin/python”

# Expose port 5000 to the outside world
EXPOSE 5000
#CMD ["flask", "run", "--host", "0.0.0.0"]

# Run the executable
CMD ["python", "main.py"]