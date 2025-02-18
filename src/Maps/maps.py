import json
import sys,os
paths = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0,paths)



class Map():
    def __init__(self,location):
        location = os.path.join(paths,location)
        with open(location,'r') as file:
            self.data = json.load(file)
        self.preferred_background_image = self.data["preferred_background_image"]
        self.locations = self.data["locations"]
        self.total_height_px = self.data["total_height_px"]
        self.total_width_px = self.data["total_width_px"]
        self.cell_size_px = self.data["cell_size_px"]
        self.allowed_blocks = self.data["allowed_blocks"]
        self.disallowed_blocks = self.data["disallowed_blocks"]
        self.allowed_locations = []


    def get_allowed_locations(self):
        self.allowed_locations = []
        for i in range(len(self.locations)):
            for j in range(len(self.locations[i])):
                if self.locations[i][j]==1:
                    self.allowed_locations.append((i,j))
        print(self.allowed_locations)
        return self.allowed_locations

