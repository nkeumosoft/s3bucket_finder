"""
    Author: Noutcheu Libert Joran
"""
import csv
import logging
import os
from pathlib import Path
from typing import List, Optional

import pandas


def save_result_to_csv(
    content_make_to_csv: List[dict],
    header_file: List[str],
    file_name: str,
    folder_name: str = "ResultsCSV",
) -> None:
    """write a data into a csv file.

    :param content_make_to_csv: list[ file:dict ] that you want to print in
     your csv file
    :param header_file: list content str list of your header csv file
    :param file_name: str  this is the name of your file
    :param folder_name: str  this is the name of your output folder
    :return None
    """

    # we get a home folder to create a csv in ResultsCS folder

    folder = makefolder(folder_name)

    with open(f"{folder}/{file_name}.csv", "w", encoding="UTF-8") as file:
        writer = csv.DictWriter(file, fieldnames=header_file)
        # Use writerows() not writerow()
        writer.writeheader()
        writer.writerows(content_make_to_csv)


def save_data_to_csv_with_pandas(
    data_for_make_to_csv: List[dict],
    file_name: str,
    folder_name: str = "ResultsCSV",
) -> Optional[str]:
    """write a data into a csv file.

    :param data_for_make_to_csv: list[ file:dict ] that you want to print
    in your csv file
    :param file_name: str  this is the name of your file
    :param folder_name: str  this is the name of your output folder
    :return None
    """

    folder = makefolder(folder_name)
    dataframe = pandas.DataFrame(data_for_make_to_csv)
    dataframe.to_csv(f"{folder}/{file_name}.csv")
    return folder


def makefolder(folder_path: str) -> Optional[str]:
    """create a folder.

    :param folder_path: str the path of folder that you want to check
    :return folder:str
    """
    try:
        if folder_path in "ResultsCSV":
            folder = os.getcwd()
            folder = os.path.join(folder, folder_path)
        else:
            folder = check_absolute_path(folder_path)

        if not folder_exist(folder):
            os.mkdir(folder)

        return folder
    except FileNotFoundError:
        pass
    return None


def folder_exist(folder_path: str) -> bool:
    """check if folder exist.

    :param folder_path: str the path of folder that you want to check
    :return :bool
    """
    try:
        if os.path.isdir(folder_path):
            return True
    except FileNotFoundError:
        logging.error(f"No such file or directory: {folder_path}")

    return False


def check_absolute_path(path_link: str) -> str:
    """check if path is relative and changer it to absolute path.

    :param path_link: str the path of folder that you want to check
    :return folder:str
    """
    home = str(Path.home())
    if home not in path_link:
        folder = os.path.join(home, path_link)
    else:
        folder = path_link

    return folder
