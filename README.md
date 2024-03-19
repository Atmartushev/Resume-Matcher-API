Start docker container: docker-compose up

Migrations should be made using: docker-compose exec web python manage.py migrate

Restarting and Running service :
docker-compose down
docker-compose up -d
