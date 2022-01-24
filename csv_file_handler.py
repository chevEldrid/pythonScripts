import csv


class CSVFileHandler:
    def __init__(self, name):
        self.name = name

    def file_exists(self):
        exists = True
        try:
            with open(self.name) as csvfile:
                csv.reader(csvfile, delimiter=',')
        except:
            exists = False
        return exists

    def read_file(self):
        card_list = []
        with open(self.name) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                try:
                    card_list.append((row[0], row[1], row[2]))
                except:
                    print(f"Error on {row[0]}. Will be dropped from Table")
        del card_list[0]
        return card_list

    def write_file(self, card_list):
        with open(self.name, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["card", "qty", "price"])
            for card in card_list:
                writer.writerow([card[0], card[1], card[2]])
