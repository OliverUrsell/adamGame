from typing import List, Tuple
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
    human_id: int
    chips: int

    def __init__(self, player_id, chips):
        self.id = player_id
        self.human_id = player_id + 1
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


def play_game(number_of_players: int, starting_chips: int = 5, log=False) -> Tuple[int, List[int]]:
    """
    Play the luck game (See README.md)

    Players are identified by id. Player 2 is to the right of player 1 and player `number_of_players` to the left of
    player 1

    :param number_of_players: The number of players that are in the game
    :param starting_chips: The number of chips each player starts with
    :param log: Whether to print the events of the game to stdout
    :return: (winning player, elimination order) as integer ids - The last id in the elimination order is the winner
    """
    players: List[_Player] = [
        _Player(player_id, starting_chips) for player_id in range(number_of_players)
    ]

    elimination_order = []

    player = players[0]
    while len(players) > 1:
        print(f"Player {player.human_id}") if log else ...

        if player.chips == 0:
            old_player = player
            player = _next_player(player, players)
            players.remove(old_player)
            elimination_order.append(old_player.human_id)
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
    elimination_order.append(winning_player.human_id)
    print(f"The elimination order was: {elimination_order}") if log else ...
    print(f"This winner was player {winning_player.human_id}") if log else ...

    return winning_player.human_id, elimination_order

def play_multiple_games(number_of_players: int, number_of_games: int=100000) -> List[int]:
    """
    Plays multiple games
    :param number_of_games:
    :return: an array where each position is the number of times that player has won
    """
    output = [0]*number_of_players
    for game in range(number_of_games):
        winner, _ = play_game(number_of_players)
        output[winner-1] += 1
    return output


if __name__ == '__main__':
    num_players = int(input("Number of Players: "))
    play_game(num_players, log=True)
