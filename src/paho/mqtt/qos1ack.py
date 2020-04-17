import threading

class Once(object):
    def __init__(self, callableFn):
        self._m = threading.Lock()
        self._callable = callableFn
        self._called = False
        self._result = None

    def execute(self):
        with self._m:
            if not self._called:
                self._result = self._callable()
        return self._result

def upon_delivery(handle_message, send_ack):
    rc = send_ack()
    handle_message(lambda: rc)
    return rc

def once_message_handled(handle_message, send_ack):
    send_ack_function = Once(send_ack)
    handle_message(send_ack_function.execute)
    return send_ack_function.execute()

STRATEGIES = {
    "UPON_DELIVERY": upon_delivery, 
    "ONCE_MESSAGE_HANDLED": once_message_handled
}

def get_strategy(identifier):
    if identifier in STRATEGIES:
        return STRATEGIES[identifier]
    return None

def list_available_strategies():
    return STRATEGIES.values()

