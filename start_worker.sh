#!/bin/bash

nohup celery -A tasks worker --loglevel=error -c 144 -f worker.log &
