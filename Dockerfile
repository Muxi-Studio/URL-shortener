FROM python:3.6
MAINTAINER Andrewpqc <andrewpqc@>mails.ccnu.edu.cn>

ENV DEPLOY_PATH /URLshorter

RUN mkdir -p $DEPLOY_PATH
WORKDIR $DEPLOY_PATH

Add requirements.txt requirements.txt
RUN pip install --index-url http://pypi.doubanio.com/simple/ -r requirements.txt --trusted-host=pypi.doubanio.com

Add . .