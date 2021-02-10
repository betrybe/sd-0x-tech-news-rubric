import csv


def csv_importer(filepath):
    try:
        if filepath.endswith(".csv"):
            with open(filepath) as file:
                csv_file = csv.DictReader(file, delimiter=";", quotechar='"')
                data = [item for item in csv_file]
                return data
        else:
            raise ValueError("Formato invalido")
    except FileNotFoundError:
        raise ValueError("Arquivo tests/file_not_exist.csv não encontrado")
