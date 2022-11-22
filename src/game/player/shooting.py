from game.game import Game
from game.player import Player
from game.team import other_team


def did_shot_go_in(_distance: float) -> float:
    return True


def player_shoots(game: Game, player: Player):
    assert player.has_ball
    assert game.team_with_ball == player.team

    player.has_ball = False
    target_basket = game.court.target_rim_position(player.team)
    shot_distance = player.position.get_distance(target_basket)

    scored = did_shot_go_in(shot_distance)
    if scored:
        game.scores[player.team] += 2
        game.court.hoops[other_team(player.team)].score()

    game.team_with_ball = other_team(player.team)
    for other_player in game.players:
        if other_player.team != player.team:
            other_player.has_ball = True
            break
