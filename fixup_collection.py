import sys

from shared.csv_file_handler import CSVFileHandler
# Given two csv files, moves all cards above one threshold to the first file, and all below to the other...
# ---------------------------
# intake output file
BULK_CEILING = 0.99

VALUED_CSV_ARG_POS = 1
BULK_CSV_ARG_POS = 1


def filter_lists(valued, bulk):
    adjusted_valued = []
    adjusted_bulk = []
    total_cards = valued + bulk
    for i, val in enumerate(total_cards):
        name = val[0]
        qty = val[1]
        price = float(val[2])
        # if the card hasn't already been found...
        if price > BULK_CEILING:
            adjusted_valued.append((name, qty, price))
        else:
            adjusted_bulk.append((name, qty, price))

    return [adjusted_valued, adjusted_bulk]


def main():
    valued_file = sys.argv[1]
    bulk_file = sys.argv[2]
    valued_file_reader = CSVFileHandler(valued_file)
    bulk_file_reader = CSVFileHandler(bulk_file)

    if(valued_file_reader.file_exists() and bulk_file_reader.file_exists()):
        print(f"{valued_file} and {bulk_file} successfully read in, values will be stored as VALUED and BULK accordingly")
    else:
        print(f"{valued_file} and {bulk_file} could not be read in as VALUED and BULK accordingly. Exiting.")
        sys.exit()

    valued = valued_file_reader.read_file()
    bulk = bulk_file_reader.read_file()

    valued, bulk = filter_lists(valued, bulk)

    # sort prices from high to low
    valued = sorted(
        valued, key=lambda tup: float(tup[2]), reverse=True)
    bulk = sorted(
        bulk, key=lambda tup: float(tup[2]), reverse=True)
    # now print to csv
    valued_file_reader.write_file(valued)
    bulk_file_reader.write_file(bulk)

    print("Bulk successfully sorted. Have a pleasant day")


if __name__ == "__main__":
    main()
