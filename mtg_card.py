class MTGCard:
    def __init__(self, full_name, quantity, price):
        self.full_name = full_name
        self.quantity = int(quantity)
        self.price = float(price)

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

    def print_card(self):
        return (self.full_name, self.quantity, self.price)
