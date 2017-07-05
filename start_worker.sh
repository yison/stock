#!/bin/bash

nohup celery -A tasks worker --loglevel=info -c 300 -f realtime.log -Q for_realtime &
#nohup celery -A tasks worker --loglevel=info -c 640 -f workerA.log -Q for_task_A &
#nohup celery -A tasks worker --loglevel=info -c 128 -f workerB.log -Q for_task_B &
