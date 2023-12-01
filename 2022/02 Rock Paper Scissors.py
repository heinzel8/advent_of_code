from enum import Enum

filename = r"02 Rock Paper Scissors.txt"

def get_input_data():
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]

def get_test_data():
    return "A Y,B X,C Z".split(",")

class shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3

class game_result(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6

def to_move(c:str):
    if c in ["A", "X"]:
        return shape.ROCK
    if c in ["B", "Y"]:
        return shape.PAPER
    if c in ["C", "Z"]:
        return shape.SCISSOR

def to_result(c:str):
    if c == "X":
        return game_result.LOSE
    elif c == "Y":
        return game_result.DRAW
    elif c == "Z":
        return game_result.WIN

win_lose_map = {
    shape.PAPER: shape.ROCK,
    shape.ROCK: shape.SCISSOR,
    shape.SCISSOR: shape.PAPER }

lose_win_map = dict((val,key) for key,val in win_lose_map.items())

def get_game_result(my_move, others_move):
    if my_move == others_move:
        return game_result.DRAW
    return game_result.WIN if lose_win_map[others_move] == my_move else game_result.LOSE

def calculate_score(my_move:shape, others_move:shape):
    return my_move.value + get_game_result(my_move, others_move).value

def determine_move(expected_result : game_result, others_move : shape):
    if expected_result == game_result.DRAW: 
        return others_move
    elif expected_result == game_result.WIN: 
        return lose_win_map[others_move]
    else:
        return win_lose_map[others_move]

def run_game(lines):
    score1, score2 = 0, 0
    for line in lines:
        col1, col2 = line.split(" ")
        score1 += calculate_score(my_move=to_move(col2), others_move=to_move(col1))
        
        my_move = determine_move(expected_result=to_result(col2), others_move=to_move(col1))
        score2 += calculate_score( my_move, to_move(col1))
        
    return score1, score2

def test_calculate_game_results():
    assert get_game_result(shape.SCISSOR, shape.SCISSOR) == game_result.DRAW
    assert get_game_result(shape.SCISSOR, shape.PAPER) == game_result.WIN
    assert get_game_result(shape.SCISSOR, shape.ROCK) == game_result.LOSE
    
    assert get_game_result(shape.ROCK, shape.ROCK) == game_result.DRAW
    assert get_game_result(shape.ROCK, shape.SCISSOR) == game_result.WIN
    assert get_game_result(shape.ROCK, shape.PAPER) == game_result.LOSE

    assert get_game_result(shape.PAPER, shape.PAPER) == game_result.DRAW
    assert get_game_result(shape.PAPER, shape.ROCK) == game_result.WIN
    assert get_game_result(shape.PAPER, shape.SCISSOR) == game_result.LOSE

def test_reference_solution_one():
    expected = [8, 1, 6]
    for i in range(0, 3):
        data = get_test_data()[i]
        others_move = to_move(data.split(" ")[0])
        my_move = to_move(data.split(" ")[1])
        assert calculate_score(my_move, others_move) == expected[i]

    solution1, _ = run_game(get_test_data())
    assert solution1 == 15

def test_reference_solution_two():
    expected_scores = [4, 1, 7]
    expected_my_moves = [shape.ROCK, shape.ROCK, shape.ROCK]
    for i in range(0, 3):
        col1, col2 = get_test_data()[i].split(" ")
        others_move = to_move(col1)
        my_move = determine_move(expected_result=to_result(col2), others_move=others_move)
        assert my_move == expected_my_moves[i]
        assert calculate_score(my_move, others_move) == expected_scores[i]

    _, solution2 = run_game(get_test_data())
    assert solution2 == 12

def test_solution():
    solution1, solution2 = run_game(get_input_data())
    assert solution1 == 11906
    assert solution2 == 11186

if (__name__ == "__main__"):
    solution1, solution2 = run_game(get_input_data())
    print("solution1", solution1, "points")
    print("solution2", solution2, "points")
