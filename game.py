from typing import List
from enum import Enum
from random import randint


class _Roll(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3

    def __str__(self):
        return self.name.lower()


class _Player:
    id: int
    chips: int

    def __init__(self, player_id, chips):
        self.id = player_id
        self.chips = chips


def _roll_dice() -> _Roll:
    roll = randint(1, 6)
    assert (0 < roll < 7)

    if roll < 3:
        return _Roll.LEFT
    elif 2 < roll < 5:
        return _Roll.RIGHT
    elif roll > 4:
        return _Roll.CENTER


def _next_player(current_player: _Player, players: List[_Player]) -> _Player:
    new_index = players.index(current_player) + 1
    if new_index >= len(players):
        new_index = 0
    return players[new_index]


def _previous_player(current_player: _Player, players: List[_Player]):
    new_index = players.index(current_player) - 1
    if new_index < 0:
        new_index = len(players) - 1
    return players[new_index]


def play_game(number_of_players: int, starting_chips: int = 5, log=True):
    players: List[_Player] = [
        _Player(player_id, starting_chips) for player_id in range(number_of_players)
    ]

    player = players[0]
    while len(players) > 1:
        print(f"Player {player.id}") if log else ...

        if player.chips == 0:
            old_player = player
            player = _next_player(player, players)
            players.remove(old_player)
            print(f"has just been eliminated") if log else ...
            continue

        rolls = [_roll_dice()]

        if player.chips > 1:
            rolls.append(_roll_dice())
            print(f"Rolled {rolls[0]} and {rolls[1]}") if log else ...
        elif log:
            print(f"Rolled {rolls[0]}")

        for roll in rolls:
            if roll == _Roll.CENTER:
                player.chips -= 1
            elif roll == _Roll.LEFT:
                _previous_player(player, players).chips += 1
                player.chips -= 1
            elif roll == _Roll.RIGHT:
                _next_player(player, players).chips += 1
                player.chips -= 1
            else:
                raise ValueError(f"Unexpected roll {roll}")

        player = _next_player(player, players)

    winning_player = players[0]
    print(f"This winner was player {winning_player.id}") if log else ...


if __name__ == '__main__':
    num_players = int(input("Number of Players: "))
    play_game(num_players)
