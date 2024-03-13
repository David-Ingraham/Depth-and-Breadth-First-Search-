from __future__ import annotations
import random
from enum import Enum
from typing import NamedTuple

from Stack import *
from Queue import *

###########################################################
class Contents(str, Enum):
    ''' create an enumeration to define what the visual contents 
        of a Cell are; using str as a "mixin" forces all the entries
        to be strings; using an enum means no cell entry can be 
        anything other than the options here '''
    EMPTY   = " "
    START   = "◎"  # "S"
    GOAL    = "◆"  # "G"
    BLOCKED = "░"  # "X"
    PATH    = "★"  # "*"

    def __str__(self) -> str: return self.value

###########################################################
class Position(NamedTuple):
    ''' named tuple that allows us to use .row and .col rather 
        than the less-easy-to-read [0] and [1] for accessing 
        values'''
    row: int
    col: int

    def __str__(self) -> str: return f"({self.row},{self.col})"

###########################################################
class Cell:
    ''' class that allows us to use Cell as a data type -- 
        row, column, & cell contents '''
    __slots__ = ('_position', '_contents', '_parent')

    def __init__(self, row: int, col: int, contents: Contents, seen: bool)-> None:
        self._position: Position = Position(row, col)
        self._contents: Contents = contents
        self._parent:   Cell     = None
        self._seen: bool         = False

    def __str__(self) -> str:
        contents = "[EMPTY]" if self._contents == Contents.EMPTY else self._contents
        result = f"({self._position.row},{self._position.col}): {contents}"
        if self._parent is not None: 
            result += f"({self._parent._position.row}, {self._parent._position.col})"
        return result

    def getPosition(self) -> Position:    return self._position
    def getParent(self)   -> Cell | None: return self._parent

    def setParent(self, parent: Cell) -> None:  self._parent = parent 
    def markOnPath(self)              -> None:  self._contents = Contents.PATH

    def isBlocked(self) -> bool:  return self._contents == Contents.BLOCKED
    def isGoal(self)    -> bool:  return self._contents == Contents.GOAL

    def __eq__(self, other: Cell) -> bool:
        return self._position == other._position and \
               self._contents == other._contents and \
               self._parent   == other._parent
    

        
###########################################################
class Maze:
    __slots__ = ('_num_rows', '_num_cols', '_start', '_goal', '_grid')

    def __init__(self, num_rows: int = 10, num_cols: int = 10, \
                       start: Position = Position(0,0), \
                       goal:  Position = Position(9,9), \
                       proportion_blocked: float = 0.2, \
                       debug: bool = False) -> None:
        ''' Maze initializer method
        Parameters:
            num_rows:           number of rows in the grid
            num_cols:           number of columns in the grid
            start:              Position object indicating (row,col) of the start cell
            goal:               Position object indicating (row,col) of the goal cell
            proportion_blocked: proportion of cells to be blocked (between 0.0 and 1.0)
            debug:              whether to use one of the Maze examples from slides
        Raises:
            TypeError if proportion_blocked is not float
            TypeError if start of goal is not Position
            ValueError if proportion_blocked is outside (0,1)
        '''
        if not isinstance(proportion_blocked, float):
            raise TypeError("proportion_blocked argument must be a float")
        if proportion_blocked < 0 or proportion_blocked > 1:
            raise ValueError("proportion_blocked argument must be a float b/w 0 and 1")
        if not isinstance(start, Position) or not isinstance(goal, Position):
            raise TypeError("start and goal must both be Position objects")

        if debug:  # set up 6X5 maze example from course slides
            num_rows = 6; num_cols = 5;
            start = Position(5, 0)
            goal  = Position(0, 4)

        self._num_rows: int  = num_rows
        self._num_cols: int  = num_cols

        # set up the start and goal Cell objects
        self._start: Cell = Cell(start.row, start.col, Contents.START)
        self._goal:  Cell = Cell(goal.row,  goal.col,  Contents.GOAL)

        # create a 2D list of Cell objects, all initially empty
        self._grid: list[ list[Cell] ] = \
            [ [Cell(r,c, Contents.EMPTY) for c in range(num_cols)] \
              for r in range(num_rows) ]

        # overwrite the appropriate locations with the start and goal Cells
        self._grid[start.row][start.col] = self._start
        self._grid[goal.row][goal.col]   = self._goal

        if debug:
            # for example from slides
            blocked_cells = [(1,0),(1,3),(2,1),(2,4),(3,2),(5,1),(5,3),(5,4)]
            for pos in blocked_cells:
                p = Position(*pos)  # expand the pos tuple & pass to Position. the * before something itterable breaks it down to individula arguments 
                self._grid[p.row][p.col]._contents = Contents.BLOCKED
        else:
            # put blocks at random spots in the grid, using given proportion

            options: list[Cell] = [cell for row in self._grid for cell in row]

            options.remove(self._start)
            options.remove(self._goal)

            how_many:int = int((num_rows * num_cols -2) * proportion_blocked)

            blocked: list[Cell] = random.sample(options,k= how_many) #radnom selction of cells to block from our 1d list of cells

            for cell in blocked:
                cell._contents = Contents.BLOCKED #this only chnages the grid data becuase the cell class is mutable. blcoked and grid point to same memeory address, to changing things in blocked chnages things in grid becuase they are pointing at the same things we are ultamtley changin. which is the object at a memory address both point ot the same memeory address
            pass

    def __str__(self) -> str:
        ''' creates a str version of the Maze, showing contents, with cells
            delimited by vertical pipes
        Returns:
            a str representation of the Maze
        '''
        maze_str = ""
        for row in self._grid:  # row : list[Cell]
            maze_str += "|" + "|".join([cell._contents for cell in row]) + "|\n"
        return maze_str[:-1]  # remove the final \n
    


    def getStart(self) -> Cell: return self._start 

    def getGoal(self) -> Cell: return self._goal


    def showPath(self: Maze, goal: Cell) -> None:
        path =[]
        cell = goal
        while cell._parent is not None:
            path.append(cell)
            cell = cell._parent

        path.append(cell)
        assert(cell == self._start)

        path.reverse()

        for cell in path:
            if cell not in [self._goal, self._start]:
                cell.markOnPath()

        print(self) #pirnting newly marked up maze with the path shown 

    def getSearchLocations(self, cell: Cell)-> list[Cell]:
        current_cell = cell.getPosition()
        res = []
        res.append(self._grid[current_cell.row-1][current_cell.col])
        res.append(self._grid[current_cell.row+1][current_cell.col])
        res.append(self._grid[current_cell.row][current_cell.col+1])
        res.append(self._grid[current_cell.row][current_cell.col-1]) 


        
        for cell in res:
            if cell._seen == True | cell.isBlocked == True :
                res.remove(cell)


        return res


    def depth_first_search(self) -> Cell | None:
        #adding cells to the stack in clockwise order, starting from upCell
        #if cell is avalible and not seen, added to stack
        #last cell to be added is the chosen cell
        #the chosen cell's contents are updated to path and 


        stack = Stack()

        cells: list = Maze.getSearchLocations()

        for cell in cells:
            stack.push(cell)

        

        




        pass

###########################################################
def main() -> None:

    #m = Maze(debug = True)
    
    m = Maze(debug = True)
    print(m)

    m._grid[0][4]._parent = m._grid[0][3]
    m._grid[0][3]._parent = m._grid[0][2]
    m._grid[0][2]._parent = m._grid[0][1]
    m._grid[0][1]._parent = m._grid[0][0]

    print(m.getSearchLocations(m._grid[0][1]))
    m._grid[0][0]._parent = m._grid[1][0]
    m._grid[1][0]._parent = m._grid[2][0]
    m._grid[2][0]._parent = m._grid[3][0]
    m._grid[3][0]._parent = m._grid[4][0]
    m._grid[4][0]._parent = m._grid[5][0]


    print()
    m.showPath(m._goal)

    print()






    '''
    start = Cell(0,0, Contents.START)
    goal  = Cell(9,9, Contents.GOAL)
    empty = Cell(4,4, Contents.EMPTY)
    block = Cell(2,2, Contents.BLOCKED)
    path  = Cell(9,8, Contents.PATH)

    for c in [start,goal,empty,block,path]:
        print(c)
    print('-' * 40)

    print(f"before: {empty}")
    empty.markOnPath()
    print(f"after:  {empty}")


    print('-' * 40)

    for c in Contents:
        print(c)
    print('-' * 40)

    p1 = Position(3,4)
    p2 = Position(9,8)
    p3 = (7,7)

    print(f"row for p1 is: {p1.row}")
    print(f"col for p1 is: {p1.col}")
    print(f"row for p3 is: {p3[0]}")
    print(f"col for p3 is: {p3[1]}")
    print(f"p2 is: {p2}")
    '''


if __name__ == "__main__":
    main()
