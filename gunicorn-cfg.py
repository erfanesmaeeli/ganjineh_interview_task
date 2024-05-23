bind = ':8000'
workers = 4
threads =  3
accesslog = 'logs/gunicorn.access.log'
errorlog = 'logs/errors.log'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True