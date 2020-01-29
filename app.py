import json
import random
from time import sleep
from flask import Flask, render_template, request, Response
from flask_cors import CORS
from kafka import KafkaConsumer, KafkaProducer

app = Flask(__name__)

CORS(app)


producer = KafkaProducer(
    bootstrap_servers="localhost:9094".split(","),
    compression_type='gzip'
)


def event_stream(consumer):
    # forever loop until client or server force close
    while True:
        msg_pack = consumer.poll(timeout_ms=300, max_records=500)
        for _, messages in msg_pack.items():
            for msg in messages:
                # print('data:{0}\n\n'.format(msg.value.decode()))
                yield 'data:{0}\n\n'.format(msg.value.decode())

    # if session interupted
    consumer.close()


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/pub")
def publish():
    sentence = request.args.get('sentence')
    producer.send("TestTopic", json.dumps(sentence).encode('utf-8'))
    return "OK"


@app.route("/sub")
def subscribe():

    consumer = KafkaConsumer(
        'TestTopic',
        enable_auto_commit=True,
        auto_offset_reset='latest',
        bootstrap_servers="localhost:9094".split(","),
        group_id='gid_' + str(random.randint(10, 999)),
    )

    return Response(
        response=event_stream(consumer),
        status=200,
        mimetype='text/event-stream'
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
