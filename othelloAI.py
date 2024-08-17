import sys
import time

def find_next_move(board, player, depth):

   # Max
    if player == "x":
        return max_move(board,depth)
   # that is depth-limited to "depth".  Return the best available move.
    else:
        return min_move(board,depth)



def max_move(board, depth):
    possible = possible_moves(board,"x")
    temp = possible[0]
    maxval = min_step(make_move(board,"x",temp), depth, -1 * infinity, infinity)
    for ind in possible:
        result = min_step(make_move(board,"x",ind), depth, -1 * infinity, infinity)
        if result > maxval:
            maxval = result
            temp = ind
    return temp

def min_move(board, depth):
    possible = possible_moves(board,"o")
    temp =possible[0]
    minval = max_step(make_move(board,"o",temp), depth, -1 * infinity, infinity)
    for ind in possible:
        result = max_step(make_move(board,"o",ind), depth, -1 * infinity, infinity)
        if result < minval:
            minval = result
            temp = ind
    return temp

def max_step(board, depth, alpha, beta):
    if depth == 0 or goaltest(board):
        return score(board)
    results = list()
    for next_board in possible_moves(board, "x"):
        r = min_step(make_move(board,"x",next_board), depth-1, alpha, beta)
        #alphabeta pruning here
        if r > alpha:
            alpha = r
        results.append(r)
    if len(results) == 0:
        return score(board)
    if max(results)<alpha:
        return max(results)
    return alpha

def min_step(board, depth, alpha, beta):
    if depth == 0 or goaltest(board):
        return score(board)
    results = list()
    for next_board in possible_moves(board, "o"):
        r = max_step(make_move(board,"o",next_board), depth-1, alpha, beta)
        #alphabeta pruning here
        if beta > r:
            beta = r
        results.append(r)
    if len(results) == 0:
        return score(board)
    if min(results)>beta:
        return min(results)
    return beta

def score(board):
    sum = 0
    corners = [board[0], board[7], board[56], board[63]]
    for c in corners:
        if c == "x":
            sum += 35
        if c == "o":
            sum += -35
    edges=[board[1],board[8],board[9],board[6],board[14],board[15],board[48],board[49],board[57],board[54],board[55],board[62]]
    for e in edges:
        if e == "x":
            sum += 5
        if e == "o":
            sum += -5
    #next to corners
    if board[0] == ".":
        nexttocorners = [board[1], board[8], board[9]]
        for n in nexttocorners:
            if n == "x":
                sum += -25
            if n == "o":
                sum += 25
    if board[7] == ".":
        nexttocorners = [board[6], board[14], board[15]]
        for n in nexttocorners:
            if n == "x":
                sum += -25
            if n == "o":
                sum += 25
    if board[56] == ".":
        nexttocorners = [board[48], board[49], board[57]]
        for n in nexttocorners:
            if n == "x":
                sum += -25
            if n == "o":
                sum += 25
    if board[63] == ".":
        nexttocorners = [board[62], board[54], board[55]]
        for n in nexttocorners:
            if n == "x":
                sum += -25
            if n == "o":
                sum += 25
    #next to edges
    for x in range(2, 6):
        edge = board[8*x]#left
        if edge == "o":
            if board[8*x+1] == "x":
                sum += -25
        if edge == "x":
            if board[8*x+1] == "o":
                sum += 25
        edge = board[8*(x+1)-1]#top
        if edge == "o":
            if board[8*(x+1)-2] == "x":
                sum += -25
        if edge == "x":
            if board[8*(x+1)-2] == "o":
                sum += 25
        edge = board[x]
        if edge == "o":
            if board[x+8] == "x":
                sum += -25
        if edge == "x":
            if board[x+8] == "o":
                sum += 25
        edge = board[x+56]
        if edge == "o":
            if board[x+48] == "x":
                sum += -25
        if edge == "x":
            if board[x+48] == "o":
                sum += 25

    if board.count("x") >= 32 or board.count("o")>= 32:
        sum += board.count("x") * 10
        sum += board.count("o") * -10
    else:
        xmoves = len(possible_moves(board,"x"))
        omoves = len(possible_moves(board,"o"))
        sum += 10 * (xmoves-omoves)
    return sum


def goaltest(board):
   if "." not in board:
      return True
   if possible_moves(board,"x") == 0 and possible_moves(board,"o") == 0:
      return True
   return False

def convertBoard(board): #8 -> 10
    temp = "??????????"
    for c in range(8):
        temp += "?"
        for r in range(8):
            temp += board[8*c + r]
        temp += "?"
    temp += "??????????"
    return temp

def convertBackBoard(board): #10 -> 8
    temp =""
    for c in range(8):
        for r in range(8):
            temp += board[10*c + r + 11]
    return temp


def possible_moves(board,token):#board is 10x10, token is which symbol ur using
    board = convertBoard(board)
    opponent = "xo"["ox".index(token)]
    possible = set()
    for index in range(0,len(board)):
        if board[index] == token:
            for direction in directions:
                temp = index + direction
                while temp >= 0 and temp < len(board) and board[temp] == opponent:
                    temp += direction
                if temp >= 0 and temp < len(board) and temp != index + direction and board[temp] == ".":
                    possible.add(convert_10i_to_8i(temp))
    return list(possible)   

def convert_10i_to_8i(i):
    return 8* ((i//10) - 1) + i%10-1

def make_move(board,token,index):
    opponent = "xo"["ox".index(token)]
    board = board[:index] + token + board[index+1:]
    board = convertBoard(board)
    index = 10*((index//8) + 1) + index%8+1
    for direction in directions:
        temp = index + direction 
        while temp >= 0 and temp < len(board) and board[temp] == opponent:
            temp += direction
        if temp >= 0 and temp < len(board) and temp != index + direction and board[temp] == token:
            new_temp = index+direction
            while new_temp != temp:
                board = board[:new_temp] + token + board[new_temp+1:]
                new_temp += direction
    return convertBackBoard(board)

global directions
directions = [-11, -10, -9, -1, 1, 9, 10, 11]
global infinity
infinity = 99999999999999999999999999999999999

board = sys.argv[1]
player = sys.argv[2]
depth = 1
for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
  print(find_next_move(board, player, depth))
  depth += 1

class Strategy():
   logging = True  # Optional
   def best_strategy(self, board, player, best_move, still_running):
       depth = 1
       for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
           best_move.value = find_next_move(board, player, depth)
           depth += 1



results = []
with open("boards_timing.txt") as f:
   for line in f:
       board, token = line.strip().split()
       temp_list = [board, token]
       print(temp_list)
       for count in range(1, 7):
           print("depth", count)
           start = time.perf_counter()
           find_next_move(board, token, count)
           end = time.perf_counter()
           temp_list.append(str(end - start))
       print(temp_list)
       print()
       results.append(temp_list)
with open("boards_timing_my_results.csv", "w") as g:
   for l in results:
       g.write(", ".join(l) + "\n")