"""SinkOrSail v. 1.0.0

Copyright (c) 2014 Joshua Moore_
"""

import random
from collections import deque


#Exception classes: _Error, OOBError, InputError, OverlapError
class _Error(Exception):
    """Base class for exceptions in this module."""
    pass


class OOBError(_Error):
    """Raised when value entered is outside of the board limits."""

    
class InputError(_Error):
    """Raised when user input is unanticipated value or type."""


class OverlapError(_Error):
    """Raised when Points overlap on a Board."""


#Object classes: Board, Point, Ship, Player, AI
class Board(object):
    """A Board object is a 10x10 grid representing the game board.

    Board width and height are set to 10.  References to these attributes
    are used throughout the module in lieu of the integer 10 to
    facilitate later forks using different size boards and fleet sizes.
    
    Instance attributes:
        name (string)
        width (integer)
        height (integer)
        grid (nested list of strings)
        content (list of Ship objects)
    """
    
    def __init__(self, name="Board"):
        """Initializes a Board object."""
        self.name = name
        self.width = 10
        self.height = 10
        self.grid = [["~" for x in range(self.width)]
                     for y in range(self.height)]
        self.content = [] #stores pointers to all Ship objects on board

    def __repr__(self):
        """Returns a string of board.name and a labelled board.grid."""
        x_label = (
            "A", "B", "C", "D", "E",
            "F", "G", "H", "I", "J"
            )
        name_string = "\n" + self.name + "\n"
        grid_string = "  " + " ".join(x_label[:self.width]) + "\n"
        for y, row in enumerate(self.grid):
            grid_string += str(y) + " " + " ".join(row) + "\n"           
        grid_string += "Ships Afloat: {}\n".format(len(self.content))
        board_string = name_string + grid_string
        return board_string

    def isoverlap(self, point):
        """Return True if point in ship in self.content. Else, return False."""
        for ship in self.content:
            if (point in ship.ext) or (point in ship.buffer):
                return True
        return False

    def inline(self, h1, h2):
        """Returns a list of four Points in line with h1 and h2.

        Specifically, the first two Points in the list are the next
        two Points on a ray with h1 as the initial point and
        extended through h2.  The latter two points are the next two
        Points on a ray with h2 as the initial point and extended
        through h1.  If h1 == h2, an empty list is returned.
        """
        
        line = []
        if h1.x == h2.x:
            if h1 < h2:
                for i in range(1, 3):
                    if h2.y + i < self.height:
                        try:
                            line.append(Point(self, h2.x, h2.y + i))
                        except OOBError:
                            break
                for i in range(1, 3):
                    if h1.y - i >= 0:
                        try:
                            line.append(Point(self, h1.x, h1.y - i))
                        except OOBError:
                            break
            elif h1 > h2:
                for i in range(1, 3):
                    if h2.y - i >= 0:
                        try:
                            line.append(Point(self, h2.x, h2.y - i))
                        except OOBError:
                            break
                for i in range(1, 3):
                    if h1.y + i < self.height:
                        try:
                            line.append(Point(self, h1.x, h1.y + i))
                        except OOBError:
                            break
        elif h1 < h2:
            for i in range(1, 3):
                if h2.x + i < self.width:
                    try:
                        line.append(Point(self, h2.x + i, h2.y))
                    except OOBError:
                        break
            for i in range(1, 3):
                if h1.x - i >= 0:
                    try:
                        line.append(Point(self, h1.x - i, h1.y))
                    except OOBError:
                        break
        elif h1 > h2:
            for i in range(1, 3):
                if h2.x - 1 >= 0:
                    try:
                        line.append(Point(self, h2.x - i, h2.y))
                    except OOBError:
                        break
            for i in range(1, 3):
                if h1.x + i < self.width:
                    try:
                        line.append(Point(self, h1.x + i, h1.y))
                    except OOBError:
                        break
        return line
                    
    def place_ship(self, point, direction="down", order=0):
        """Method for placing Ship objects on a Board instance.

        This method is invoked by Player.generate_fleet() and
        AI.generate_fleet() to facilitate the initialization of
        10 Ships of the proper type and number.
        """
        
        if order > 5:
            s = Ship(self, point)
        elif (order < 6) and (order > 2):
            s = Ship(self, point, direction, "destroyer")
        elif (order == 1) or (order == 2):
            s = Ship(self, point, direction, "cruiser")
        else:
            s = Ship(self, point, direction, "battleship")
        return s
    
    def rand_point(self):
        """Initializes a Point at random coordinates on self."""
        rdgen = random.Random()
        x = rdgen.randrange(self.width)
        y = rdgen.randrange(self.height)
        return Point(self, x, y)
    
    def rand_ship(self, order=0):
        """Initializes a Ship with a random starting point and direction."""
        point = self.rand_point()
        direction = rand_direction()
        s = self.place_ship(point, direction, order)
        return s


class Point(object):
    """Represents a location on a Board's grid.

    Instance attributes:
        x (integer)
        y (integer)
        board (Board object)
    """
    
    #Dictionary for column letter-index conversions:
    row_keys = {
        "A": 0, "B": 1, "C": 2, "D": 3, "E": 4,
        "F": 5, "G": 6, "H": 7, "I": 8, "J": 9,
        0: "A", 1: "B", 2: "C", 3: "D", 4: "E",
        5: "F", 6: "G", 7: "H", 8: "I", 9: "J"
        }

    def __init__(self, board, x, y):
        """Initializes a Point object on board with coordinates (x, y).

        Note that (x, y) is used to mirror standard geometric notation,
        not to imply the use of a tuple.  Raises OOBError if x or y are
        outside the range of the board.
        """
        
        if (x < board.width and y < board.height) and (x >= 0 and y >= 0):
            self.x = x
            self.y = y
            self.board = board
        else:
            raise OOBError

    def __repr__(self):
        return "{}{}".format(Point.row_keys[self.x], self.y)

    def __str__(self):
        return "{}{}".format(Point.row_keys[self.x], self.y)

    def __lt__(self, other):
        """Defines the < operator for Point objects.

        Two Points p and q satisfy p < q if and only if p.x < q.x or
        p.x == q.x and p.y < q.y.
        """
        
        if self.x == other.x:
            if self.y < other.y:
                return True
        elif self.x < other.x:
            return True
        return False

    def __le__(self, other):
        """Defines the <= operator

        Two Points p and q satisfy p <= q if and only if p > q is False.
        """
        
        if not (self > other):
            return True
        return False

    def __eq__(self, other):
        """Defines the == operator for Point objects.

        Two Points p and q satisfy p == q if and only if p.x == q.x and
        p.y == q.y.
        """
        
        if (self.x == other.x) and (self.y == other.y):
            return True
        return False

    def __ne__(self, other):
        """Defines the != operator for Point objects.

        Two Points p and q satisfy p != q if and only if p == q is False.
        """
        
        if not (self == other):
            return True
        return False

    def __gt__(self, other):
        """Defines the > operator for Point objects.

        Two Points p and q satisfy p > q if and only if p.x > q.x or
        p.x == q.x and p.y > q.y.
        """
        
        if self.x == other.x:
            if self.y > other.y:
                return True
        elif self.x > other.x:
            return True
        return False

    def __ge__(self, other):
        """Defines the >= operator

        Two Points p and q satisfy p >= q if and only if p < q is False.
        """
        
        if not (self < other):
            return True
        return False

    def adj_pts(self):
        """Returns a list points adjacent to self.

        Adjacent is defined as horizontally or vertically adjacent.  Diagnal
        is not considered adjacent in this module.
        """
        
        adj = []
        if (self.y + 1) < self.board.height: 
            adj.append(Point(self.board, self.x, self.y + 1)) #down
        if self.y > 0: 
            adj.append(Point(self.board, self.x, self.y - 1)) #up
        if (self.x + 1) < self.board.width: 
            adj.append(Point(self.board, self.x + 1, self.y)) #right
        if self.x > 0: 
            adj.append(Point(self.board, self.x - 1, self.y)) #left
        return adj

    def display(self, symbol):
        """Alters board.grid to display self as symbol; no return value."""
        self.board.grid[self.y][self.x] = symbol


class Ship(object):
    """Ship objects are game pieces occupying space on the board.
    
    Instance attributes:
        ext (list of Points)
        valid (list of Points)
        buffer (list of Points)
        board (Board)
        symbol (string)
        kind(string)
    """
    
    def __init__(self, board, point, direction="down", kind="submarine"):
        """Initializes a Ship object and appends it to board.content.

        Raises OverlapError if any Point in the new Ship is equivalent
        to any Point in the board's other Ships or their buffers.
        Raises InputError if argument passed to direction is invalid or
        if argument passed to kind is invalid."""
        self.board = board
        direct = {"down", "up", "left", "right"}
        length = {
            "battleship": 4, "cruiser": 3,
            "destroyer": 2, "submarine": 1
            }
        if (direction not in direct) or (kind not in length):
            raise InputError
        self.kind = kind
        if kind == "submarine":
            self.symbol = "S"
        if kind == "destroyer":
            self.symbol = "D"
        if kind == "cruiser":
            self.symbol = "C"
        if kind == "battleship":
            self.symbol = "B"
        if direction == "down":
            self.ext = [Point(self.board, point.x, point.y + n)
                        for n in range(length[self.kind])]
            
        if direction == "up":
            self.ext = [Point(self.board, point.x, point.y - n)
                        for n in range(length[self.kind])]
            
        if direction == "right":
            self.ext = [Point(self.board, point.x + n, point.y)
                        for n in range(length[self.kind])]
            
        if direction == "left":
            self.ext = [Point(self.board, point.x - n, point.y)
                        for n in range(length[self.kind])]
        #Confirm that the new Ship is neither adjacent to nor
        #overlapping other Ships on board.
        for p in self.ext:
            if self.board.isoverlap(p):
                raise OverlapError
        
        self.ext.sort()
        self.valid = self.ext.copy()
        buffer = []
        if direction in {"right", "left"}:
            if self.ext[0].x > 0:
                left_of = Point(self.board, self.ext[0].x - 1, point.y)
                buffer.append(left_of)
                
            if point.y > 0:
                parallel_above = [Point(self.board, p.x, p.y - 1) for
                                  p in self.ext]
                buffer.extend(parallel_above)
                    
            if (point.y + 1) < self.board.height:
                parallel_below = [Point(self.board, p.x, p.y + 1) for
                                  p in self.ext]
                buffer.extend(parallel_below)
                    
            if (self.ext[-1].x + 1) < self.board.width:
                right_of = Point(self.board, self.ext[-1].x + 1, point.y)
                buffer.append(right_of)

        else: #If direction in {"down", "up"}:
            if self.ext[0].y > 0:
                above = Point(self.board, point.x, self.ext[0].y - 1)
                buffer.append(above)
                
            if point.x > 0:
                parallel_left = [Point(self.board, p.x - 1, p.y) for
                                 p in self.ext]
                buffer.extend(parallel_left)
                    
            if (point.x + 1) < self.board.width:
                parallel_right = [Point(self.board, p.x + 1, p.y) for
                                  p in self.ext]
                buffer.extend(parallel_right)
                    
            if (self.ext[-1].y + 1) < self.board.height:
                below = Point(self.board, point.x, self.ext[-1].y + 1)
                buffer.append(below)
                
        self.buffer = buffer
        self.board.content.append(self)

    def __repr__(self):
        ship_string = "{} at {}".format(self.kind, str(self.ext))
        return ship_string
            
    def display(self):
        """Displays Ship's location on self.board."""
        for p in self.ext:
            p.display(self.symbol)

    def display_buffer(self, symbol="#"):
        """Displays Ship's buffer on self.board."""
        for p in self.buffer:
            p.display(symbol)

            
class Player(object):
    """An interface between the end-user and the user's game board."""
    def __init__(self):
        your_name = input("Enter your name: ")
        self.board = Board(name=your_name)
        self.guesses = []

    def input_point(self, board, prompt="Enter point (ex. A4): "):
        """Prompts user to input a point.

        Loops until a valid point is entered."""
        
        while True:
            response = input(prompt)
            if len(response) < 2:
                print("Invalid input.")
                continue
            x_string = response[0].upper()
            y_string = response[1]
            if (x_string.isalpha() and y_string.isnumeric() and
                x_string in Point.row_keys):
                x = Point.row_keys[x_string]
                y = int(y_string)
            else:
                print("Invalid input.")
                continue
            if (x >= board.width or y >= board.height) or (x < 0 or y < 0):
                print("Out of bounds.")
                continue
            point = Point(board, x, y)
            return point


    def input_direction(self):
        """Prompts the user to input a direction.

        Loops until a valid direction is entered."""
        
        valid_directions = {"down", "up", "right", "left"}
        while True:
            direction = input("Enter direction: ")
            if direction not in valid_directions:
                print("Input must be one of the following: ",
                      valid_directions)
                continue
            return direction
        
    def generate_fleet(self):
        """Places 10 ships according to user input.

        Iterates ten times, using user input to produce one battleship,
        two cruisers, three destroyers, and four submarines.
        """
        
        height = self.board.height
        width = self.board.width
        for i in range(10):
            print(self.board)
            if i > 5:
                print("Place your submarine! (1x1)")
            elif (i < 6) and (i > 2):
                length = 2
                print("Place your destroyer! (2x1)")   
            elif (i == 1) or (i == 2):
                length = 3
                print("Place your cruiser! (3x1)")
            else:
                length = 4
                print("Place your battleship! (4x1)")

            while True:
                point = self.input_point(self.board)
                if self.board.isoverlap(point):
                    print("Ship Overlap. Try Again.")
                    continue
                if i < 6:
                    direction = self.input_direction()
                    if (direction == "down") and (point.y+length >= height):
                        print("Extension Out of Bounds. Try Again.")
                        continue
                    elif (direction == "right") and (point.x+length >= width):
                        print("Extension Out of Bounds. Try Again.")
                        continue
                    elif (direction == "up") and (point.y-length < 0):
                        print("Extension Out of Bounds. Try Again.")
                        continue
                    elif (direction == "left") and (point.x-length < 0):
                        print("Extension Out of Bounds. Try Again.")
                        continue
                    try:
                        s = self.board.place_ship(point, direction, order=i)
                    except OverlapError:
                        print("Ship Overlap. Try Again.")
                        continue
                else:
                    try:
                        s = self.board.place_ship(point, order=i)
                    except OverlapError:
                        print("Ship Overlap. Try Again.")
                        continue
                s.display()
                s.display_buffer()
                break
        for s in self.board.content:
            s.display_buffer("~")
                    

    def input_guess(self, ai):
        while True:
            gs = self.input_point(board=ai.board,
                                  prompt="Enter Guess (ex. A4)")
            if gs in self.guesses:
                print("You've already guessed there. Try again.")
                continue
            self.guesses.append(gs)
            break    
        self.check_guess(gs)

    def check_guess(self, guess):
        """Compares guess with ships on board.

        If guess is a hit, removes ship from board.content.
        The guess argument should be a Point object.
        """
        
        for ship in guess.board.content:
            if guess in ship.valid:
                guess.display("X")
                print(guess.board)
                ship.valid.remove(guess)
                print("{} hits opponent's {}!".format(guess, ship.kind))
                if len(ship.valid) == 0:
                    guess.board.content.remove(ship)
                    print("You sank opponent's {}!".format(ship.kind))
                    print(guess.board)
                return True
        guess.display(" ")
        print(guess.board)
        print("{} missed opponent's fleet.".format(guess))
        return False
        

class AI(object):
    """Contains AI Ship placement and guess-related methods."""
    def __init__(self, name="Opponent"):
        """An AI object has attributes for memory and decision making.

        Instance attributes:
            name (string)
            board (Board)
            guesses (list of Points): Contains prohibited guesses; populated
                by past guesses and the buffers of sunken Ships.
            combo (list of Points): Contains previous hits; cleared when a
                Ship is sunken.
            adj_guide (deque of Points): Contains Points adjacent to last hit;
                used to refine guesses after first hit.  Cleared when a ship
                is sunken.
            guide (deque of Points): Contains Points on a ray in front of and
                behind first two hits on a Ship.  Cleared when a Ship is
                sunken.   
        """
        
        self.name = name
        self.board = Board(self.name)
        self.guesses = []
        self.combo = []
        self.adj_guide = deque([])
        self.guide = deque([])
          
    def generate_fleet(self):
        for i in range(10):
            while True:
                try:
                    self.board.rand_ship(order=i)
                except (OverlapError, OOBError):
                    continue
                break

    def random_guess(self, player):
        while True:
            gs = player.board.rand_point()
            if gs in self.guesses:
                continue
            else:
                break
        return gs

    def make_guess(self, player):
        """Decides a point to guess."""
        if self.guide:
            # If a guessing strategy has been formed, follow it.
            gs = self.guide.popleft()
            self.guesses.append(gs)
            return gs
        elif self.combo:
            # If an enemy ship has been hit.
            if (len(self.combo) == 1) and not self.adj_guide:
                # If a list of adjacent points has not been generated, do so.
                adj = self.combo[-1].adj_pts()
                for p in adj:
                    if p in self.guesses:
                        adj.remove(p)
                self.adj_guide.extend(adj)
                rg = random.Random()
                n = rg.randrange(len(self.adj_guide))
                self.adj_guide.rotate(n)
            if len(self.combo) == 1:
                # Target a space adjacent to last hit.
                gs = self.adj_guide.pop()
            elif len(self.combo) == 2:
                # If an enemy ship has been hit twice, form a strategy that
                # targets the next two spaces in line with past hits, then
                # two the two spaces in line behind the last two hits.
                line = player.board.inline(self.combo[-2], self.combo[-1])
                for p in line[:]:
                    if p in self.guesses:
                        line.remove(p)
                self.guide.extend(line)
                gs = self.guide.popleft()
            else:
                # A catch-all in case there is a hole in the above logic.
                print("Wait, what just happened in make_guess?")#debug info
            self.guesses.append(gs)
            return gs
        else:
            # If an enemy ship has not been hit since the beginning or since
            # the last enemy ship was sunk, guess a random space.
            gs = self.random_guess(player)
            self.guesses.append(gs)
        return gs

    def check_guess(self, guess):
        """Compares guess with ships on board.

        The guess argument should be a Point object on the player board.
        """
        
        for ship in guess.board.content:
            if guess in ship.valid:
                # If guess hits ship:
                print("{} hit your {}!".format(guess, ship.kind))
                guess.display("X")
                ship.valid.remove(guess)
                self.combo.append(guess)
                if not ship.valid:
                    # If hit sinks ship, reset guess refinement attributes
                    # and append ship's all adjacent Points to self.guesses.
                    guess.board.content.remove(ship)
                    print("Your {} has been sunk!".format(ship.kind))
                    for p in ship.buffer:
                        if p not in self.guesses:
                            self.guesses.append(p)
                    self.combo.clear()
                    self.guide.clear()
                    self.adj_guide.clear()
                print(guess.board)
                return True
        # If guess misses enemy fleet:
        if self.guide:
            # Rotating the guide left after a miss switches the direction of
            # future guesses popped from guide.
            self.guide.rotate(-1)
        print("{} missed your fleet.".format(guess))
        guess.display(" ")
        print(guess.board)
        return False

    def guess(self, player):
        gs = self.make_guess(player)
        print("{} guesses {}".format(self.name, gs))
        self.check_guess(gs)



def rand_direction():
    """Randomly returns one of four cardinal direction as a string."""
    directions = ("down", "up", "right", "left")
    rdgen = random.Random()
    num = rdgen.randrange(4)
    direction = directions[num]
    return direction


def main():
    while True:
        print("## _##############\n" + 
              "##|_  | |\ | |/###\n" + 
              "## _| | | \| |\###\n" + 
              "##########_#######\n" + 
              "######/\ |_)######\n" + 
              "##### \/ | \######\n" + 
              "##_###__##########\n" + 
              "#|_  |__| | |  ###\n" + 
              "# _| |  | | |__###\n" + 
              "##################\n"
              )
        print("1. Play\n2. Quit")
        opt = input(":::")
        if (opt == "1") or ("p" in opt.lower()):
            play_loop()
        elif (opt == "2") or ("q" in opt.lower()):
            break

        
def play_loop():
    ai = AI()
    ai.generate_fleet()
    player = Player()
    player.generate_fleet()
    iteration = 0
    while True:
        iteration += 1
        print("Round: ", iteration)
        print(ai.board)
        player.input_guess(ai)
        input("<Press Enter>\n-------------")
        if len(ai.board.content) == 0:
            print("Winner!")
            break
        
        ai.guess(player)
        input("<Press Enter>\n-------------")
        if len(player.board.content) == 0:
            print(player.board)
            print("You Lose.")
            break


if __name__ == "__main__":
    main()
