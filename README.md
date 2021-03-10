# Coconut-server



web_api:
        container_name: web-api-container
        build: ./api
        restart: always
        # command: uwsgi  --emperor uwsgi.ini
        command: uwsgi --ini uwsgi.ini
        # ports:
        # - "8002:8000"
        volumes:
        - api_data:/docker_api  //hot reload suspend 
        depends_on:
sudo apt-get install libpq-dev
### 功能

- 第三方登入
- 商品加入購物車
- 非同步寄送訂單確認郵件
- 後台管理
- RWD
- Google analysis
- 部署 (AWS+Docker+uWSGI+NGINX+Certbot)
- CouldWatch

### Tool

Front end:
 - Angular
 - HTML/SCSS
 - Typescript
 - GA (TO DO!)
 
 Backend:
 - Django
 - Celery
 - RabbitMQ
 
 Cache:
 - Redis
 
 Database:
 - PostgreSQL
 
 Deploy:
 - AWS (EC2, S3)
 - Docker
 - Docker-compose
 - NGINX
 - Travis-ci (TO DO!)

```
python3 -m venv venv

#activate the virtualenv
. env/bin/activate
pip install -r requirements.txt

#run the django project
python manage.py migrate
python manage.py loaddata fixtures/*
python manage.py createsuperuser
python manage.py runserver 

Django Server Error: port is already in use
sudo lsof -t -i tcp:8000 | xargs kill -9
```
Certbot
https://xenby.com/b/101-%E6%95%99%E5%AD%B8-%E7%94%B3%E8%AB%8Blets-encrypt%E6%86%91%E8%AD%89%E8%88%87%E5%95%9F%E7%94%A8https-nginx

Migrate database
In general cases:
python manage.py makemigrations
python manage.py migrate

Docker
```
docker container stop $(docker container ls -aq)
docker container rm $(docker container ls -aq)
```
