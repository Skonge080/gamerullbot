import requests
from flask import Flask
from threading import Thread
import time
from os import environ


PING_URL = os.environ['PING_URL']


app = Flask(__name__)

@app.route('/')
def index():
    return "Alive"

def keep_alive():
    def run():
        app.run(host='0.0.0.0', port=8080)

    t = Thread(target=run)
    t.start()


def send_request():
    def send():
        while True:
            try:
                response = requests.head(PING_URL)
                if response.status_code == 200:
                    print("Успешный запрос к проекту")
                else:
                    print(f"Ошибка при обращении к проекту. Код состояния: {response.status_code}")
            except Exception as e:
                print(f"Произошла ошибка при выполнении запроса: {str(e)}")
            
            time.sleep(60)

    t = Thread(target=send)
    t.start()
