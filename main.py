import random
import copy
from reportlab.pdfgen import canvas

while True:
    n1 = int(
        input(
            "Please enter how big you want your board to be (q x q). Values must be between (3 - 9): "
        )
    )
    if 3 <= n1 <= 9:
        break
WIDTH = n1
HEIGHT = n1
board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

carved_board = -1


def is_valid(x, y):
    return 0 <= x < WIDTH and 0 <= y < HEIGHT


def carve_out_board(board, curr_i, curr_j):
    global carved_board
    if carved_board != -1:
        return
    if curr_j == WIDTH:
        curr_j = 0
        curr_i += 1
    if curr_i == HEIGHT:
        if carved_board == -1:
            carved_board = copy.deepcopy(board)
        return
    r = list(range(1, WIDTH + 1))
    random.shuffle(r)
    for n1 in r:
        is_valid = True
        for n2 in board[curr_i]:
            if n2 == n1:
                is_valid = False
                break
        for i in range(HEIGHT):
            if board[i][curr_j] == n1:
                is_valid = False
                break
        if is_valid == True:
            board[curr_i][curr_j] = n1
            carve_out_board(board, curr_i, curr_j + 1)
            board[curr_i][curr_j] = 0


splitted_board = -1
trackings = -1


def split_out_board(board, counters, curr_ss, curr_i, curr_j, t):
    global splitted_board, trackings
    if splitted_board != -1:
        return
    if sum(board, []).count(0) == 1:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    board[i][j] = curr_ss
                    t[curr_ss].append((i, j))
                    break
        if splitted_board == -1:
            splitted_board = copy.deepcopy(board)
            trackings = copy.deepcopy(t)
        return
    if counters == 0:
        counters = random.randint(1, 4)
        curr_ss += 1
        t[curr_ss] = []
    pathways = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # random.shuffle(pathways);
    for ni, nj in pathways:
        next_i = curr_i + ni
        next_j = curr_j + nj
        if is_valid(next_j, next_i) and board[next_i][next_j] == 0:
            board[curr_i][curr_j] = curr_ss
            t[curr_ss].append((curr_i, curr_j))
            split_out_board(board, counters - 1, curr_ss, next_i, next_j, t)
            t[curr_ss].pop()
            board[curr_i][curr_j] = 0
    return


carve_out_board(board, 0, 0)
split_out_board(board, 0, 0, 0, 0, {})

for row in carved_board:
    print(row)
print("\n")

the_operations = {}
for key in trackings:
    if len(trackings[key]) == 0:
        continue
    if (
        len(trackings[key]) == 2
        and carved_board[trackings[key][0][0]][trackings[key][0][1]]
        % carved_board[trackings[key][1][0]][trackings[key][1][1]]
        == 0
    ):
        key_opp = "/"
        evaluations = [
            str(carved_board[trackings[key][0][0]][trackings[key][0][1]]),
            "/",
            str(carved_board[trackings[key][1][0]][trackings[key][1][1]]),
        ]
    elif (
        len(trackings[key]) == 2
        and carved_board[trackings[key][1][0]][trackings[key][1][1]]
        % carved_board[trackings[key][0][0]][trackings[key][0][1]]
        == 0
    ):
        key_opp = "/"
        evaluations = [
            str(carved_board[trackings[key][1][0]][trackings[key][1][1]]),
            "/",
            str(carved_board[trackings[key][0][0]][trackings[key][0][1]]),
        ]
    elif len(trackings[key]) == 2:
        key_opp = "-"
        evaluations = [
            str(carved_board[trackings[key][1][0]][trackings[key][1][1]]),
            "-",
            str(carved_board[trackings[key][0][0]][trackings[key][0][1]]),
        ]
    elif len(trackings[key]) == 1:
        key_opp = ""
        evaluations = str(carved_board[trackings[key][0][0]][trackings[key][0][1]])
        the_operations[key] = [key_opp, evaluations]
        continue
    else:
        key_opp = random.choice(["+", "*"])
        evaluations = []
        for y, x in trackings[key]:
            evaluations.append(str(carved_board[y][x]))
            evaluations.append(key_opp)
        evaluations.pop()
    evaluations = int(abs(eval("".join(evaluations))))
    the_operations[key] = [key_opp, evaluations]

q = 50
my_canvas = canvas.Canvas(
    "ken_ken_board.pdf", pagesize=((q * 2) + (WIDTH * q), (q * 2) + (HEIGHT * q))
)
my_canvas.setFont("Helvetica", 8)

my_answers = canvas.Canvas(
    "ken_ken_answers.pdf", pagesize=((q * 2) + (WIDTH * q), (q * 2) + (HEIGHT * q))
)


def draw_out_canvas():
    ares_dones = {}
    my_canvas.setLineWidth(1)
    tempf = WIDTH * q
    for i in range(len(splitted_board)):
        for j in range(len(splitted_board[i])):
            col = splitted_board[i][j]
            curr_i = q * (i + 1) - q
            curr_j = q * (j + 1)
            -q
            upper_bound, lower_bound, left_bound, right_bound = (
                False,
                False,
                False,
                False,
            )
            if i == 0 or splitted_board[i - 1][j] != col:
                upper_bound = True
            if i == len(splitted_board) - 1 or splitted_board[i + 1][j] != col:
                lower_bound = True
            if j == 0 or splitted_board[i][j - 1] != col:
                left_bound = True
            if j == len(splitted_board[i]) - 1 or splitted_board[i][j + 1] != col:
                right_bound = True
            if upper_bound == True:
                my_canvas.setLineWidth(5)
                # print(curr_i + 25 , col);
                my_canvas.line(
                    curr_j, tempf - curr_i + q, curr_j + q, tempf - curr_i + q
                )
                my_canvas.setLineWidth(1)
            else:
                my_canvas.line(
                    curr_j, tempf - curr_i + q, curr_j + q, tempf - curr_i + q
                )
            if lower_bound == True:
                my_canvas.setLineWidth(5)
                my_canvas.line(curr_j, tempf - curr_i, curr_j + q, tempf - curr_i)
                my_canvas.setLineWidth(1)
            else:
                my_canvas.line(curr_j, tempf - curr_i, curr_j + q, tempf - curr_i)
            if left_bound == True:
                my_canvas.setLineWidth(5)
                my_canvas.line(curr_j, tempf - curr_i, curr_j, tempf - curr_i + q)
                my_canvas.setLineWidth(1)
            else:
                my_canvas.line(curr_j, tempf - curr_i, curr_j, tempf - curr_i + q)
            if right_bound == True:
                my_canvas.setLineWidth(5)
                my_canvas.line(
                    curr_j + q, tempf - curr_i, curr_j + q, tempf - curr_i + q
                )
                my_canvas.setLineWidth(1)
            else:
                my_canvas.line(
                    curr_j + q, tempf - curr_i, curr_j + q, tempf - curr_i + q
                )
            if col not in ares_dones:
                key1, n1 = the_operations[col]
                my_canvas.drawString(curr_j + 3, tempf - curr_i + 34, f"{n1}, {key1}")
            ares_dones[col] = True


def draw_out_answers(my_canvas):
    ares_dones = {}
    my_canvas.setLineWidth(1)
    tempf = WIDTH * q
    for i in range(len(splitted_board)):
        for j in range(len(splitted_board[i])):
            col = splitted_board[i][j]
            curr_i = q * (i + 1) - q
            curr_j = q * (j + 1)
            -q
            upper_bound, lower_bound, left_bound, right_bound = (
                False,
                False,
                False,
                False,
            )
            if i == 0 or splitted_board[i - 1][j] != col:
                upper_bound = True
            if i == len(splitted_board) - 1 or splitted_board[i + 1][j] != col:
                lower_bound = True
            if j == 0 or splitted_board[i][j - 1] != col:
                left_bound = True
            if j == len(splitted_board[i]) - 1 or splitted_board[i][j + 1] != col:
                right_bound = True
            if upper_bound == True:
                my_canvas.setLineWidth(5)
                # print(curr_i + 25 , col);
                my_canvas.line(
                    curr_j, tempf - curr_i + q, curr_j + q, tempf - curr_i + q
                )
                my_canvas.setLineWidth(1)
            else:
                my_canvas.line(
                    curr_j, tempf - curr_i + q, curr_j + q, tempf - curr_i + q
                )
            if lower_bound == True:
                my_canvas.setLineWidth(5)
                my_canvas.line(curr_j, tempf - curr_i, curr_j + q, tempf - curr_i)
                my_canvas.setLineWidth(1)
            else:
                my_canvas.line(curr_j, tempf - curr_i, curr_j + q, tempf - curr_i)
            if left_bound == True:
                my_canvas.setLineWidth(5)
                my_canvas.line(curr_j, tempf - curr_i, curr_j, tempf - curr_i + q)
                my_canvas.setLineWidth(1)
            else:
                my_canvas.line(curr_j, tempf - curr_i, curr_j, tempf - curr_i + q)
            if right_bound == True:
                my_canvas.setLineWidth(5)
                my_canvas.line(
                    curr_j + q, tempf - curr_i, curr_j + q, tempf - curr_i + q
                )
                my_canvas.setLineWidth(1)
            else:
                my_canvas.line(
                    curr_j + q, tempf - curr_i, curr_j + q, tempf - curr_i + q
                )
            my_canvas.drawString(
                curr_j + int(q / 2) - 3,
                tempf - curr_i + int(q / 2) - 3,
                str(carved_board[i][j]),
            )
            ares_dones[col] = True


draw_out_canvas()
draw_out_answers(my_answers)
my_canvas.save()
my_answers.save()
