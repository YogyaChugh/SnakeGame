"""This file defines the Fruits class for spawning fruits on map"""

import os,sys,json, random
paths = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))
sys.path.insert(0,paths)

from src.Maps.maps import Map

class Fruits:
    """Fruits class for random fruits on map"""

    def __init__(self,fruit_type,map_set):

        #Input checking
        if not isinstance(map,Map):
            raise ValueError("Fruits class requires a map object ! \nCurrent Type: ",type(map_set))
        if not isinstance(fruit_type,str):
            raise ValueError("Fruit type should be of str type ! \nCurrent Type: ",type(fruit_type))
        temp_filepath = os.path.join(paths,"src/Fruits/saved_fruits.json")
        if not os.path.isfile(temp_filepath):
            raise FileNotFoundError("Saved Fruits file not found ! It has either been moved/deleted !")

        #Opens file and checks it
        with open(temp_filepath) as file:
            self.data = json.load(file)
        if self.data=={}:
            raise ValueError("Data File Empty :)")
        if fruit_type in self.data:
            self.data = self.data[fruit_type]
        else:
            raise ValueError("Key is missing. Available keys:", self.data.keys())

        #Data set
        self.location = ()
        self.map = map_set
        self.fruit_type = fruit_type

        self.randomize()

    def randomize(self):
        """Sets random location on map for fruit"""
        self.location = random.choice(self.map.get_allowed_locations())