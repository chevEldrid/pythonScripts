import sys
import shutil

from shared.csv_file_handler import CSVFileHandler

TXT_ARG_POS = 1

# gets name and quantity of card assuming quantity is read in as '5x Thing'


def extract_card(line):
    split_line = line.split()
    quantity = split_line[0].split('x')[0]
    del split_line[0]
    name = " ".join(split_line)
    return [name, quantity]


def read_collection_file(file):
    cards_to_load = []
    with open(file) as txtfile:
        lines = txtfile.readlines()
        for line in lines:
            # this script assumes cards are listed as such:
            # 2x Island
            name, quantity = extract_card(line)
            cards_to_load.append([name, quantity, 0.0])
    return cards_to_load


def main():
    cards_file = sys.argv[TXT_ARG_POS]
    output_file = cards_file.split("data/")[1]
    # strip file extension and add identifier
    output_file = (output_file.split(".")[0] + ".csv")

    cards = read_collection_file(cards_file)
    output_file_reader = CSVFileHandler(output_file)
    output_file_reader.write_file(cards)
    print(f"{output_file} created, all cards loaded with price 0")
    shutil.move(output_file, 'data/')


if __name__ == "__main__":
    main()
