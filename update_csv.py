import sys
import csv
import requests
import json
import time
#google stuff
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

#command line arguments: [-r] - just consolidate, no price pulling
#                        [-p] - just price, don't consolidate
#                        [-g] - rocket that card file to the goog
#                        [-l] - prints more details for debugging
#Ascii codes for colored ouput
class bcolors:
    FAIL = '\033[91m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
#
card_file = ""
out_file = ""
cards = [] #name, qty, price
result_names = [] #list of result card names
result = [] #generated card list
#argv stuff
reprice = True
condense = True
logCards = False
uploadCards = False
#pricing info
bulk_ceiling = 0.99
bulk_rate = 5 #x$/1000 bulk cards
total_value = 0.0
new_value = 0.0
bulk_count = 0
min_delt = 1.00
min_mod = 0.10
def is_float(word):
    temp = False
    try:
        float(word)
        temp = True
    except:
        temp = False
    return temp

#given scryfall api card data, finds paper printing with cheapest price
def cheapest_print(cardData, foil, set_code, col_number):
    printings = cardData["data"]
    prices = []
    #print("col_number selected: "+col_number)
    for price in printings:
        #if foil flag, use foil price
        if foil:
            cardPrice = price["prices"]["usd_foil"]
        else:
            cardPrice = price["prices"]["usd"]
        #special filters
        if price["oversized"] == True:
            continue
        if price["set_type"] == "memorabilia":
            continue
        #if card has no usd price, it might only have a foil price
        if not is_float(cardPrice):
            cardPrice = price["prices"]["usd_foil"]
        if cardPrice != None:
            #if specific collector numnber wanted
            col_num_cleared = False
            if col_number == 0:
                col_num_cleared = True
            elif price["collector_number"].upper() == str(col_number).upper():
                col_num_cleared = True
            #if specific set wanted...
            set_cleared = False
            if set_code == "":
                set_cleared = True
            elif price["set"].upper() == set_code.upper():
                set_cleared = True
            #checks if specific conditions met
            if set_cleared and col_num_cleared:
                prices.append(float(cardPrice))
    return min(prices)

#given card name, pings scryfall for card data
def get_price(card, foil, set_code, col_number):
    price = -1
    card_name = get_name(card)
    if logCards:
        print(str(card_name)+":- GET PRICE")
    try:
        url = "https://api.scryfall.com/cards/search?q=!\"{0}\"&order={1}&unique=prints".format(card_name, "name")
        #print(url)
        r = requests.get(url)
        #print("request got")
        x = json.loads(r.text)
        #pass foil flag to cheapest print
        if logCards:
            print(str(card_name)+":- GET CHEAPEST")
        price = cheapest_print(x, foil, set_code, col_number)
    except:
        print("ERROR ON: " + card)
    time.sleep(.15)
    return price

#given card name, is the card foil
def is_foil(card):
    words = card.split()
    for word in words:
        if word == "*f*":
            return True
    return False

#given card name, gets set code
def get_set_code(card):
    words = card.split()
    for word in words:
        if "[" in word:
            return word[1:-1]
    return ""

#given card name, gets collectors number
def get_collector_number(card):
    words = card.split()
    for word in words:
        if "{" in word:
            return int(word[1:-1])
    return 0

#removes tags given to card name on sheet
def get_name(card):
    words = card.split()
    name = []
    for word in words:
        #if card is foil...
        if word == "*f*":
            continue
        #if card has set code in the form [kld]...
        if "[" in word:
            continue
        #if card had collectors number in form {126}...
        if "{" in word:
            continue
        name.append(word)
    return " ".join(name)

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
    if logCards:
        print('File ID: %s' % file.get('id'))

#---------------------------
#intake output file
try:
    with open(sys.argv[1]) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        print(sys.argv[1] + " successfully read in")
except:
    print("ERROR: csv file could not be read. Please input name of csv as first arg")
    sys.exit()
card_file = sys.argv[1]
out_file = sys.argv[1]
#check for arg about repricing list
if '-r' in sys.argv:
    reprice = False
    print("Will not pull new price data from scryfall")
else:
    print("Will pull new price data from scryfall")
#check for arg about condensing list
if '-p' in sys.argv:
    condense = False
    print("Will not check for consolidation")
else:
    print("Will consolidate all duplicates")
if '-l' in sys.argv:
    logCards = True
    print("Will print more information about processes")
#check for arg about uploading to the goog
if '-g' in sys.argv:
    uploadCards = True
    print("Will upload card file to the goog")
#bring in file with all card information...
with open(card_file) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        try:
            cards.append((row[0], row[1], row[2]))
            #print(row)
        except:
            print("Error on {0}. Will be dropped from Table".format(row[0]))
#create copy of cards list to iterate through and not mess up for loop
del cards[0]
#sort for duplicates
for i, val in enumerate(cards):
    name = val[0]
    qty = int(val[1])
    old_price = float(val[2])
    #if the card hasn't already been found...
    if name not in result_names:
        if reprice:
            foil = is_foil(name)
            set_code = get_set_code(name)
            collector_number = get_collector_number(name)
            price = float(get_price(name, foil, set_code, collector_number))
        else:
            price = float(val[2])
        #iterate through every remaining entry in table, if condensing
        if condense:
            for j in range(i+1, len(cards)):
                if cards[j][0] == name:
                    qty += int(cards[j][1])
        #if there was an error with the price pulling...
        if price > 0:
            result.append((name, qty, price))
            #keep track of new value added since last run (good when uploading a bunch of stuff)
            if old_price == 0 and price > bulk_ceiling:
                new_value += price
            elif old_price == 0 and (price > 0 and price < bulk_ceiling):
                new_value += (1/1000.0*bulk_rate)
            #if there's been a considerable change in price...
            #different conditions if price is sub dollar
            delta = abs(price - old_price)
            min_reached = delta > min_delt
            if min_reached and price >= (1.0 + min_mod) * old_price:
                print(bcolors.OKGREEN+"Spike"+bcolors.ENDC+" on: {0}: From ${1} to ${2} (You have {3})".format(name, old_price, price, qty))
            if min_reached and price <= (1.0 - min_mod) * old_price:
                print(bcolors.FAIL+"Drop"+bcolors.ENDC+" on: {0}: From ${1} to ${2} (You have {3})".format(name, old_price, price, qty))
        else:
            result.append((name, qty, old_price))
        #only add result to result name table if we're preventing duplicate searches
        if condense:
            result_names.append(name)
#sort prices from high to low
result = sorted(result, key=lambda tup: float(tup[2]), reverse=True)
#now print to csv
with open(out_file, "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["card","qty","price"])
    for card in result:
        #generate pricing info...
        if float(card[2]) > bulk_ceiling:
            total_value += (float(card[2]) * int(card[1])) #price * qty
        else:
            bulk_count += int(card[1]) #qty
        writer.writerow([card[0], card[1], card[2]])
collection_value = total_value + (bulk_count/1000.0*bulk_rate)
print("Total collection valued at {0:.2f}, with bulk rated at {1} per thousand".format(collection_value, bulk_rate))
print("New additions valued at {0:.2f}, with same bulk rating. Nice!".format(new_value))
if uploadCards:
    print("Attempting to upload to the Google....")
    #assuming data folder
    upload_to_google(out_file.split('/')[1], out_file, 'text/csv')
    print("Upload successful! Byebye!")