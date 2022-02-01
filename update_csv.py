import sys
from datetime import date
from csv_file_handler import CSVFileHandler
from mtg_card import MTGCard
from scryfall_fetcher import ScryfallFetcher
from utils import BASHColors
# google stuff
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

# command line arguments: [-r] - just consolidate, no price pulling
#                        [-p] - just price, don't consolidate
#                        [-g] - rocket that card file to the goog
#                        [-l] - prints more details for debugging
# Ascii codes for colored ouput
CSV_ARG_POS = 1

# customizable fields - use to adjust printout of card price changes
MIN_DELT = 1.00
MIN_MOD = 0.10
BULK_CEILING = 0.99
BULK_RATE = 5  # x$/1000 bulk cards


def upload_to_google(filename, filepath, filetype):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath, mimetype=filetype)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()


def set_command_flags(command_flags):
    # default values
    reprice = condense = upload_cards = True
    log_cards = False

    if '-r' in command_flags:
        reprice = False
        print("Will not pull new price data from scryfall")
    else:
        print("Will pull new price data from scryfall")
    # check for arg about condensing list
    if '-p' in command_flags:
        condense = False
        print("Will not check for consolidation")
    else:
        print("Will consolidate all duplicates")
    if '-l' in command_flags:
        log_cards = True
        print("Will print more information about processes")
    # check for arg about uploading to the goog
    if '-g' in command_flags:
        upload_cards = True
        print("Will upload card file to the goog")
    # bring in file with all card information...
    return [reprice, condense, log_cards, upload_cards]


def main():
    card_file = sys.argv[CSV_ARG_POS]
    out_file = sys.argv[CSV_ARG_POS]
    csv_file_reader = CSVFileHandler(card_file)

    if(csv_file_reader.file_exists()):
        print(f"{card_file} successfully read in.")
    else:
        print("ERROR: csv file could not be read. Please input csv as first argument")
        sys.exit()

    # set command line flags
    reprice, condense, log_cards, upload_cards = set_command_flags(sys.argv)
    # read in card file
    cards = csv_file_reader.read_file()

    result = []
    result_names = []
    new_value = 0.0
    for i, val in enumerate(cards):
        card = MTGCard(val[0], val[1], val[2])
        # if the card hasn't already been found...
        if card.name not in result_names:
            if reprice:
                price = ScryfallFetcher.fetch_card_prices(card)
            else:
                price = float(card.price)
            # iterate through every remaining entry in table, if condensing
            if condense:
                for j in range(i+1, len(cards)):
                    if cards[j][0] == card.name:
                        card.quantity += int(cards[j][1])
            # if there was an error with the price pulling...
            if price > 0:
                result.append((card.name, card.quantity, price))
                # keep track of new value added since last run (good when uploading a bunch of stuff)
                if card.price == 0 and price > BULK_CEILING:
                    new_value += price
                elif card.price == 0 and (price > 0 and price < BULK_CEILING):
                    new_value += (1/1000.0*BULK_RATE)
                # if there's been a considerable change in price...
                # different conditions if price is sub dollar
                delta = abs(price - card.price)
                min_reached = delta > MIN_DELT
                if min_reached and price >= (1.0 + MIN_MOD) * card.price:
                    print(
                        f"{BASHColors.OKGREEN}Spike{BASHColors.ENDC} on: {card.name}: From ${card.price} to {price} (You have {card.quantity})")
                if min_reached and price <= (1.0 - MIN_MOD) * card.price:
                    print(
                        f"{BASHColors.FAIL}Drop{BASHColors.ENDC} on: {card.name}: From ${card.price} to ${price} (You have {card.quantity})")
            else:
                result.append((card.name, card.quantity, card.price))
            # only add result to result name table if we're preventing duplicate searches
            if condense:
                result_names.append(card.name)

    # sort prices from high to low
    result = sorted(result, key=lambda tup: float(tup[2]), reverse=True)
    # generate statistics
    total_value = 0.0
    bulk_count = 0
    for card in result:
        if float(card[2]) > BULK_CEILING:
            total_value += (float(card[2]) * int(card[1]))  # price * qty
        else:
            bulk_count += int(card[1])  # qty

    csv_file_reader.write_file(result)

    collection_value = total_value + (bulk_count/1000.0*BULK_RATE)
    print("Total collection valued at {0:.2f}, with bulk rated at {1} per thousand".format(
        collection_value, BULK_RATE))
    print("New additions valued at {0:.2f}, with same bulk rating. Nice!".format(
        new_value))
    if upload_cards:
        print("Attempting to upload to the Google....")
        # assuming data folder
        googFileName = out_file.split('/')[1] + str(date.today())
        upload_to_google(out_file.split('/')[1], out_file, 'text/csv')
        print("Upload successful! Byebye!")


if __name__ == "__main__":
    main()
