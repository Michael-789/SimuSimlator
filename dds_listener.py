import queue

from rticonnector.subscriber import Subscriber
from rticonnector.topic_data import TopicEnum


class DDSListener():
    def __init__(self, _queue:queue.Queue):
        self._queue = _queue
        topic_filter = "A_sourceID.A_platformId = 1 AND (A_sourceID.A_systemId = 14 AND  A_sourceID.A_moduleId = 9)"

        self.subscriber = Subscriber(TopicEnum.DETECTION,filter_str = topic_filter, subscribe_event=self.handle_enqueue)


    def start_listening(self):
        print("Start listening for DDS. A_sourceID.A_platformId = 1 AND (A_sourceID.A_systemId = 14 AND  A_sourceID.A_moduleId = 9)")
        self.subscriber.start()

    def handle_enqueue(self, topic_enum: TopicEnum, data, *args, **kwargs):
        self._queue.put(data)
