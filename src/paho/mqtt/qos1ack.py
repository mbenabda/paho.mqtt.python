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

def upon_successful_handling(handle_message, send_ack):
    send_ack_function = Once(send_ack)
    err = handle_message(send_ack_function.execute)
    if err is None:
        return send_ack_function.execute()
    return 0

STRATEGIES = {
    "UPON_DELIVERY": upon_delivery, 
    "UPON_SUCCESSFUL_HANDLING": upon_successful_handling
}

def get_strategy(identifier):
    if identifier in STRATEGIES:
        return STRATEGIES[identifier]
    return None

def list_available_strategies():
    return STRATEGIES.values()

