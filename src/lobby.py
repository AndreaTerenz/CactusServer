import random
from dataclasses import dataclass, field

from hashids import Hashids


class Lobby:
    def __init__(self, i: str):
        self.id: str = i
        self.players: list[str] = []

    def add_player(self, p_id: str):
        if not(p_id in self.players):
            self.players.append(p_id)

    def remove_player(self, p_id: str):
        if (idx := self.find_player(p_id)) in len(self.players):
            self.remove_player_at(idx)

    def remove_player_at(self, idx: int):
        self.players.pop(idx)

    def find_player(self, p_id: str):
        # A bit more efficient (get the idx as soon as possible or "die" trying)
        try:
            return self.players.index(p_id)
        except ValueError:
            return -1

    def is_empty(self):
        return len(self.players) <= 0

hashids = Hashids(min_length=6)

lobbies = []
start_id_idx = random.randint(0, 100)
current_id_idx = start_id_idx
print(start_id_idx)


def new_lobby(creator_id: str):
    """Extra possible parameters:
    - game settings
    - max players
    """
    global current_id_idx

    lobby_id = hashids.encode(current_id_idx)
    current_id_idx += 1

    l = Lobby(lobby_id)
    l.add_player(creator_id)

    lobbies.append(l)
    return lobby_id, len(lobbies) - 1


def join_lobby(player_id: str, lobby_idx: int):
    if lobby_idx in range(len(lobbies)):
        lobbies[lobby_idx].add_player(player_id)


def leave_lobby(player_id: str, lobby_idx: int):
    if lobby_idx in range(len(lobbies)):
        l : Lobby = lobbies[lobby_idx]
        l.remove_player(player_id)

        if l.is_empty():
            lobbies.pop(lobby_idx)
