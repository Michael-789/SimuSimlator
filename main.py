# This is a sample Python script.
import json
import os
import queue
import threading

import socketio


import dds_publisher
from SimObj import SimObj
from convertor import convert_from_idl, convert_to_idl
from dds_listener import DDSListener
from dds_publisher import DDSPublisher

sub_queue = queue.Queue(3000)
# Press the green button in the gutter to run the script.

sio = socketio.Client()
socketio_host = os.getenv("SOCKETIO_SERVER", "localhost")
socketio_port = os.getenv("SOCKETIO_PORT", "5000")
sio.connect(f'http://{socketio_host}:{socketio_port}')
dds_publisher = DDSPublisher()


def get_detection():
    while True:
        detection = sub_queue.get()
        obj = convert_from_idl(detection)
        json_obj = obj.serialize_to_string()
        print("Got detection:", json_obj)
        try:
            sio.emit("client_message", json_obj)
        except KeyboardInterrupt:
            sio.disconnect()


@sio.event
def connect():
    print("Connected to server!")
    # Send message to server
    sio.emit('my_message', {'data': 'Hello from client!'})

@sio.event
def server_message(json_obj):
    print(f"Received from server: {json_obj}")
    tempObj = json.loads(json_obj)
    simObj = SimObj(**tempObj)
    detection = convert_to_idl(simObj)
    dds_publisher.publish(detection)


@sio.event
def disconnect():
    print("Disconnected from server")


if __name__ == '__main__':
    dds_subscriber = DDSListener(sub_queue)
    dds_subscriber.start_listening()
    threading.Thread(target=get_detection, daemon=True).start()
    dds_subscriber.subscriber.join()
    sio.disconnect()

