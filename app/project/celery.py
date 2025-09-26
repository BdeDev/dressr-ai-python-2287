import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


## To run celery worker in background demon mode , go to inside django container inside app directory run below commands
'''
docker exec -e PYTHONPATH=/app <dajngo_container_id> celery -A project worker -l info

docker exec -e PYTHONPATH=/app <dajngo_container_id> celery -A project status 
docker exec -e PYTHONPATH=/app milanahoy-django-1 celery -A project status 


celery -A project worker -l info ## run celery worker

celery -A project worker -l info --detach  ## run celery worker in backgrould demon mode

celery -A project worker -l info --concurrency=10 -n worker1@%h ## start celery worker with worker name helpful for if have multiple worker

celery -A project status  ## check celery demon worker status


## celery auto scale ( this will start minimum 5 concurrency and maximum 25 concurrency based on load insted of hard coded concurrency like --concurrency=10 )

celery -A project worker -l info --autoscale=25,5 -n worker1@%h

# doc reference : https://docs.celeryq.dev/en/stable/reference/cli.html#cmdoption-celery-worker-autoscale


### to start worker for celery beat ( preodit task )

celery -A project beat -l info 

celery -A project beat --loglevel=debug 

ps aux | grep 'celery beat' ## Check the Beat Process Directly

## To stop workers 

celery -A project control shutdown



## Check celery process 

ps aux | grep 'celery'

## Kill all process by celery
pkill -9 -f 'celery'

pkill -9 -f 'celery worker1'

## Starte celery process 
celery -A project worker -l info 




## Check the Registered tasks : This shows registered tasks to workers
celery -A project inspect registered


## This command shows tasks currently being executed
celery -A project inspect active

## Check the Queue : This shows tasks that are waiting in the queue but haven’t started yet

celery -A project inspect reserved

## Look for Scheduled Tasks : These are tasks that are delayed or scheduled for future execution

celery -A project inspect scheduled


## Combine All Checks : run all three inspect commands together to get a full picture

celery -A project inspect active reserved scheduled



## Visual using flower

pip3 install flower
celery -A project flower --port=5555
celery -A project flower --port=5555 --basic-auth=user:pswd  ## with authentication user and password


http://localhost:5555/ ## open flower server 


## run server on wsgi using gunicorn over production server

pip3 install gunicorn
    
gunicorn project.wsgi:application --bind 0.0.0.0:8000

gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 3

    
'''