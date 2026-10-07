from enum import Enum

class Color(Enum):
    WHITE = "WHITE"
    BLACK = "BLACK"

class Side(Enum):       #Enum necesario para la funcion de enroque
    RIGHT = "RIGHT" 
    LEFT = "LEFT"

class MatchState(Enum):
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    WAITING = "WAITING" #Estado nuevo necesario para la logica de start match
    WAITING_PROMOTION = "WAITING_PROMOTION"  

class PromotingType(Enum):
    KNIGHT = "KNIGHT"
    ROOK = "ROOK"
    QUEEN = "QUEEN"
    BISHOP = "BISHOP" 