import logging
import os
import time
import random
from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram, Gauge

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('flask_app_info', 'FlaskOps info', version='1.0.0')

order_counter = Counter('flaskops_orders_total', 'Total orders', ['status'])
db_query_time = Histogram('flaskops_db_query_seconds', 'DB query')
active_users = Gauge('flaskops_active_users', 'Active users')


@app.route('/health')
def health():
    return {
        "status": "healthy", "version": os.getenv(
            "APP_VERSION", "1.0.0")}, 200


@app.route('/ready')
def readiness():
    return {"ready": True}, 200


@app.route('/')
def index():
    active_users.set(random.randint(10, 100))
    return {"app": "FlaskOps", "message": "Running on Kubernetes!",
            "pod": os.getenv("POD_NAME", "unknown"),
            "namespace": os.getenv("POD_NAMESPACE", "unknown")}


@app.route('/orders', methods=['POST'])
def create_order():
    with db_query_time.time():
        time.sleep(random.uniform(0.01, 0.1))
    status = random.choice(['success', 'success', 'success', 'failed'])
    order_counter.labels(status=status).inc()
    if status == 'failed':
        return {"error": "Order failed"}, 500
    return {
        "order_id": f"ORD-{random.randint(1000, 9999)}", "status": "created"}, 201


@app.route('/stress')
def stress():
    s = time.time()
    while time.time() - s < 2:
        _ = sum(i * i for i in range(10000))
    return {"message": "CPU stressed"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
