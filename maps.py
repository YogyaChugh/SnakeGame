# This file contains the Map class responsible for
# creating Map objects using the json file

# File Imports
import json
import os
import sys

import flet as ft

import base

temop = os.path.abspath(os.path.dirname(__file__))
bundle_dir = getattr(sys, "_MEIPASS", temop)
bundle_dir = os.path.abspath(bundle_dir)


class Map:
    """Class Map storing default/saved maps"""

    def __init__(self, map_type):

        # Input checking
        if not isinstance(map_type, str):
            raise ValueError(
                "Value must be a string! ", "\nCurrent type: ", type(map_type)
            )
        map_file = os.path.join(bundle_dir, "assets/saved_maps.json")
        with open(map_file, "r") as f:
            self.data = json.load(f)
        if self.data == {}:
            raise ValueError("Data File is empty !")
        if map_type in self.data:
            self.data = self.data[map_type]
        else:
            raise ValueError(
                "Key is missing. Available keys:",
                self.data.keys(),
            )
        if self.data == {}:
            raise ValueError("Data File set is empty !")

        # Main Logic
        self.map_type = map_type
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
                if self.locations[i][j] == 1:
                    self.allowed_locations.append((i, j))
        return self.allowed_locations

    def get_three_headed_locations(self):
        temp_list = []
        for i in self.get_allowed_locations():
            goa = [
                base.add_tuples(i, (1, 0)),
                base.add_tuples(i, (-1, 0)),
                base.add_tuples(i, (0, 1)),
                base.add_tuples(i, (0, -1)),
            ]
            goa = [a for a in goa if a in self.allowed_locations]
            if len(goa) >= 3:
                temp_list.append(i)
        if temp_list == []:
            raise ValueError(
                "No points with minimum 3 open ends in ",
                f"object map ! Map type:- {self.map_type}",
            )
        return temp_list

    def get_container(self, width, height):
        grid_view = ft.GridView(
            run_spacing=0,
            padding=0,
            runs_count=len(self.data["locations"][0]),
            child_aspect_ratio=1,
            expand=1,
            expand_loose=True,
            spacing=0,
            width=width / 2,
        )
        block_size = (width / 2) / len(self.data["locations"][0])
        height_container = block_size * len(self.data["locations"])
        top = (height - height_container) / 2

        for i in self.data["locations"]:
            for j in i:
                if j == 0:
                    grid_view.controls.append(
                        ft.Image("wooden_dark_block.png"),
                    )
                elif j == 1:
                    grid_view.controls.append(ft.Image("wooden_block.png"))
        cont = ft.Container(
            content=grid_view,
            expand=True,
            left=width / 4,
            top=top,
        )
        return (cont, width / 4, top, block_size)
