#!/bin/bash
docker compose down -v --remove-orphans --rmi all
docker compose run --rm manage makemigrations
docker compose run --rm manage migrate
docker compose up backend -d
docker compose run --rm manage createsuperuser --noinput --username admin --email admin@example.com
docker compose run --rm manage shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u=User.objects.get(username='admin'); u.set_password('admin'); u.save()"
docker compose run --rm manage loaddata cantina/initial_data.json
