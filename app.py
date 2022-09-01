from flask import Flask, request, json
import random
import src.lobby as lobby

app = Flask(__name__)


@app.route('/')
def hello_world():
    return {'Hello': random.randint(0, 9)}


@app.route('/new-lobby/<player_name>', methods=['GET'])
def create_lobby(player_name):
    """Used to create a lobby"""
    l_id, l_idx = lobby.new_lobby(player_name)
    return json.dumps({
        'lobby_id': l_id,
        'lobby_idx': l_idx,
        'success': True,
    }), 200, {'ContentType': 'application/json'}


@app.route('/deck', methods=['GET'])
def get_deck():
    """Used to get the initial shuffled deck"""
    deck = []
    for i in range(1, 41):
        deck.append(i % 10)
    random.shuffle(deck)

    return {'deck': deck}


if __name__ == '__main__':
    app.run()
