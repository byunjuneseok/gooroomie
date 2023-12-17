workers = 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 30
threads = 1

bind = "0.0.0.0:8080"

pythonpath = "app"
wsgi_app = "applications.http.main:create_app()"
