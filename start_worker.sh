#!/bin/bash

nohup celery -A tasks worker --loglevel=error -c 768 -f worker.log -n workerA -Q for_task_A &
nohup celery -A tasks worker --loglevel=error -c 256 -f worker.log -n workerB -Q for_task_B &
