FROM rgdevops123/rgcentos7.6

ARG APPDIR="/devopsweb/"
WORKDIR ${APPDIR}

ENV FLASK_APP devopsweb.py

COPY config.py devopsweb.py docker-run.sh gunicorn.py requirements.txt .env ${APPDIR}
COPY app app
COPY migrations migrations
COPY tests tests

RUN /usr/local/bin/pip3 install -r requirements.txt

EXPOSE 5000
EXPOSE 25

ENTRYPOINT ["/devopsweb/docker-run.sh"]
