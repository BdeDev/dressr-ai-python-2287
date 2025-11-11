#!/bin/bash

# Load environment variables from .env file
set -a
. ./app/project/.env_testing
set +a

until [ "`docker inspect -f {{.State.Health.Status}} mysql-django-1`"=="healthy" ]; do
    sleep 0.1;
done;

# Run MySQL command inside the container
docker exec mysql-django-1 mysql -u root -p "$MYSQL_ROOT_PASSWORD" mysql -e "ALTER USER '$MYSQL_USER'@'%' IDENTIFIED WITH caching_sha2_password BY '$MYSQL_PASSWORD';"

echo "MySQL is up - running migrations..."
python3 ./app/manage.py makemigrations
python3 ./app/manage.py migrate

# Create superuser if it doesn't exist
echo "from accounts.models import User; User.objects.create_superuser('$ADMIN_USERNAME', '$ADMIN_EMAIL', '$ADMIN_PASSWORD') if not User.objects.filter(username='$ADMIN_USERNAME').exists() else None" | python3 ./app/manage.py shell


echo "Removing cron jobs..."
python3 ./app/manage.py crontab remove
echo "Adding cron jobs..."
python3 ./app/manage.py crontab add

echo "Starting cron service..."
service cron start

echo "Starting Django development server..."
python3 ./app/manage.py runserver 0.0.0.0:8000 --reload