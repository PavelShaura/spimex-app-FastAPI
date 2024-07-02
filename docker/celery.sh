#!/bin/bash

celery -A worker.tasks:celery_app worker --loglevel=info &
celery -A worker.tasks:celery_app beat --loglevel=info
