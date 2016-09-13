from kombu import Queue

BROKER_URL = 'amqp://guest@10.239.131.155:5672//'
CELERY_RESULT_BACKEND = 'rpc://'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_ENABLE_UTC = True
CELERY_QUEUES = (
    Queue('default',    routing_key='default'),
    Queue('for_task_A', routing_key='for_task_A'),
    Queue('for_task_B', routing_key='for_task_B'),
)
