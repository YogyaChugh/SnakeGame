# This file contains functions to perform operations on
# tuples saving data from unintended
# changes to tuples ! It has functions for adding content in tuples,
# multiplying with a scalar
# or getting the difference between 2 collinear tuples (1 value is common)
# NOTE: This file is hard-coded for tuples with 2 values only !

import math
import os
import sys

import flet as ft

atempboy = os.path.abspath(os.path.dirname(__file__))
bundle_dir = getattr(sys, "_MEIPASS", atempboy)
bundle_dir = os.path.abspath(bundle_dir)

audio2 = ft.Audio(os.path.join(bundle_dir, "audio/bonus.wav"), autoplay=True)
audio1 = ft.Audio(os.path.join(bundle_dir, "audio/lose.wav"), autoplay=True)


def add_tuples(a, b):
    """Just adds 2 tuples dude"""
    # Input checking
    if not isinstance(a, tuple) and not isinstance(b, tuple):
        raise ValueError(
            "Values passed are not tuples as their intended usage ! \nTypes: ",
            type(a),
            " and ",
            type(b),
        )
    if (
        not all(isinstance(item, int) for item in a)
        and not all(isinstance(item2, float) for item2 in a)
    ) or (
        not all(isinstance(item3, int) for item3 in b)
        and not all(isinstance(item4, float) for item4 in b)
    ):
        raise ValueError("Tuple values are other than int or string !")
    if len(a) != len(b):
        raise ValueError(
            "Values passed are not of same length",
            " as their intended usage ! \nTuple 1 length: ",
            len(a),
            "\nTuple 2 length: ",
            len(b),
        )

    # Main Logic
    c = []
    for i in range(len(a)):
        c.append(a[i] + b[i])
    return tuple(c)


def mul_tuple(a, b):
    """Multiplies the tuple a with number b"""
    # Input checking
    if not isinstance(a, tuple):
        raise ValueError(
            "Value passed is not a tuple as it's intended usage ! \nTypes: ",
            type(a),
            " and ",
            type(b),
        )
    if not isinstance(b, int) and not isinstance(b, float):
        raise ValueError(
            "Value passed is neither an integer nor a float",
            " as it's intended usage ! \nSupplied Type: ",
            type(b),
        )
    if not all(isinstance(item, int) for item in a) and not all(
        isinstance(item2, float) for item2 in a
    ):
        raise ValueError(
            "Values in the tuple are of types other",
            " than int or string !",
        )

    # Main Logic
    a = list(a)
    for i in range(len(a)):
        a[i] = int(a[i] * b)
    return tuple(a)


def diff_tuples(a, b):
    """Gets difference between 2 tuples but note"""
    """that they should have either same row or same column"""
    # Input checking
    if not isinstance(a, tuple) or not isinstance(b, tuple):
        raise ValueError(
            "Values passed are not tuples as their intended usage ! \nTypes: ",
            type(a),
            " and ",
            type(b),
        )
    if (
        not all(isinstance(item, int) for item in a)
        and not all(isinstance(item2, float) for item2 in a)
    ) or (
        not all(isinstance(item3, int) for item3 in b)
        and not all(isinstance(item4, float) for item4 in b)
    ):
        raise ValueError(
            "Values in the tuple are of types other",
            " than int or string !",
        )
    if len(a) != len(b):
        raise ValueError(
            "Values passed are not of same length as their",
            " intended usage ! \nTuple 1 length: ",
            len(a),
            "\nTuple 2 length: ",
            len(b),
        )

    # Main Logic
    if a[0] == b[0]:
        return math.fabs(b[1] - a[1])
    elif a[1] == b[1]:
        return math.fabs(b[0] - a[0])
    else:
        raise ValueError(
            "Differentiating tuples are not having any value",
            " in common ! \nTuples: \n",
            a,
            "\n",
            b,
        )
