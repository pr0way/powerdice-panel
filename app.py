from flask import Flask, render_template
from flask_mqtt import Mqtt
from dotenv import load_dotenv
from os import getenv

load_dotenv() 

app = Flask(__name__)

# Set configuration from environment variables
app.config.update({
    'MQTT_BROKER_URL': getenv('MQTT_BROKER_URL', 'nanomq'),
    'MQTT_BROKER_PORT': int(getenv('MQTT_BROKER_PORT', 1883)),
    'MQTT_KEEPALIVE': int(getenv('MQTT_KEEPALIVE', 60)),
    'MQTT_TLS_ENABLED': getenv('MQTT_TLS_ENABLED', 'false').lower() == 'true',
    'MQTT_TOPIC': getenv('MQTT_DEFAULT_TOPIC', 'powerdice/status'),
})

mqtt = Mqtt()
mqtt.init_app(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc: int) -> None:
    print('Connected to MQTT broker with result code ' + str(rc))
    mqtt.subscribe(app.config['MQTT_TOPIC'])


@mqtt.on_message()
def handle_message(client, userdata, message) -> None:
    print(f'Received message: {message.payload.decode()} on topic {message.topic}')


@app.route('/')
def home():
    return render_template('index.html')