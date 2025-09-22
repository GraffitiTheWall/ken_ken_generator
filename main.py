import random
import copy
from reportlab.pdfgen import canvas

#This is for the command line. It will take in the user's input!
while True:
    n1 = int(
        input(
            "Please enter how big you want your board to be (q x q). Values must be between (3 - 9): "
        )
    )
    if 3 <= n1 <= 9:
        break
        
#Creates the board. A 0 denotes an empty cell.
WIDTH = n1
HEIGHT = n1
board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

carved_board = -1

def is_valid(x, y):
    
    '''
    Checks if an 'x' and a 'y' coordinate are in the bounds of a board.
    '''
    
    return 0 <= x < WIDTH and 0 <= y < HEIGHT

def carve_out_board(board, curr_i, curr_j):

    '''
    All this function does is fill the board with random numbers from 1 to WIDTH (inclusive), making sure that each number is not repeated
    in the same row or column (thus, following the rules of ken_ken). An empty cell will have a value of 0. The program tries to fill in the
    current cell ('curr_i' , 'curr_j') with a valid number (a number that is not repeated in a row or a column). Once that valid number is
    found, it recurses to the next number by adding 1 to curr_j. However, if curr_j is equivalent to the width of that board (i.e., it has
    reached the end of it's row), 1 will be added to curr_i (moving down a row), and, curr_j will equal 0 (to begin with the first cell in
    the new row).
    Once all of the cells have been filled, we save that valid baord into carved board, and all other recursion call stacks will be stopped.
    '''
    
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
    
    '''
    This function carves out the 'cells' in the board. Each cell will store 1 to 4 values (inclusive). We keep track of the amount of values
    in each cell using counters. Once counters hits 0 (all of the values in the cell have been added in), we choose another number from 1 to
    4 (inclusive), which will decide howmany values the next cell stores. Each cell will have a corresponding number (we will call this the
    cell's 'id') given to it, and that 'id' number will be saved and stored in t. Each key in t will be equal to the coordinates of each 
    value that are in that 'cell'.
    We go to the next coordinate by either going up, left, down, or, right, given whatever current coordinate we are in. We check if that 
    next coordinate is valid (i.e., in the bounds of the board) by using the is_valid() function. Once the board has been completely filled
    out (i.e., there are no more empty cells, or, 0s, in the board), we save that board in 'splitted_board', and stop all recursion stack
    calls.
    '''
    
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

'''
This program then proceeds to iterating through each 'id' in trackings, and, choosing an operation for that 'id', or, cell. For example,
an 'id' with one value in it will have no operation ('key_opp'). With a length of two, however, it could have two operations: either
division or subtraction. With a length of greater than two, it's operation could be either of the following: multiplication or addition.
Once an operation is chosen, that operation 'key_opp' and the answer (evaluating all the numbers based off of that 'key_opp', stored
in 'evaluation') will be stored in 'the_operation', along with the cell's 'id', or, 'key'.
'''

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
    
    '''
    This function is used for carving out the board into a pdf file using reportlab. To create the borders, it checks for each bound: upper,
    lower, left, and right bounds for drawing out the 'lines', or, the 'borders', using the 'splitted_board' nested array inside of the 
    canvas file. It writes the key_operation along with the needed value at the top of each cell. It then outputs the canvas as a pdf file
    for the user to use.
    '''
    
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
    
    '''
    The same logic as the draw_out_canvas() function, but now, we are writing in the answers. So, this function is for creating the answer key.
    '''
    
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
