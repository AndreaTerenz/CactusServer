from flask import Flask, request, json
import random, logging, atexit
import src.lobby as lobby

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return {'Hello': random.randint(0, 9)}


@app.route('/new-lobby/<player_name>', methods=['GET'])
def create_lobby(player_name):
    """Used to create a lobby"""
    l_id, l_idx = lobby.new_lobby(player_name)

    logging.info(f"Created lobby '{l_id}' by player '{player_name}'")

    return json.dumps({
        'lobby_id': l_id,
        'lobby_idx': l_idx,
        'success': True,
    }), 200, {'ContentType': 'application/json'}


@app.route('/join-lobby/<player_name>/<lobby_id>', methods=['GET'])
def join_lobby(player_name, lobby_id):
    """Used to create a lobby"""
    idx = lobby.find_lobby_idx(lobby_id)
    ok = False

    if idx != -1:
        ok = lobby.join_lobby(player_name, idx)

    if ok:
        logging.info(f"Player '{player_name}' joined lobby '{lobby_id}'")
        logging.info(f"Players in lobby '{lobby_id}': {lobby.players_in_lobby(lobby_id)}")

    return json.dumps({
        'lobby_id': lobby_id,
        'lobby_idx': idx,
        'success': ok,
    }), 200 if ok else 400, {'ContentType': 'application/json'}


@app.route('/leave-lobby/<player_name>/<lobby_id>', methods=['GET'])
def leave_lobby(player_name, lobby_id):
    """Used to create a lobby"""
    idx = lobby.find_lobby_idx(lobby_id)
    left, removed = lobby.leave_lobby(player_name, idx)

    if left:
        logging.info(f"Player '{player_name}' left lobby '{lobby_id}'")

    if removed:
        logging.info(f"Lobby '{lobby_id}' was removed")

    return json.dumps({'success': left}), 200 if left else 400, {'ContentType': 'application/json'}


@app.route('/deck', methods=['GET'])
def get_deck():
    """Used to get the initial shuffled deck"""
    deck = []
    for i in range(1, 41):
        deck.append(i % 10)
    random.shuffle(deck)

    return {'deck': deck}

def on_shutdown():
    pass

if __name__ == '__main__':
    app.run()
