"""This file consists of the Snake class responsible for creating snake object"""

#Add upper directory path
import sys,os,math,asyncio
import flet as ft
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

#Other important imports
import json,random
from base import *
import maps  # Importing the Map class from maps.py
from PyPDF2 import PdfReader


#Dictionary + List storing directions possible
directions_dict = {"LEFT":(-1,0),"RIGHT":(1,0),"UP":(0,-1),"DOWN":(0,1)}
directions_list = ["LEFT","RIGHT","UP","DOWN"]

class GameOver(Exception):
    def __init__(self,message="Game's Over"):
        self.message = message
        super().__init__(self.message)

class Snake:
    """Class representing a snake on a particular map ! Requires a map object to be linked !\n
    Has the following functions:-\n
    1)fetch_direction(current_location,ftemp) - Requires list of locations to choose from and returns the direction\n
    2)get_snakepos_random() - Requires a map object and fills the location list with a random snake position on the map\n
    3)move() - Moves the snake by 1 position\n
    4)check() - Checks if the snake is in disallowed sections(its own body or the border/restricted blocks)"""
    def __init__(self,snake_type,map_for_snake):
        #Checks if map is an object of Map class

        #Input checking
        if not isinstance(map_for_snake,maps.Map):
            raise ValueError("Should supply a Map object !\n Current Type: ",type(map_for_snake))
        if not isinstance(snake_type,str):
            raise ValueError("File type shared for snake is invalid !\n Current Type: ",type(snake_type))
        if not os.path.isfile(os.path.abspath(os.path.join(bundle_dir,"saved_snakes.json"))):
            raise ValueError("Saved snakes file either moved or renamed ! Update Code !")

        with open("saved_snakes.json") as file:
            data = json.load(file)
        data = data[snake_type]
        self.data = data
        if data=={}:
            raise ValueError("Snake Data not found ! Data list empty !")

        #check_snake_json(data)

        #Data from saved_snakes.json
        self.snake_type = snake_type
        self.name = data["Name"]
        self.graphics_location = data["snake_graphics"]
        self.color_encodings = data["color_encodings"]
        self.length = data["length"]
        self.images = None
        self.left = 0
        self.top = 0
        self.size = 0
        self.moving = True
        self.done = False
        self.first = True

        #Other data
        self.move_allowed = True
        self.map = map_for_snake
        self.locations = [] #Stores the beginning,end and breakpoints of the snake's body,i.e. (2,3),(2,1)
        self.direction = None
        self.direction_pt = None
        self.keep_track_length = 0
        self.prev_images = None

        self.get_snakepos_random() #Initialize location of snake on map

    def increase_length(self):
        self.length+=1
        a = self.get_direction(self.locations[-1],self.locations[-2])
        b = mul_tuple(a,-1)
        self.locations[-1] = add_tuples(self.locations[-1],b)

    def reset(self,e=None):
        self.locations = []
        self.direction = None
        self.direction_pt = None
        self.keep_track_length = 0
        self.left = 0
        self.top = 0
        self.size = 0
        self.move_allowed = True
        self.done = False
        self.length = self.data["length"]
        self.name = self.data["Name"]
        self.graphics_location = self.data["snake_graphics"]
        self.color_encodings = self.data["color_encodings"]

        self.get_snakepos_random()

    @staticmethod
    def fetch_direction(current_location, ftemporary):
        """Requires a list of locations from which it chooses randomly and returns the direction for the snake"""

        #Input checking
        if not isinstance(current_location,tuple):
            return ValueError("Current location needs to be a tuple !\n Current type: ",type(current_location))
        if len(current_location) not in range(0,3):
            return ValueError("Current location tuple is incorrect !\n Current Location: ",current_location)
        if not all(isinstance(temp_var,int) for temp_var in current_location) and not all(isinstance(temp_var2,float) for temp_var2 in current_location):
            return ValueError("Current location has values of type other than ",type(int),"/",type(float))
        if not isinstance(ftemporary,list):
            return ValueError("Possible values need to be in form of a list !\n Current type: ",type(ftemporary))
        if not ftemporary:
            return ValueError("Possible value list is empty !")

        #Main Logic
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
            raise ValueError("Couldn't find snake object direction ! \nChosen Block: ",chosen_block) #JUST IN CASE

    def get_snakepos_random(self):
        """Randomly assigns location to the snake ! Called during initialization of the game"""

        #Checks if map is an object of Map class
        if not isinstance(self.map,maps.Map):
            raise TypeError("Should supply a Map object ! \nCurrent Type: ",type(self.map))

        #Member function of map for getting allowed locations in the form of (1,2) (row, column)
        allowed_locations = self.map.get_allowed_locations()
        if len(allowed_locations)<1:
            raise ValueError("Map data incorrectly supplied !\nlen(locations allowed) :",len(allowed_locations))

        #Just to store where the last breakpoint(could be head) points to
        temp_direction_pt = None

        if self.length<3:
            raise ValueError("Minimum length for the snake is 3 blocks !\n Current Length: ",self.length)

        #Loops for every body part of snake
        for i in range(self.length):
            if i==0:
                self.locations = []

            #What if it's the head! We need to randomize the location and also set the direction
            if len(self.locations) == 0:
                self.locations.append(random.choice(self.map.get_three_headed_locations()))
                #This line is to eliminate the locations whose opposite isn't present ! like remove the UP location if DOWN isn't there
                #It is done to ensure that the snake has scope of movement in both directions
                zee = [(add_tuples(self.locations[0],(1,0)),add_tuples(self.locations[0],(-1,0))),(add_tuples(self.locations[0],(0,1)),add_tuples(self.locations[0],(0,-1)))]
                ftemp = [(c[0],c[1]) for c in zee if (c[0] in allowed_locations  and c[1] in allowed_locations)]
                ftemp_2 = []
                for i in ftemp:
                    ftemp_2.append(i[0])
                    ftemp_2.append(i[1])
                if len(ftemp_2)<2: #Just in Case there is none (0% chances though cause of above loop)
                    raise ValueError("Final Temporary list got less expected values for spawning positions !\nValues: ",ftemp)

                #Fetching direction and also the points to be added later
                self.direction = self.fetch_direction(self.locations[0],ftemp_2)
                if not self.direction:
                    raise ValueError("Direction can't be None ! fetch_direction() returned None")
                temp_direction_pt = self.direction_pt = directions_dict[self.direction]

                #These temp direction ones will be used later in order to remember the direction of the last stored breakpoint
            else:
                #Just in Case
                if not self.direction:
                    raise ValueError("No direction for the snake :)")
                if not temp_direction_pt:
                    temp_direction_pt = self.direction_pt

                #The next position to suspect based on the temporary direction of last breakpoint
                #The current position ! That's it
                current_pos = add_tuples(self.locations[-1],mul_tuple(temp_direction_pt,-(i - self.keep_track_length)))
                next_pos = add_tuples(current_pos,mul_tuple(temp_direction_pt,-1))
                if (next_pos in allowed_locations) and (next_pos not in self.locations): #If the next position is even possible
                    if i == self.length-1: #If it's the tail
                        #NOTE: self.locations stores the beginning,end and breakpoints only
                        self.locations.append(current_pos)
                    else:
                        #It's just the body
                        pass
                else:
                    #What if there's a breakpoint
                    self.locations.append(current_pos)  #Added Breakpoint
                    self.keep_track_length += diff_tuples(self.locations[-1],self.locations[-2]) #Keeps track of the length before the last breakpoint

                    #Storing all possible positions for the snake after the breakpoint (Use ur mind, you will know that there can be max 2)
                    temp_nextpos_possible = [add_tuples(current_pos,(temp_direction_pt[1],temp_direction_pt[0])),add_tuples(current_pos,(-temp_direction_pt[1],-temp_direction_pt[0]))]
                    temp_nextpos_possible = [a for a in temp_nextpos_possible if a in allowed_locations]
                    if temp_nextpos_possible==[]:
                        if (i+1)!=self.length:
                            raise Warning("Snake length not completed but reached an end !")
                            return

                    #Store the direction and direction_pt for this breakpoint
                    temp_direction = self.fetch_direction(current_pos,temp_nextpos_possible)
                    temp_direction_pt = directions_dict[temp_direction]

    def move(self):
        if not self.images:
            raise ValueError("Can't move snake ! there are no graphics associated !")
        """Moves the snake by 1 position and calls the check() function to verify if it's possible"""
        if not self.move_allowed or not self.locations[0]: #In case snake is in diallowed blocks
            return None
        temp = self.locations[0]
        self.locations[0] = add_tuples(self.locations[0],self.direction_pt) #Updates the head position
        if self.locations[0][0]!=self.locations[1][0] and self.locations[0][1]!=self.locations[1][1]:
            newer = []
            newer.append(self.locations[0])
            newer.append(temp)
            newer.extend(self.locations[1:])
            self.locations = newer

        #When 0th index of last breakpoint and tail are same, update the tail accordingly
        if self.locations[-1][0] == self.locations[-2][0]:
            #If the snake tail is on right of the breakpoint, so subtract 1 from tail acc to game coordinate system
            if self.locations[-1][1]>self.locations[-2][1]:
                self.locations[-1] = add_tuples(self.locations[-1],(0,-1))
            #Vice Versa
            else:
                self.locations[-1] = add_tuples(self.locations[-1],(0,1))
        #When 1st index is same
        elif self.locations[-1][1] == self.locations[-2][1]:
            if self.locations[-1][0]>self.locations[-2][0]:
                self.locations[-1] = add_tuples(self.locations[-1],(-1,0))
            else:
                self.locations[-1] = add_tuples(self.locations[-1],(1,0))
        #Doesn't happen cause of code in get_snakepos_random but just for the sake of precaution
        else:
            raise ValueError("Two adjacent breakpoints don't have anything in common !\nBreakpoints: ",self.locations[-1],",",self.locations[-2])

        #What if after the above code, the tail reaches the breakpoint location, then just let one live :)
        if self.locations[-1]==self.locations[-2]:
            self.locations.pop(-1)

        #Check if the snake has crossed its limits
        self.check()

    def check(self):
        """Checks whether the snake is in disallowed blocks and sets the self.move_allowed accordingly as well
        as setting the self.locations to all None"""
        for i in self.locations:
            #If either in disallowed locations or touches its own body
            if (i not in self.map.get_allowed_locations()) or (self.locations.count(i)>1):
                self.move_allowed = False
                #Set its own locations to None
                for j in range(len(self.locations)):
                    self.locations[j] = None
                raise GameOver

    def find_len(self):
        if self.locations==[]:
            return 0
        counting = 1
        second_count = 0
        temp = self.locations[0]
        while True:
            if counting==self.length or second_count==len(self.locations):
                return counting
            while temp!=self.locations[second_count]:
                if temp[0]==self.locations[second_count][0]:
                    if temp[1]>self.locations[second_count][1]:
                        temp = (temp[0],temp[1]-1)
                    else:
                        temp = (temp[0],temp[1]+1)
                else:
                    if temp[0]>self.locations[second_count][0]:
                        temp = (temp[0]-1,temp[1])
                    else:
                        temp = (temp[0]+1,temp[1])
                counting += 1
            if temp==self.locations[second_count]:
                second_count += 1
        return counting

    def get_direction(self,a,b):
        if a[0]==b[0]:
            c = -(a[1]-b[1])
            return (0,int(c/abs(c)))
        else:
            c = -(a[0]-b[0])
            return (int(c/abs(c)),0)

    def draw(self, left, top, size):
        images = []
        self.images = []
        self.left = left
        self.top = top
        self.size = size
        next = 0
        temp = self.locations[0]
        direction = mul_tuple(directions_dict[self.direction], -1)
        
        turning_dict = {
            ((0,1),(1,0)):"body_topright.png",
            ((0,1),(-1,0)):"body_topleft.png",
            ((0,-1),(1,0)):"body_bottomright.png",
            ((0,-1),(-1,0)):"body_bottomleft.png",
            ((1,0),(0,-1)):"body_topleft.png",
            ((1,0),(0,1)):"body_bottomleft.png",
            ((-1,0),(0,-1)):"body_topright.png",
            ((-1,0),(0,1)):"body_bottomright.png"
        }
    
        for i in range(self.length):
            if next < len(self.locations) and temp == self.locations[next]:
                next += 1
                if i == 0:
                    img_loc = {
                        (0, 1): "head_down.png",
                        (0, -1): "head_up.png",
                        (1, 0): "head_right.png",
                        (-1, 0): "head_left.png"
                    }.get(directions_dict[self.direction], "head_right.png")
                
                elif i == self.length - 1:
                    img_loc = {
                        (0, 1): "tail_down.png",
                        (0, -1): "tail_up.png",
                        (1, 0): "tail_right.png",
                        (-1, 0): "tail_left.png"
                    }.get(direction, "tail_right.png")
                
                else:
                    if next < len(self.locations):
                        temp_direction = self.get_direction(temp, self.locations[next])
                        img_loc = turning_dict.get((direction, temp_direction), "body_horizontal.png")
                        direction = temp_direction
                    else:
                        img_loc = "body_horizontal.png"
            
            else:
                img_loc = "body_horizontal.png" if direction in [(1, 0), (-1, 0)] else "body_vertical.png"
    
            image_path = os.path.abspath(os.path.join(bundle_dir, img_loc))
    
            temp_image = ft.Image(
                src=img_loc,
                width=size,
                height=size,
                left=left + (temp[0] * size),
                top=top + (temp[1] * size),
                fit=ft.ImageFit.FILL
            )
    
            self.images.append((img_loc[1:-4], left + (temp[0] * size), top + (temp[1] * size), size, temp_image))
            images.append(temp_image)
    
            temp = add_tuples(temp, direction)  # Move to the next position
    
        return images




if __name__ == "__main__":
    new_map = maps.Map("Map_01")
    bb = Snake("Snake_01",new_map)
    print("Snake locations: ",bb.locations)
    bb.move()
    print("New Snake locations: ",bb.locations)
    bb.move()
    print("New Snake locations: ",bb.locations)
    bb.move()
    print("New Snake locations: ",bb.locations)
    bb.move()
    print("New Snake locations: ",bb.locations)
