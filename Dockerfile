FROM rgdevops123/rgcentos7.6

ARG APPDIR="/devopswebnl/"
WORKDIR ${APPDIR}

ENV FLASK_APP devopswebnl.py

COPY config.py devopswebnl.py docker-run.sh gunicorn.py requirements.txt .env ${APPDIR}
COPY app app
COPY migrations migrations
COPY tests_pytests tests_pytests
COPY tests_selenium tests_selenium
COPY tests_unittests tests_unittests

RUN /usr/local/bin/pip3 install -r requirements.txt

EXPOSE 5000
EXPOSE 25

ENTRYPOINT ["/devopswebnl/docker-run.sh"]
