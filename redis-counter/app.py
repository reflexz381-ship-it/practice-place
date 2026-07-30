import os
import redis
from flask import Flask

app = Flask(__name__)
redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379)

@app.route('/')
def count():
    visits = redis_client.incr('visits')
    return f"This page has been visited {visits} times\n"

@app.route('/ping')
def ping():
    pings = redis_client.incr('pings')
    return "pong\n"

@app.route('/ping_stats')
def ping_stats():
    pings = redis_client.get('pings')
    if pings is None:
        pings = 0
    else:
        pings = int(pings)
    return f"Ping has been called {pings} times\n"
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
