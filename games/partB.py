# Main Author: Wilgard Fils-aime , Jaehyuk Heo
# Main Reviewer:Ziyang Wang

import partD
import partC

# This function duplicates and returns the board. You may find this useful
def copy_board(board):
        current_board = []
        height = len(board)
        for i in range(height):
            current_board.append(board[i].copy())
        return current_board


# this function is your evaluation function for the board
def evaluate_board (board, player):
    score = 0
    height = len(board)
    width  = len(board[0])
    
    #check for winning conditions
    for i in range(height):
        for j in range(width):
            cell_value = board[i][j]
            score += cell_value

    #Adjusting score for winning or losing situations
    #e.g: if a player has a winning configuration, boost or reduce the score
    if is_winning(board, player):
        return float('inf') 
    elif is_winning(board, -player):
        return float('-inf') 
    
    if sign(player) != sign(score): # another player is leading the score
        return score if player == 1 else -score
    else:
        return abs(score)

# we will use player sign to determine cell color
# win means all cells are with same sign
# a win is when all cells of the board are with same sign/color
def is_winning(board, player):
    height = len(board)
    width = len(board[0])

    for i in range(height):
        for j in range(width):
            if board[i][j] != 0 and (sign(board[i][j]) != sign(player)):
                return False  # not winning as long as one cell is with different sign

    return True


def sign(a):
    return (a > 0) - (a < 0)


class GameTree:
    class Node:
        def __init__(self, board, depth, player, move, tree_height = 4):
            self.board = copy_board(board)
            self.depth = depth
            self.player = player
            self.children = []
            self.move = move
            if depth < tree_height-1 and not is_winning(board, player) and not is_winning(board, -player):  
                # max depth = height -1
                # nodes with max depth do not need to expend, they should be the leaf nodes
                self.expand(tree_height)
                
        def expand(self, tree_height):
            next_player = -1 if self.player == 1 else 1
            for move in self.get_legal_moves(self.board, self.player):
                new_board = self.make_move(copy_board(self.board), move, self.player)
                child_node = GameTree.Node(new_board, self.depth + 1, next_player, move, tree_height)
                self.children.append(child_node)
                

        def get_legal_moves(self, board, player):
            height = len(board)
            width = len(board[0])
            moves = []
            for i in range(height):
                for j in range(width):
                    if board[i][j] == 0 or  sign(board[i][j]) == sign(player): 
                        # 0 represent an empty cell
                        # can place gem into an empty cell, or a cell already has gem on it
                        moves.append((i, j))
                    
            return moves


        def make_move(self, board, move, player):
            board[move[0]][move[1]] += player  # place one more gem on that cell
            if a1_partd.get_overflow_list(board): 
                newQueue = a1_partc.Queue()
                a1_partd.overflow(board, newQueue)
                board = newQueue.get_back()
            return board


    def __init__(self, board, player, tree_height = 4):
        self.player = player
        self.board = copy_board(board)
        self.tree_height = tree_height
        self.root = self.Node(self.board, 0 , 1*self.player, (0,0),  tree_height)
        # you will need to implement the creation of the game tree here.  After this function completes,
        # a full game tree will be created.
        # hint: as with many tree structures, you will need to define a self.root that points to the root
        # of the game tree.  To create the tree itself, a recursive function will likely be the easiest as you will
        # need to apply the minimax algorithm to its creation.


    def minimax(self, node):
        if  len(node.children) == 0 or is_winning(node.board, node.player) or is_winning(node.board, -node.player):
            node.score= evaluate_board(node.board, self.player)
            return node.score

        evenLevel = (node.depth +1 % 2) == 0
        if evenLevel:
            max_eval = float('-inf')
            for child in node.children:
                eval = self.minimax(child)
                max_eval = max(max_eval, eval)
            node.score = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for child in node.children:
                eval = self.minimax(child)
                min_eval = min(min_eval, eval)
            node.score = min_eval
            return min_eval

    def get_move(self):
        self.minimax(self.root)
        best_move = None
        best_score = float('-inf')
        
        for child in self.root.children:
            
            if child.score > best_score:
                best_score = child.score
                best_move = child.move
        return best_move

    def clear_tree(self):

        def unlink_nodes(node):
            for child in node.children:
                unlink_nodes(child)
            node.children = []

        unlink_nodes(self.root)
        self.root = None
        
    
