<img src="https://toxsl.com/themes/new/img/logo.png"  alt="Toxsl Technologies">

<p>
  <p>
  TOXSL Technologies, offer end-to-end web development solutions empowering various enterprises to transform their businesses. Our expertise grows with your business constantly and our intuitive web solutions best suit your business requirements.
  </p>
</p>


# About Dressr AI Application

Dressr is a mobile-first, AI-powered wardrobe management platform designed to transform the way users interact with their clothing. The application enables users to digitize their physical wardrobes, create a personalized AI avatar, and receive intelligent outfit suggestions tailored to their style, preferences, and occasions. With virtual try-on capabilities, Dressr acts as a personal stylist—helping users experiment with looks, discover new styles, and optimize their wardrobes. Built with a modular structure, the platform is future-ready, allowing seamless integration of advanced AI features, e-commerce partnerships, and social functionalities as it evolves.

# Prerequisites

* To run this project you must have installed docker.
* Please check mysql status by using command `system mysql status` if it is active then follow below commands
	
# Project Setup Using Docker

1. Create build of of the project using below command.
```sh
docker-compose build --no-cache
```

2. Once build is created use following command to up containers.
```sh
docker-compose up -d
```

3. Execute `django` container.
```sh
docker exec -it <CONTAINER_ID> bash
```

4. Change directory and go inside `app` directory and type below commands
```sh
cd app/
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuerper
python3 manage.py add_django_site
```

5. Install cron inside `app` directory and run cron jobs
```sh
apt-get install cron
python3 manage.py crontab add
exit;
```

6. Restart `django` container.
```sh
docker restart <NAME_OF_CONATAINER>
```

# Running the project:

Once all containers are up and there is no error found in terminal:
- Go To browser and type `localhost:8000`

# Other Useful Commands

1. To create `build` of specific service use below command.
```sh
docker-compose build --no-cache <NAME_OF_SERVICE>
```

2. To `up containers` which are not running.
```sh
docker-compose up -d
```

3. To check container `status` use following command.
```sh
docker ps or pocker ps -a
```

4. To `restart` any container use following command.
```sh
docker restart <NAME_OF_CONATAINER>
```

5. To check logs of specific `container` use following command.
```sh
docker logs --follow <NAME_OF_CONATAINER>
```

6. To kill `container`.
```sh
docker kill <CONTAINER_ID>
```

7. Compose `down` all containers
```sh
docker-compose down
```

# Project Setup Without Docker

# Prerequisites

* Make sure python version `3.8` or above is installed in your system.
* Create database using `phpmyadmin` or directly from `mysql terminal`.
* Go inside project directory and update `.env` file for mysql connection.

# Getting Started

* Go inside `app` directory and install dependencies.
* Use the package manager `pip/pip3` to install requirement.

```bash
pip3 install -r requirement.txt [ubuntu/mac] 
pip install -r requirement.txt [windows]
```


# Project Setup
	
1. Remove `migrations` from all apps.
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```

	
2. Run this command for `makemigrations`.
```bash
python3 manage.py makemigrations [ubuntu/mac] 
python manage.py makemigrations [windows] 
```

			
3. Run this command to `migrate` 
```bash
python3 manage.py migrate [ubuntu/mac] 
python manage.py migrate [windows] 
```

			
4. Run this command to create `superuser`.
```bash
python3 manage.py createsuperuser
```


5. Run this command to start `project`.
```bash
python3 manage.py runserver [ubuntu/mac] 
python manage.py runserver [windows] 

```

# Running the project on different port:

To start this project on different `port` run this command on your terminal:
```bash
python3 manage.py runserver 0:<PORT>[ubuntu/mac] 
python manage.py runserver 0:<PORT>[windows] 
```
