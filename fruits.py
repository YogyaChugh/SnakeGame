"""This file defines the Fruits class for spawning fruits on map"""

import json
import os
import random
import sys

import flet as ft

import maps
import snake

tempo = os.path.abspath(os.path.dirname(__file__))
bundle_dir = getattr(sys, "_MEIPASS", tempo)
bundle_dir = os.path.abspath(bundle_dir)


class Fruits:
    """Fruits class for random fruits on map"""

    def __init__(self, fruit_type, map_set, snake_set):

        # Input checking
        if not isinstance(map_set, maps.Map):
            raise ValueError(
                "Fruits class requires a map object !",
                " \nCurrent Type: ",
                type(map_set),
            )
        if not isinstance(fruit_type, str):
            raise ValueError(
                "Fruit type should be of str type ! ",
                "\nCurrent Type: ",
                type(fruit_type),
            )
        if not isinstance(snake_set, snake.Snake):
            raise ValueError(
                "Fruits class requires a snake object ! \nCurrent Type: ",
                type(snake_set),
            )

        h = os.path.join(bundle_dir, "assets/saved_fruits.json")
        with open(h) as file:
            self.data = json.load(file)
        if self.data == {}:
            raise ValueError("Data File Empty :)")
        if fruit_type in self.data:
            self.data = self.data[fruit_type]
        else:
            raise ValueError(
                "Key is missing. Available keys:",
                self.data.keys(),
            )

        # Data set
        self.location = ()
        self.map = map_set
        self.snake = snake_set
        self.fruit_type = fruit_type

        self.randomize()

    def randomize(self):
        """Sets random location on map for fruit"""
        temp = self.map.get_allowed_locations()
        temp = [a for a in temp if temp not in self.snake.locations]
        self.location = random.choice(temp)

    def draw(self, left, top, size):
        img = "fruit.png"

        imag = ft.Image(
            img,
            width=size,
            height=size,
            left=left + size * self.location[0],
            top=top + size * self.location[1],
            fit=ft.ImageFit.FILL,
        )
        return imag
