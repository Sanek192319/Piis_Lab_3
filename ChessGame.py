import chess
from evaluation import evaluate
class AIEngine:
    def __init__(self, board: chess.Board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color


    def negaMax(self, depth):
        bestMove = chess.Move.null()
        bestScore = float('-inf')
        if (depth == 0):
            return (evaluate(self.board), None)
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -1*(self.negaMax(depth - 1)[0])
            if score > bestScore:
                bestScore = score
                bestMove = move
            self.board.pop()
        return bestScore, bestMove


    def negaScout(self, depth, alpha, beta):
        bestMove = chess.Move.null()
        bestScore = float('-inf')
        if (depth == 0):
            return (evaluate(self.board), None)


        def getMaxScore(depth, alpha, beta):
            if (depth == 0):
                return evaluate(self.board)
            a = alpha
            b = beta
            i = 1

            for move in self.board.legal_moves:
                self.board.push(move)
                t = -1*(self.negaScout(depth - 1, -b, -alpha)[0])
                self.board.pop()
                if t > alpha and t < beta and i > 1 and depth < self.maxDepth - 1:
                    a = -1*(self.negaScout(depth - 1, -beta, -t)[0])
                a = max(a, t)
                if a >= beta:
                    return a
                b = a + 1
                i = i + 1
            return a

        for move in self.board.legal_moves:
            self.board.push(move)
            score = -1*(getMaxScore(depth-1, alpha, beta))
            self.board.pop()

            if score > bestScore:
                bestScore = score
                bestMove = move
    
        return (bestScore, bestMove)


    def pvs(self, depth, alpha, beta):
        bestMove = chess.Move.null()
        bestScore = float('-inf')
        if (depth == 0):
            return (evaluate(self.board), None)

        def getPVScore(depth, alpha, beta):
            if depth == 0:
                return evaluate(self.board)
            bSearchPv = True
            for move in self.board.legal_moves:
                self.board.push(move)
                if bSearchPv:
                    score = -1*(getPVScore(depth - 1, -beta, -alpha))
                else:
                    score = -1*(getPVScore(depth - 1, -alpha-1, -alpha))
                    if score > alpha and score < beta:
                        score = -1*(getPVScore(depth - 1, -beta, -alpha))
                self.board.pop()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
                    bSearchPv = False
            return alpha

        for move in self.board.legal_moves:
            self.board.push(move)
            score = -1*(getPVScore(depth-1, alpha, beta))
            self.board.pop()

            if score > bestScore:
                bestScore = score
                bestMove = move
    
        return (bestScore, bestMove)


class GameEngine:
    def __init__(self, board: chess.Board):
        self.board = board

    def playHumanMove(self):
        print("Possible moves: ", self.board.legal_moves)
        play = input("Enter your move: ")
        self.board.push_san(play)

    def playAIMove(self, maxDepth, color, method, alpha, beta):
        engine = AIEngine(self.board, maxDepth, color)

        if(method=='negamax'):
            bestMove = engine.negaMax(maxDepth)[1]

        elif(method=='negascout'):
            bestMove = engine.negaScout(maxDepth, alpha, beta)[1]

        else:
            bestMove = engine.pvs(maxDepth, alpha, beta)[1]
            
            
        print('BEST MOVE', bestMove)
        self.board.push(bestMove)
        return

    def startGame(self, method):
        aiColor = chess.BLACK
        print("The game started!")
        print("You play WHITE!")
        maxDepth = 3
        alpha = float('-inf')
        beta = float('inf')
        turn = chess.WHITE
        while (not self.board.is_checkmate()):
            print(self.board)
            if turn == chess.WHITE:
                print('\n\nWhite move\n\n')
                self.playHumanMove()
                turn = chess.BLACK
                continue
            if turn == chess.BLACK:
                print('\n\nBlack move\n\n')
                self.playAIMove(maxDepth, aiColor, method, alpha, beta)
                turn = chess.WHITE
                continue
        return

    
if __name__ == '__main__':
    game = GameEngine(chess.Board())
    print("Possible methods: negamax, negascout, pvs")
    method = input("Choose method: ")
    while True:
        if method != "negamax" and method != "negascout" and method != "pvs":
            print("Wrong method, try again")
            method = input("Choose method: ")
        else:
            break
    print("You choosed method", method)
    game.startGame(method)