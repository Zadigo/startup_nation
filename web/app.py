from flask import Flask

from startup_nation.app.config.context import context_processor

app = Flask(__file__)


@app.route('/')
def home():
    return

if __name__ == "__main__":
    app.run(host='localhost', port=7000, use_debugger=True)
