import asyncio
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from pathlib import Path

from constants import BASE_DIR
from loader.utils import load_data_from_excel_file, load_database


def parser():
    parser = ArgumentParser(
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("load_data", help="Ведите имя файла и имя листа через аргументы")

    parser.add_argument("-n", "--name", type=str, help="Введите имя файла.")
    parser.add_argument("-s", "--sheet", type=str, help="Введите имя листа.")

    args: Namespace = parser.parse_args()

    if not args.name or not args.sheet:
        raise ValueError

    return args.name, args.sheet


if __name__ == "__main__":
    name_file, sheet = parser()
    path_file: Path = BASE_DIR / name_file
    if not path_file.is_file():
        raise FileNotFoundError
    data = load_data_from_excel_file(path_file, "Лист1")
    asyncio.run(load_database(data))
