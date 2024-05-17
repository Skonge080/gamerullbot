import requests
from flask import Flask
from threading import Thread
import time

app = Flask(__name__)

@app.route('/')
def index():
    return "Alive"

def keep_alive():
    def run():
        app.run(host='0.0.0.0', port=8080)

    t = Thread(target=run)
    t.start()

def send_get_request():
    def send():
        while True:
            try:
                response = requests.head('http://127.0.0.1:8080/')
                if response.status_code == 200:
                    print("Успешный запрос к проекту")
                else:
                    print(f"Ошибка при обращении к проекту. Код состояния: {response.status_code}")
            except Exception as e:
                print(f"Произошла ошибка при выполнении запроса: {str(e)}")
            
            time.sleep(60)

    t = Thread(target=send)
    t.start()
