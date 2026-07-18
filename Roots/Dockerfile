# Stage 1: Build & Dependency Isolation
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Hardened Production Runtime
FROM python:3.11-slim AS runner
WORKDIR /app

RUN groupadd -g 10002 app-group && \
    useradd -u 10002 -g app-group -s /bin/bash -m app-user

COPY --from=builder /root/.local /home/app-user/.local
COPY app.py .

RUN chown -R app-user:app-group /app
USER 10002

ENV PATH=/home/app-user/.local/bin:$PATH
ENV APP_ENV=production

EXPOSE 8080
ENTRYPOINT ["python", "app.py"]