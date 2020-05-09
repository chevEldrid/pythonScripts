Welcome to the wonderous world of random scripts!
The virtual environment will be: scriptCollection

Scripts:
# articleGenerator.py
articleGenerator.py -i <inputfile>

Article Generator replaces all instances of mtg cards [[In Brackets]] with the appropriate anchor tags to allow hovering. All links lead to scryfall.
Errors printed to console and given anchor tags with no hrefs

# update_csv.py
update_csv.py <inputfile> [-r] [-p]

Update CSV is part of a couple scripts that help keep track of your mtg collection. Runs on a given .csv and pulls all price data from scryfall, printing any big changes in price

[-r] prevents price pulling, but will consolidate multiple copies of a card if they're found on different rows
[-p] doesn't consolidate but pulls prices. I don't really know why this option exists but it seemed a good idea at the time...

Program will also print a collection valuation at the end, with an adjustable "price ceiling" and "bulk rate" to fit current market trends

The % change in price to produce a print to console can also be adjusted

# delete_card.py
delete_card.py "card name" <inputfile>

To prevent needing to dig too much into the CSVs, especially for deletion - deletes one copy of a card from csv, or prints error if card not found

# fixup_collection.py
fixup_collection.py <valuefile> <bulkfile>

If you're like me and want to keep value cards separate from bulk, after you update prices you might find some cards slipping below the bulk threshold in your value collection and vice-versa. Running this script will automatically sort based on a variable "BULK_CEILING" and then sorting each by price
