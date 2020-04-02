import os
from unidecode import unidecode

PATH = "/home/james/Fantasy-Premier-League/data"
EXAMPLE = "/home/james/Fantasy-Premier-League/data/2016-17/gws/gw5.csv"


def remove_accents(file_name, excel_encoding=False):
    with open(file_name.replace(".csv", ".cleaned.csv"), "w") as write_file:
        if excel_encoding:
            with open(file_name, encoding="cp1252") as open_file:
                for line in open_file:
                    line = unidecode(line)
                    write_file.write(line)
        else:
            with open(file_name) as open_file:
                for line in open_file:
                    line = unidecode(line)
                    write_file.write(line)


if __name__ == "__main__":
    for year in os.listdir(PATH):
        for file in os.listdir(os.path.join(PATH, year, "gws")):
            if file.endswith(".csv"):
                print(os.path.join(PATH, year, "gws", file))
                excel_encoding = year in ["2016-17", "2017-18", "2018-19"]
                remove_accents(os.path.join(PATH, year, "gws", file), excel_encoding)
