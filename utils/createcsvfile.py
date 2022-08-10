"""
    Author: Noutcheu Libert Joran
"""
import csv
import logging
import os
from pathlib import Path

import pandas


def save_result_to_csv(content_make_to_csv, header_file, file_name) -> None:
    """write a data into a csv file.

    :param content_make_to_csv: list[ file:dict ] that you want to print in
     your csv file
    :param header_file: list content str list of your header csv file
    :param file_name: str  this is the name of your file
    :return None
    """

    # we get a home folder to create a csv in ResultsCS folder
    folder_name = "ResultsCSV"
    folder = makefolder(folder_name)

    with open(folder + f"/{file_name}.csv", "w", encoding="UTF-8") as file:
        writer = csv.DictWriter(file, fieldnames=header_file)
        # Use writerows() not writerow()
        writer.writeheader()
        writer.writerows(content_make_to_csv)


def save_data_to_csv_with_pandas(data_for_make_to_csv, file_name) -> None:
    """write a data into a csv file.

    :param data_for_make_to_csv: list[ file:dict ] that you want to print
    in your csv file
    :param file_name: str  this is the name of your file
    :return None
    """

    folder_name = "ResultsCSV"
    folder = makefolder(folder_name)

    dataframe = pandas.DataFrame(data_for_make_to_csv)
    dataframe.to_csv(folder + "/" + file_name + ".csv")


def makefolder(folder_path):
    home = str(Path.home())
    folder = os.path.join(home, folder_path)
    if not os.path.isdir(folder):
        os.mkdir(folder)

    return folder