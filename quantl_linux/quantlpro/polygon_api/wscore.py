import json
import signal
import threading
from typing import Optional, Callable
import time
from threading import Thread
import websocket


STOCKS_CLUSTER = "stocks"
FOREX_CLUSTER = "forex"
CRYPTO_CLUSTER = "crypto"


class WebSocketClient:
    DEFAULT_HOST = "socket.polygon.io"

    # TODO: Either an instance of the client couples 1:1 with the cluster or an instance of the Client couples 1:3 with
    #  the 3 possible clusters (I think I like client per, but then a problem is the user can make multiple clients for
    #  the same cluster and that's not desirable behavior,
    #  somehow keeping track with multiple Client instances will be the difficulty)
    def __init__(self, cluster: str, auth_key: str, process_message: Optional[Callable[[str], None]] = None,
                 on_close: Optional[Callable[[websocket.WebSocketApp], None]] = None,
                 on_error: Optional[Callable[[websocket.WebSocketApp, str], None]] = None,
                 should_print = True ,mongo_collection=None):
        self._host = self.DEFAULT_HOST
        self.url = f"wss://{self._host}/{cluster}"
        self.ws: websocket.WebSocketApp = websocket.WebSocketApp(self.url, on_open=self._default_on_open(),
                                                                 on_close=self._default_on_close,
                                                                 on_error=self._default_on_error,
                                                                 on_message=self._default_on_message())
        self.auth_key = auth_key
        self.should_print = should_print
        self.process_message = process_message
        self.ws.on_close = on_close
        self.ws.on_error = on_error

        # being authenticated is an event that must occur before any other action is sent to the server
        self._authenticated = threading.Event()
        # self._run_thread is only set if the client is run asynchronously
        self._run_thread: Optional[threading.Thread] = None

        '''Eventually for our ML we wish to store data in our MDB cluster for mining '''
        self.mongo_collection = mongo_collection

        # TODO: this probably isn't great design.
        #  If the user defines their own signal handler then this will gets overwritten.
        #  We still need to make sure that killing, terminating, interrupting the program closes the connection
        signal.signal(signal.SIGINT, self._cleanup_signal_handler())
        signal.signal(signal.SIGTERM, self._cleanup_signal_handler())



    def run(self):
        self.ws.run_forever()


    def run_async(self):
        self._run_thread = threading.Thread(target=self.run)
        self._run_thread.start()

    def close_connection(self):
        self.ws.close()
        if self._run_thread:
            self._run_thread.join()

    def subscribe(self, *params):
        # TODO: make this a decorator or context manager
        self._authenticated.wait()

        sub_message = '{"action":"subscribe","params":"%s"}' % self._format_params(params)

        self.ws.send(sub_message)
        #self.ws.send(json.dumps(sub_message))

    def _keepalive(self, interval=30):
        while self.ws.connected:
            self.ws.ping("keepalive")
            time.sleep(interval)

    def _listen(self):
        self.keepalive.start()
        while not self.stop:
            try:
                data = self.ws.recv()
                msg = json.loads(data)
            except ValueError as e:
                self.on_error(e)
            except Exception as e:
                self.on_error(e)
            else:
                self.on_message(msg)


    def unsubscribe(self, *params):
        # TODO: make this a decorator or context manager
        self._authenticated.wait()

        sub_message = '{"action":"unsubscribe","params":"%s"}' % self._format_params(params)
        self.ws.send(sub_message)

    def _cleanup_signal_handler(self):
        return lambda signalnum, frame: self.close_connection()

    def _authenticate(self, ws):
        ws.send('{"action":"auth","params":"%s"}' % self.auth_key)
        self._authenticated.set()

    @staticmethod
    def _format_params(params):
        return ",".join(params)

    @property
    def process_message(self):
        return self.__process_message

    @process_message.setter
    def process_message(self, pm):
        if pm:
            self.__process_message = pm
            self.ws.on_message = lambda ws, message: self.__process_message(message)

    def _default_on_message(self):
        return lambda ws, message: self._default_process_message(message)


    @staticmethod
    def _default_process_message(message):
        print(message)

    def _default_on_open(self):
        def f(ws):
            self._authenticate(ws)

        return f

    @staticmethod
    def _default_on_error(ws, error):
        print("error:", error)

    @staticmethod
    def _default_on_close(ws):
        print("### closed ###")