import random

from hashids import Hashids


class Lobby:
    def __init__(self, l_id: str, l_idx: int):
        self.id: str = l_id
        self.idx: int = l_idx
        self.players: list[str] = []

    def add_player(self, p_id: str):
        if not (p_id in self.players):
            self.players.append(p_id)
            return True

        return False

    def remove_player(self, p_id: str):
        if (idx := self.find_player(p_id)) in range(len(self.players)):
            self.remove_player_at(idx)
            return True

        return False

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


hashids = Hashids(min_length=8, salt="rise and shine Dr Freeman")
lobbies = []
start_idx = random.randint(0, 100)


def new_lobby(creator_id: str):
    """Extra possible parameters:
    - game settings
    - max players
    """
    current_idx = start_idx + len(lobbies)

    lobby_id = hashids.encode(current_idx)

    l = Lobby(lobby_id, current_idx)
    l.add_player(creator_id)

    lobbies.append(l)

    return lobby_id, len(lobbies) - 1


def join_lobby(player_id: str, lobby_idx: int):
    if lobby_idx in range(len(lobbies)):
        lobbies[lobby_idx].add_player(player_id)


def leave_lobby(player_id: str, lobby_idx: int):
    l: Lobby = lobbies[int(lobby_idx)]

    left: bool = l.remove_player(player_id)

    removed: bool = False
    if l.is_empty():
        lobbies.pop(lobby_idx)
        removed = True

    return left, removed

def lobby_id_range():
    return range(start_idx + len(lobbies))

def find_lobby(lobby_id: str):
    for l in lobbies:
        if l.id == lobby_id:
            return l

    return None
def find_lobby_idx(lobby_id: str):
    for idx, l in enumerate(lobbies):
        if l.id == lobby_id:
            return idx

    return -1
