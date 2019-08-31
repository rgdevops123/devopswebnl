# Get the latest OS image.
FROM rgdevops123/rgcentos7.6

# Set Maintainer.
LABEL maintainer "rgdevops123@gmail.com"

# Set the Working Directory.
ARG APPDIR="/devopswebnl/"
WORKDIR ${APPDIR}

# Set the FLASK_APP Environment Variable.
ENV FLASK_APP devopswebnl.py

# Copy over the Application Files.
COPY config.py devopswebnl.py requirements.txt ${APPDIR}
COPY app app
COPY migrations migrations
COPY tests_pytests tests_pytests
COPY tests_unittests tests_unittests

# Install Dependencies.
RUN pip3 install --no-cache-dir -q -r requirements.txt

# Set a Health Check.
HEALTHCHECK --interval=5s \
            --timeout=5s \
            CMD curl -f http://127.0.0.1:5000 || exit 1

# Run the Image as a Non-Root User.
RUN groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser
RUN chown -R appuser:appuser ${APPDIR}
USER appuser

# Inform Docker that the container listens on port 5000.
EXPOSE 5000

# Specify the command to run.
ENTRYPOINT ["gunicorn","--bind","0.0.0.0:5000","devopswebnl:app"]
