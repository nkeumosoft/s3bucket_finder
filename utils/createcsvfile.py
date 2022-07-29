"""
    Author: Noutcheu Libert Joran
"""
import csv
import os
from pathlib import Path


def make_bucket_result_to_csv(content_make_to_csv, header_file,
                file_name) -> None:
    """
     write a data into a csv file
     :param content_make_to_csv: list[ file:dict ] that you want to print in your csv file
     :param header_file: list content str list of your header csv file
     :param file_name: str  this is the name of your file
     :return None
    """

    # we get a home folder to create a csv in ResultsCS folder
    home = str(Path.home())
    folder = os.path.join(home, "ResultsCSV")
    if not os.path.isdir(folder):
        os.mkdir(folder)

    with open(folder + f"/{file_name}.csv", 'w', encoding='UTF-8') \
            as file:
        writer = csv.DictWriter(file, fieldnames=header_file)
        # Use writerows() not writerow()
        writer.writeheader()
        writer.writerows(content_make_to_csv)
