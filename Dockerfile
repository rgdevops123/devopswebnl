# Get the latest OS image.
FROM rgdevops123/rgcentos7.6

# Set the working directory.
ARG APPDIR="/devopswebnl/"
WORKDIR ${APPDIR}

# Set the FLASK_APP environment variable.
ENV FLASK_APP devopswebnl.py

# Copy over the application files.
COPY config.py devopswebnl.py requirements.txt .env ${APPDIR}
COPY app app
COPY migrations migrations
COPY tests_pytests tests_pytests
COPY tests_unittests tests_unittests

# Install dependencies.
RUN pip3 install --no-cache-dir -q -r requirements.txt

# Run the image as a non-root user.
RUN groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser
RUN chown -R appuser:appuser ${APPDIR}
USER appuser

# Inform Docker that the container listens on port 5000.
EXPOSE 5000

# Specify the command to run.
ENTRYPOINT ["gunicorn","--bind","0.0.0.0:5000","devopswebnl:app"]
