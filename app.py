from flask import Flask
import random

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return {'Hello': random.randint(0, 9)}


@app.route('/deck', methods=['GET'])
def get_deck():  # put application's code here
    deck = []
    for i in range(1, 41):
        deck.append(i % 10)
    random.shuffle(deck)

    return {'deck': deck}


if __name__ == '__main__':
    app.run()
