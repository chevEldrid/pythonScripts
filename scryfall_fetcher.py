import sys
import csv
import requests
import json
import time


class ScryfallFetcher:
    @staticmethod
    def fetch_card_prices(card):
        price = -1
        price_found = False
        VARIATIONS = ["HHO", "CMB1", "CMB2"]
        # this gets almost every card but "non legal ones" have some exceptions...
        try:
            url = "https://api.scryfall.com/cards/search?q=!\"{0}\"&order={1}&unique=prints".format(
                card.get_name(), "name")
            r = requests.get(url)
            x = json.loads(r.text)
            price = card.get_cheapest_scryfall_price(x)
            price_found = True
            time.sleep(.15)
        except:
            time.sleep(.15)
            for set in VARIATIONS:
                try:
                    url = "https://api.scryfall.com/cards/search?q=s%3A{0}+name=!\"{1}\"&order={2}&unique=prints".format(
                        set, card.get_name(), "name")
                    r = requests.get(url)
                    x = json.loads(r.text)
                    card.get_cheapest_scryfall_price(x)
                    price_found = True
                    break
                except:
                    time.sleep(.15)
        if not price_found:
            print("Error, no price could be found for " + card.get_name())
        return price
