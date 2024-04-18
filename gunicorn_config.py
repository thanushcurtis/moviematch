bind = "0.0.0.0:8080"
workers = 3
worker_class = 'sync' 
threads = 2
wsgi = "app:app"
