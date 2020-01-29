# Python Pub Sub Kafka Over Rest API

## STEP 1: Host Kafka on Local Machine
```
    docker-compose up -d
```

## STEP 2: Entry Point

```
    gunicorn --worker-class=gevent --access-logfile - app:app
```