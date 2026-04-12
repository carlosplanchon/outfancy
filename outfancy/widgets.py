#!/usr/bin/env python3

from datetime import datetime
from re import sub
from time import strptime


def actual_date() -> str:
    """This function return the actual date."""
    now = datetime.now()
    return f"{now.day:02d}-{now.month:02d}-{now.year}"


def actual_hour() -> str:
    """This function return the actual hour."""
    now = datetime.now()
    return f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"


def compress_list(list_to_compress: list[int]) -> list[int]:
    """
    This function compress a list while maintaining order,
    I.e: [1, 6, 4] is converted in [0 ,2, 1].
    """
    # If list_to_compress is empty the same list is returned, because
    # is imposible to compress.
    if list_to_compress == []:
        return list_to_compress

    compressed_list = []
    # The list compressed_list is filled by a number of zeros that equals
    # the len of list_to_compress.
    for x in range(len(list_to_compress)):
        compressed_list.append(0)

    # Num used to fill compressed_list.
    num = 0
    # Calculate the range properly for both positive and negative numbers
    min_val = min(list_to_compress)
    max_val = max(list_to_compress)
    range_size = max_val - min_val + 1

    # It walks the numbers from minimum to maximum present in the list
    for x in range(range_size):
        # Calculate the actual number we're checking
        number = min_val + x
        if number in list_to_compress:
            # num is added to compressed list in the index that is
            # occupied by the first occurrence of this number
            compressed_list[list_to_compress.index(number)] = num
            num += 1

    return compressed_list


def create_matrix(x: int, y: int, fill: str = "") -> list[list[str]]:
    """This function create a 2d matrix based on it dimensions."""
    return [[fill for p in range(x)] for p in range(y)]


def index_is_in_list(the_list: list, index: int) -> bool:
    """This function check if an index is in the specified list."""
    return bool(0 <= index < len(the_list))


def is_complete_hour(text: str) -> bool:
    """This function check if the input is a valid complete hour."""
    for fmt in ["%H:%M:%S", "%H:%M"]:
        try:
            strptime(text, fmt)
            return True
        except ValueError:
            pass
    return False


def is_date(text: str) -> bool:
    """
    This function check if the input is a valid date, format:
    "dd-mm-yyyy, dd-mm-yy, dd-mm-yyyy hh-mm-ss, dd-mm-yy hh-mm-ss"
    "yyyy-mm-dd, yyyy-mm-dd hh-mm-ss"
    and: "d-m-yy, d-m-yyyy, h-m-s"
    """
    text = normalise_date(text)
    for fmt in [
        "%d-%m-%Y",
        "%d-%m-%y",
        "%d-%m-%Y %H-%M-%S",
        "%d-%m-%y %H-%M-%S",
        "%Y-%m-%d",
        "%Y-%m-%d %H-%M-%S"
            ]:
        try:
            strptime(text, fmt)
            return True
        except ValueError:
            pass

    return False


def printed_length(text: str) -> int:
    """This function measure the length of a printed string."""
    # It returns the length of the printed string
    return len(remove_colors(text))


def normalise_date(text: str) -> str:
    """This function normalize text, is useful to normalize dates."""
    text = text.replace(
        "/", "-").replace(
        ":", "-").replace(
        ".", "-").replace(
        "@", "-")
    return text


def remove_colors(text: str) -> str:
    """This function remove the ANSI color codes of a string."""
    # More comprehensive regex that handles:
    # - Basic colors: \x1b[31m
    # - Bold/styles: \x1b[1;32m
    # - 256 colors: \x1b[38;5;123m
    # - True RGB: \x1b[38;2;255;0;0m
    # - Any sequence length with semicolons
    return sub(
        r"\x1b\[[0-9;]*[mKHfABCDsuJSTG]?",
        "",
        text
    )
