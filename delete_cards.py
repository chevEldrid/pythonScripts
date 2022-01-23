import sys
import csv
from turtle import update
# Given a name and a file, deletes one instance of the card from that file or returns not found
# FILE = FIRST ARGUMENT, CARDS_TO_REMOVE = SECOND ARGUMENT
# ---------------------------


class bcolors:
    FAIL = '\033[91m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'


CSV_ARG_POS = 1
CARDLIST_ARG_POS = 2

card_list = []
removal_list = []
card_qty = 0


def read_collection_file(file):
    temp = []
    with open(file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            try:
                temp.append((row[0], row[1], row[2]))
                # print(row)
            except:
                print(
                    "Error on {0}. Will be dropped from Table".format(row[0]))
    # create copy of cards list to iterate through and not mess up for loop
    del temp[0]
    return temp


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

# removes tags given to card name on sheet


def get_name(card):
    words = card.split()
    name = []
    for word in words:
        # if card is foil or etched foil...
        if "*" in word:
            continue
        # if card has set code in the form [kld]...
        if "[" in word:
            continue
        # if card had collectors number in form {126}...
        if "{" in word:
            continue
        name.append(word)
    return " ".join(name)


def update_card_qty(collection, card_name):
    list_result = []
    found = False
    for i, val in enumerate(collection):
        name = get_name(val[0])
        full_name = val[0]
        qty = int(val[1])
        price = float(val[2])
        # if the card hasn't already been found...
        if not found and name == card_name:
            found = True
            card_qty = (qty - 1)
            if qty > 1:
                list_result.append((name, (qty - 1), price))
            print(bcolors.OKGREEN+"SUCCESS"+bcolors.ENDC+": " + card_name+" found. Removing " +
                  full_name+". You now have " + str(card_qty)+".")
        else:
            list_result.append((full_name, qty, price))
    if not found:
        print(bcolors.FAIL+"ERROR"+bcolors.ENDC+": "+card_name +
              " could not be found in the selected file...")
    return list_result


try:
    with open(sys.argv[CSV_ARG_POS]) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        print(sys.argv[CSV_ARG_POS] + " successfully read in")
    print("Will delete one instance of all cards in " +
          sys.argv[CARDLIST_ARG_POS])
except:
    print("ERROR: csv file could not be read. Please input name of csvs as second arg")
    sys.exit()

collection_file = sys.argv[CSV_ARG_POS]
removal_file = sys.argv[CARDLIST_ARG_POS]

card_list = read_collection_file(collection_file)
removal_list = read_removal_file(removal_file)

for card_name in removal_list:
    card_list = update_card_qty(card_list, card_name)

with open(collection_file, "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["card", "qty", "price"])
    for card in card_list:
        writer.writerow([card[0], card[1], card[2]])
