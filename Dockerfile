# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER @P3Geek

# Add the application resources URL
# RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

ADD . /rundeck-slack-service

# Update the soruces list and install basic applications
RUN apt-get update && apt-get install -y tar git curl nano wget dialog net-tools \
        build-essential python python-dev python-distribute python3-pip \
        &&  pip3 install -r /rundeck-slack-service/requirements.txt

# Rundeck URL this app will forward requests to
ENV RUNDECK_WEBHOOK_URL https://changeme

# Slack slash command's variable names (used in Slack as /mycommand var1=value1, var2=value2), note value1 and value2 set by slash command
ENV SLACK_VAR1 var1
ENV SLACK_VAR2 var2

# The web port
ENV PORT 8080

# Expose ports (same as PORT)
EXPOSE 8080

# Set the default directory where CMD will execute
WORKDIR /rundeck-slack-service

# Set the default command to execute
# when creating a new container
CMD python3 -u bot.py
