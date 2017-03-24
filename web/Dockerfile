FROM codi0/ubuntu-base:1.0

ARG DJANGO_ENV

ENV PYTHONBUFFERED=1
ENV WEB_DIR=/web

RUN mkdir $WEB_DIR

WORKDIR $WEB_DIR

ADD requirements/base.txt $WEB_DIR/  
#ADD requirements/$DJANGO_ENV.txt $WEB_DIR/

#RUN pip install -r $DJANGO_ENV.txt
RUN pip install -r base.txt

ADD . $WEB_DIR/  
