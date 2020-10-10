# Meetup.com RSVP json message Stream to PostgreSQL

Python based Docker application reads Json Stream and stores rsvp json messages to PostgreSQL

## Command to build container image 
```
docker build -t meetup-rsvp .
```

## Command to run container
```
docker run  -e WS_URL=ws://stream.meetup.com/2/rsvps \
  -e DB_HOST=10.10.10.1 \
  -e PORT=5432 \
  -e DB_USERNAME=postgres \
  -e DB_PASSWORD=postgres \
  -e DB_NAME=postgresdb \
  -e DB_POOL_MIN_SIZE=20 \
  -e DB_POOL_MAX_SIZE=20 \
  -e LOG_LEVEL=error \
  -e SHOW_ERROR=false \
  meetup-rsvp
```

## Kubernetes
```
$ kubectl create ns postgresql
$ kubectl apply -f postgresql-configmap.yml -n postgresql
$ kubectl apply -f postgresql-statefulset.yaml -n postgresql
$ kubectl apply -f postgresql-service.yml -n postgresql
$ kubectl apply -f meetup-deployment.yaml -n postgresql
```

## Ref
* ws://stream.meetup.com/2/rsvps
