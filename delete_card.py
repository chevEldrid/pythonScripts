import sys
from csv_file_handler import CSVFileHandler
# Given a name and a file, deletes one instance of the card from that file or returns not found
# FILE = FIRST ARGUMENT, CARD = SECOND ARGUMENT
# ---------------------------
CSV_ARG_POS = 1
CARD_ARG_POS = 2


def main():
    card_file = sys.argv[CSV_ARG_POS]
    card_name = sys.argv[CARD_ARG_POS]

    csv_file_reader = CSVFileHandler(card_file)
    if(csv_file_reader.file_exists()):
        print(
            f"{card_file} successfully read in. Will delete on instance of {card_name} in file")
    else:
        print("ERROR: csv file could not be read. Please input name of csvs as second arg")
        sys.exit()

    card_list = csv_file_reader.read_file()
    found = False
    list_result = []
    for i, val in enumerate(card_list):
        name = val[0]
        qty = int(val[1])
        price = float(val[2])
        # if the card hasn't already been found...
        if not found and name == card_name:
            found = True
            card_qty = (qty - 1)
            if qty > 1:
                list_result.append((name, (qty - 1), price))
            print(
                f"SUCCESS: {card_name} found and one copy removed. You have {card_qty} copies remaining!")
        else:
            list_result.append((name, qty, price))

    if not found:
        print(f"ERROR: {card_name} could not be found in the selected file...")
    else:
        csv_file_reader.write_file(list_result)


if __name__ == "__main__":
    main()
