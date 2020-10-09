# Json Stream to Postgresql

Docker with Python application reads Json Stream and stores rsvp json to Postgresql

## Command to build and 
```
docker build -t meetup-rsvp .
```

## Command to run container
```
docker run -e ws_url=ws://stream.meetup.com/2/rsvps \
  -e db_host=10.10.0.2 \
  -e db_port=5432 \
  -e db_user=postgres \
  -e db_password=postgres \
  -e db_name=books_service \
  -e db_pool_min_size=20 \
  -e db_pool_max_size=20 \
  -e log_level=error \
  -e show_error=false \
  meetup-rsvp
```

## Ref
* ws://stream.meetup.com/2/rsvps
