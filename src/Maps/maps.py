"""This file contains the Map class responsible for creating Map objects using the json file"""

#File Imports
import json
import os,sys

locs = os.path.abspath(os.path.dirname(__file__))

class Map:
    """Class Map storing default/saved maps"""
    def __init__(self,map_type):

        #Input checking
        if not isinstance(map_type,str):
            raise ValueError("Value must be a string! \nCurrent type: ",type(location))
        if not os.path.isfile(os.path.join(locs,"saved_maps.json")):
            raise FileNotFoundError("File doesn't exist !")
        with open(os.path.join(locs,"saved_maps.json"),'r') as file:
            self.data = json.load(file)
        if self.data=={}:
            raise ValueError("Data File is empty !")
        print(self.data)
        print(type(self.data))
        print(repr(list(self.data.keys())))
        if "Map_01" in self.data:
            print("Key exists!")
            self.data = self.data["Map_01"]
        else:
            print("Key is missing. Available keys:", self.data.keys())
        if self.data=={}:
            raise ValueError("Data File set is empty !")

        #Main Logic
        self.preferred_background_image = self.data["map_graphics"]
        self.locations = self.data["locations"]
        self.total_height_px = self.data["total_height_px"]
        self.total_width_px = self.data["total_width_px"]
        self.cell_size_px = self.data["cell_size_px"]
        self.allowed_blocks = self.data["allowed_blocks"]
        self.disallowed_blocks = self.data["disallowed_blocks"]
        self.allowed_locations = []


    def get_allowed_locations(self):
        """Returns the allowed locations on the map object created"""
        self.allowed_locations = []
        for i in range(len(self.locations)):
            for j in range(len(self.locations[i])):
                if self.locations[i][j]==1:
                    self.allowed_locations.append((i,j))
        return self.allowed_locations

