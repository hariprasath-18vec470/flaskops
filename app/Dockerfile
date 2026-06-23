FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS production
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY app.py .
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
EXPOSE 5000
CMD ["gunicorn","--bind","0.0.0.0:5000","--workers","2","--threads","2","--access-logfile","-","app:app"]
