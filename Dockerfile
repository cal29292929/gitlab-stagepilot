FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    STAGEPILOT_HOST=0.0.0.0

COPY pyproject.toml requirements.txt LICENSE README.md .gitlab-ci.yml ./
COPY .gitlab ./.gitlab
COPY stagepilot ./stagepilot
COPY tests ./tests

RUN pip install --no-cache-dir -r requirements.txt || true

EXPOSE 8080

CMD ["python3", "-m", "stagepilot.server", "--host", "0.0.0.0", "--port", "8080"]
