### Builder stage
FROM python:3.12-slim-bookworm AS builder

COPY docker/prod/app/requirements.txt /tmp

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev build-essential default-libmysqlclient-dev pkg-config python3-dev && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /tmp/wheels -r /tmp/requirements.txt


### Final stage
FROM python:3.12-slim-bookworm

# Python deps.
COPY --from=builder /tmp/wheels /tmp/wheels

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev supervisor libmariadb3 && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    # Install packages from wheels
    pip install --upgrade pip && \
    pip install --no-cache --no-cache-dir /tmp/wheels/* && \
    rm -rf /tmp/wheels && \
    # User settings and environment
    addgroup --gid 1000 --system app && \
    adduser --uid 1000 --system --group app && \
    mkdir -p /usr/src/app && \
    mkdir -p /usr/src/app/logs

# Supervisor and app source
COPY docker/prod/app/supervisor/supervisord.conf /etc/supervisor
COPY docker/prod/app/supervisor/conf.d /etc/supervisor/conf.d
COPY docker/prod/app/scripts/start_app.sh /usr/local/bin
COPY docker/prod/app/scripts/supervisor_starter.sh /usr/local/bin
COPY src/app /usr/src/app

RUN chmod +x /usr/local/bin/start_app.sh && \
    chmod +x /usr/local/bin/supervisor_starter.sh && \
    chown app:app /usr/src/app -R

WORKDIR /usr/src/app
USER app

CMD ["supervisord"]
