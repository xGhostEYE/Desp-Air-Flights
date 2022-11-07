# Dockerfile References: https://docs.docker.com/engine/reference/builder/

# Start from python:3.8-alpine base image
FROM python:3.10-alpine
#FROM nickgryg/alpine-pandas:3.9.12 as base



# The latest alpine images don't have some tools like (`git` and `bash`).
# Adding git, bash and openssh to the image
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh libstdc++


# Make dir app
RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --extra-index-url https://alpine-wheels.github.io/index -r requirements.txt
#RUN pip3 install -r requirements.txt

# Copy the source from the current directory to the Working Directory inside the container
COPY . .



# Expose port 5000 to the outside world
EXPOSE 5000
#CMD ["flask", "run", "--host", "0.0.0.0"]

# Run the executable
CMD ["python", "main.py"]