#!/bin/bash

nohup celery -A tasks worker --loglevel=info -c 768 -f workerA.log -Q for_task_A &
nohup celery -A tasks worker --loglevel=info -c 256 -f workerB.log -Q for_task_B &
