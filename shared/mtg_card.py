from shared.utils import is_float


class MTGCard:
    def __init__(self, full_name, quantity, price):
        self.full_name = full_name
        self.quantity = int(quantity)
        self.price = float(price)
        self.name = self.get_name()
        self.foil = self.is_foil()
        self.etched_foil = self.is_etched_foil()
        self.code = self.set_code()
        self.collector_number = self.get_collector_number()

    def get_name(self):
        words = self.full_name.split()
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

    # is the card foil?
    def is_foil(self):
        words = self.full_name.split()
        for word in words:
            if word == "*f*":
                return True
        return False

    # is the card etched foil?
    def is_etched_foil(self):
        words = self.full_name.split()
        for word in words:
            if word == "*ef":
                return True
        return False

    # is this card object set-specific?
    def set_code(self):
        words = self.full_name.split()
        for word in words:
            if "[" in word:
                return word[1:-1]
        return ""

    # does this card contain a collector number?
    def get_collector_number(self):
        words = self.full_name.split()
        for word in words:
            if "{" in word:
                return int(word[1:-1])
        return 0

    def get_cheapest_scryfall_price(self, card_data):
        printings = card_data["data"]
        prices = []
        for price in printings:
            if self.foil:
                cardPrice = price["prices"]["usd_foil"]
            elif self.etched_foil:
                cardPrice = price["prices"]["usd_etched"]
            else:
                cardPrice = price["prices"]["usd"]
            # special filters
            if price["oversized"] == True:
                continue
            if price["set_type"] == "memorabilia":
                continue
            # if card has no usd price, it might only have a foil price
            if not is_float(cardPrice):
                cardPrice = price["prices"]["usd_foil"]
            # if still doesn't have a card price, might be only an etched foil
            if not is_float(cardPrice):
                cardPrice = price["prices"]["usd_etched"]
            if cardPrice != None:
                # if specific collector numnber wanted
                col_num_cleared = False
                if self.collector_number == 0:
                    col_num_cleared = True
                elif price["collector_number"].upper() == str(self.collector_number).upper():
                    col_num_cleared = True
                # if specific set wanted...
                set_cleared = False
                if self.code == "":
                    set_cleared = True
                elif price["set"].upper() == self.code.upper():
                    set_cleared = True
                # checks if specific conditions met
                if set_cleared and col_num_cleared:
                    prices.append(float(cardPrice))
        return min(prices)

    def print_card(self):
        return (self.full_name, self.quantity, self.price)
