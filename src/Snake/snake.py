#Add upper directory path
import sys,os
paths = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))
sys.path.insert(0,paths)
defaults_path = os.path.join(paths,"defaults/snake.json")


#Other important imports
import json,random,math
from src.Maps import maps #Importing the Map class from maps.py

#Dictionary + List storing directions possible
directions_dict = {"LEFT":(0,-1),"RIGHT":(0,1),"UP":(-1,0),"DOWN":(1,0)}
directions_list = ["LEFT","RIGHT","UP","DOWN"]


#Just adds 2 tuples dude
def add_tuples(a,b):
    c = []
    for i in range(len(a)):
        c.append(a[i] + b[i])
    return tuple(c)


#Multiplies the tuple a with number b
def mul_tuple(a,b):
    a = list(a)
    for i in range(len(a)):
        a[i]=int(a[i]*b)
    return tuple(a)


#Gets difference between 2 tuples but note that they should have either same row or same column
def diff_tuples(a,b):
    if a[0]==b[0]:
        return math.fabs(b[1] - a[1])
    elif a[1]==b[1]:
        return math.fabs(b[0] - a[0])
    else:
        raise ValueError("Differentiating tuples are not having any value in common")
    return None

#Class representing each
class Snake:
    """Class representing a snake on a particular map ! Requires a map object to be linked !\n
    Has the following functions:-\n
    1)fetch_direction(current_location,ftemp) - Requires list of locations to choose from and returns the direction\n
    2)get_snakepos_random() - Requires a map object and fills the location list with a random snake position on the map\n
    3)move() - Moves the snake by 1 position\n
    4)check() - Checks if the snake is in disallowed sections(its own body or the border/restricted blocks)"""
    def __init__(self,snake_length,map):
        #Checks if map is an object of Map class
        if not isinstance(map,maps.Map):
            raise TypeError("Should supply a Map object :)")

        self.move_allowed = True
        self.map = map
        self.length = int(snake_length)
        self.locations = [] #Stores the beginning,end and breakpoints of the snake's body,i.e. (2,3),(2,1)
        self.direction = None
        self.direction_pt = None
        self.keep_track_length = 0
        a = self.get_snakepos_random() #Initialize location of snake on map
        if a!=True:
            print(a)

    def fetch_direction(self,current_location,ftemporary):
        """Requires a list of locations from which it chooses randomly and returns the direction for the snake"""
        chosen_block = random.choice(ftemporary)
        if chosen_block == add_tuples(current_location,directions_dict["DOWN"]):
            return directions_list[2] #Returns "UP" opposite
        elif chosen_block == add_tuples(current_location,directions_dict["UP"]):
            return directions_list[3] #Returns "DOWN"
        elif chosen_block == add_tuples(current_location,directions_dict["LEFT"]):
            return directions_list[1] #Returns "RIGHT"
        elif chosen_block == add_tuples(current_location,directions_dict["RIGHT"]):
            return directions_list[0] #Returns "LEFT"
        else:
            raise ValueError("Couldn't find snake object direction !") #JUST IN CASE
            return None

    def get_snakepos_random(self):
        """Randomly assigns location to the snake ! Called during initialization of the game"""

        #Checks if map is an object of Map class
        if not isinstance(self.map,maps.Map):
            raise TypeError("Should supply a Map object :)")
            return None

        #Member function of map for getting allowed locations in the form of (1,2) (row, column)
        allowed_locations = self.map.get_allowed_locations()
        if len(allowed_locations)<1:
            raise ValueError("Map data incorrectly supplied")
            return None

        #Just to store where the last breakpoint(could be head) points to
        temp_direction = None
        temp_direction_pt = None

        if self.length<3:
            raise ValueError("Minimum length for the snake is 3 blocks !")
            return None

        #Loops for every body part of snake
        for i in range(self.length):

            #What if it's the head! We need to randomize the location and also set the direction
            if len(self.locations) == 0:
                ftemp = [] #Stores temporary possible locations
                max_tries = 10 #Just to prevent infinite loop
                trial = 0
                while (len(ftemp)<3):
                    trial+=1
                    if trial>max_tries:
                        raise OverflowError("Taking too long to find perfect location on map for spawning snake ")
                        return None

                    #Reset in case loop continues
                    self.locations = []
                    self.locations.append(random.choice(allowed_locations))
                    #Hard-coded for 2-dimensional tuple
                    #ftemp initially stores all the 4 up,down,left,right locations
                    ftemp = [add_tuples(self.locations[0],(1,0)),add_tuples(self.locations[0],(0,1)),add_tuples(self.locations[0],(-1,0)),add_tuples(self.locations[0],(0,-1))]
                    ftemp = [a for a in ftemp if a in allowed_locations] #Stores allowed locations (max:4)
                    #Now ftemp has locations of all 4 directions that are allowed on the map passed to the Snake object
                if ftemp==[]:
                    raise ValueError("Couldn't find matching allowed locations on the map for the snake to spawn")
                    return None

                #This line is to eliminate the locations whose opposite isn't present ! like remove the UP location if DOWN isn't there
                #It is done to ensure that the snake has scope of movement in both directions
                ftemp = [c for c in ftemp if add_tuples(c,(2,0)) in ftemp or add_tuples(c,(-2,0)) in ftemp or add_tuples(c,(0,2)) in ftemp or add_tuples(c,(0,-2)) in ftemp]
                if len(ftemp)<2: #Just in Case there is none (0% chances though cause of above loop)
                    raise ValueError("Final Temporary list got less expected values for spawning positions")
                    return None

                #Fetching direction and also the points to be added later
                temp_direction = self.direction = self.fetch_direction(self.locations[0],ftemp)
                if self.direction == None:
                    raise ValueError("Direction can't be None ! fetch_direction() returned None")
                    return None
                temp_direction_pt = self.direction_pt = directions_dict[self.direction]

                #These temp direction ones will be used later in order to remember the direction of the last stored breakpoint
            else:
                #Just in Case
                if self.direction == None:
                    raise ValueError("No direction for the snake :)")
                    return None

                #The next position to suspect based on the temporary direction of last breakpoint
                next_pos = add_tuples(self.locations[-1],mul_tuple(temp_direction_pt,-(i - self.keep_track_length)))

                #The current position ! That's it
                current_pos = add_tuples(self.locations[-1],mul_tuple(temp_direction_pt,-(i - self.keep_track_length)+1))
                if (next_pos in allowed_locations) and (next_pos not in self.locations): #If the next position is even possible
                    if i == self.length-1: #If it's the tail
                        #NOTE: self.locations stores the beginning,end and breakpoints only
                        self.locations.append(next_pos)
                    else:
                        #It's just the body
                        pass
                else:
                    #What if there's a breakpoint
                    self.locations.append(current_pos)  #Added Breakpoint
                    self.keep_track_length += diff_tuples(self.locations[-1],self.locations[-2]) #Keeps track of the length before the last breakpoint

                    #Storing all possible positions for the snake after the breakpoint (Use ur mind, you will know that there can be max 2)
                    temp_nextpos_possible = (add_tuples(current_pos,(temp_direction_pt[1],temp_direction_pt[0])),add_tuples(current_pos,(-temp_direction_pt[1],-temp_direction_pt[0])))
                    temp_nextpos_possible = [a for a in temp_nextpos_possible if a in allowed_locations]

                    #Store the direction and direction_pt for this breakpoint
                    temp_direction = self.fetch_direction(current_pos,temp_nextpos_possible)
                    temp_direction_pt = directions_dict[temp_direction]
        return True

    def move(self):
        if not self.move_allowed:
            print("Move Restricted")
            return None
        self.locations[0] = add_tuples(self.locations[0],self.direction_pt)
        if (self.locations[-1][0] == self.locations[-2][0]):
            if (self.locations[-1][1]>self.locations[-2][1]):
                self.locations[-1] = add_tuples(self.locations[-1],(0,-1))
            else:
                self.locations[-1] = add_tuples(self.locations[-1],(0,1))
        elif (self.locations[-1][1] == self.locations[-2][1]):
            if (self.locations[-1][0]>self.locations[-2][0]):
                self.locations[-1] = add_tuples(self.locations[-1],(-1,0))
            else:
                self.locations[-1] = add_tuples(self.locations[-1],(1,0))
        else:
            raise ValueError("Two adjacent breakpoints don't have anything in common")
        if self.locations[-1]==self.locations[-2]:
            self.locations.pop(-1)
        self.check()

    def check(self):
        for i in self.locations:
            if (i not in self.map.get_allowed_locations()) or (self.locations.count(i)>1):
                print("Game Over !")
                self.move_allowed = False

new_map = maps.Map("saved_maps/default_map.json")
bb = Snake(20,new_map)
print("Snake locations: ",bb.locations)
bb.move()
print("New Snake locations: ",bb.locations)
bb.move()
print("New Snake locations: ",bb.locations)
bb.move()
print("New Snake locations: ",bb.locations)
bb.move()
print("New Snake locations: ",bb.locations)