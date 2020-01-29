# Python Pub Sub Kafka Over Rest API

## STEP 1: Host Kafka on Local Machine
```
docker-compose up -d
```

## STEP 2: Create Kafka Topic
```
docker exec kafka kafka-topics.sh --create --zookeeper zk:2181 --replication-factor 1 --partitions 3 --topic TestTopic
```

## STEP 3: Entry Point

```
gunicorn --worker-class=gevent --access-logfile - app:app
```
