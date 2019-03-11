import multiprocessing

bind = "0.0.0.0:8080"
#workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
reload = True
reload_engine = 'poll'
accesslog = '-'
worker_class = 'gevent'
