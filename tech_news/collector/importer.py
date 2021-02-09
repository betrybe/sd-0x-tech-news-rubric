import csv


def csv_importer(filepath):

    if not filepath.endswith(".csv"):
        raise ValueError("Formato invalido")

    import_result = []
    try:
        with open(filepath, newline="") as csvfile:
            for row in csv.DictReader(csvfile, delimiter=";"):
                import_result.append(build_dict_from_csv_row(row))
    except IOError:
        raise ValueError(f"Arquivo {filepath} não encontrado")
    else:
        return import_result


def build_dict_from_csv_row(row):
    built_dict = {}
    for key, value in row.items():
        built_dict[key] = value
    return built_dict
