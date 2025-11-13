FROM python:3.10

COPY ./requirements.txt .

# RUN pip3 install -r requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

## To run django server and celery 4 Workers with Concurrency as demon mode
ENV PYTHONPATH=/app
WORKDIR /app

# CMD sh -c "\
# celery -A project worker -l info --autoscale=25,5 -n worker1@%h & \
# celery -A project worker -l info --autoscale=25,5 -n worker2@%h & \
# celery -A project beat -l info & \
# python3 manage.py runserver 0.0.0.0:8000"

CMD sh -c "\
python3 manage.py runserver 0.0.0.0:8000"