# Docker Images

* List Docker images

```
docker images
```

# Docker Containers

* List Docker containers

```
docker container ls -a
```

* Start Docker container

```
docker start <container-id/name>
```

* Stop Docker container

```
docker stop <container-id/name>
```

* Check Docker container logs

```
docker logs --tail 2500 <container-id/name>
```

* To follow Docker log output or tail continuously

```
docker logs --follow <container-id/name>
```

* Stop all the running Docker containers

```
docker stop $(docker ps -a -q)
```

* Prune all containers

```
docker system prune
```

* Prune all container volumes

```
docker system prune --volumes
```

# Docker Compose

* Docker Compose build the system

```
docker-compose -f local.yml build
```

* Docker Compose start the system

```
docker-compose -f local.yml up -d
```

- -f: The Docker Compose yaml file
- -d: Detached - Run in background

* Docker Compose execute command

```
docker-compose -f local.yml run <container-id/name> <command>

# E.g
# docker-compose -f local.yml run web python web/manage.py createsuperuser
# docker-compose -f local.yml run web /bin/sh
```