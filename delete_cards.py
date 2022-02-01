import sys
from csv_file_handler import CSVFileHandler
from mtg_card import MTGCard
from utils import BASHColors
# Given a name and a file, deletes one instance of the card from that file or returns not found
# FILE = FIRST ARGUMENT, CARDS_TO_REMOVE = SECOND ARGUMENT
# ---------------------------


CSV_ARG_POS = 1
CARDLIST_ARG_POS = 2

card_list = []
removal_list = []
card_qty = 0


def generate_card_name(line):
    split_line = line.split()
    del split_line[0]
    return " ".join(split_line)


def read_removal_file(file):
    cards_to_remove = []
    with open(file) as txtfile:
        lines = txtfile.readlines()
        for line in lines:
            cards_to_remove.append(generate_card_name(line))
    return cards_to_remove


def update_card_qty(collection, card_name):
    list_result = []
    found = False
    for i, val in enumerate(collection):
        card = MTGCard(val[0], val[1], val[2])
        # if the card hasn't already been found...'
        name = card.get_name()
        if not found and name == card_name:
            found = True
            card.quantity = card.quantity - 1
            if card.quantity > 0:
                list_result.append(card.print_card())
            print(f"{BASHColors.OKGREEN}SUCCESS{BASHColors.ENDC}: {card_name} found. Removing {card.full_name}. You now have {card.quantity}.")
        else:
            list_result.append(card.print_card())
    if not found:
        print(f"{BASHColors.FAIL}ERROR{BASHColors.ENDC}: {card_name} could not be found in the selected file")
    return list_result


def main():
    collection_file = sys.argv[CSV_ARG_POS]
    removal_file = sys.argv[CARDLIST_ARG_POS]

    csv_file_reader = CSVFileHandler(collection_file)

    if(csv_file_reader.file_exists()):
        print(
            f"{collection_file} successfully read in. Will delete one instance of all cards in {removal_file}.")
    else:
        print("ERROR: csv file could not be read. Please input name of csvs as second arg")
        sys.exit()

    card_list = csv_file_reader.read_file()
    removal_list = read_removal_file(removal_file)

    for card_name in removal_list:
        card_list = update_card_qty(card_list, card_name)

    csv_file_reader.write_file(card_list)


if __name__ == "__main__":
    main()
