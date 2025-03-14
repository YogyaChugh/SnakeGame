"""This file defines the Fruits class for spawning fruits on map"""

import os,sys,json,random,requests

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

import maps

class Fruits:
    """Fruits class for random fruits on map"""

    def __init__(self,fruit_type,map_set):

        #Input checking
        if not isinstance(map,maps.Map):
            raise ValueError("Fruits class requires a map object ! \nCurrent Type: ",type(map_set))
        if not isinstance(fruit_type,str):
            raise ValueError("Fruit type should be of str type ! \nCurrent Type: ",type(fruit_type))
        temp_filepath = "https://static-files-inlg.onrender.com/saved_fruits.json"
        response = requests.get(temp_filepath)

        if response.status_code == 200:
            self.data = response.json()  # Parse JSON file
        else:
            print("Error loading JSON:", response.status_code)
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