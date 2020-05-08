#!/usr/bin/python

import sys, getopt
import re
import requests
import json
import time


anchor_tag = '\n<a\n\tclass="accented-link"\n\ttarget="_blank"\n\thref="{0}"\n\tdata-toggle="popover"\n\tdata-placement="top"\n\tdata-content="<img src=\'{1}\' width=100% height=100%>">\n\t{2}\n</a>'

#returns a 2-element array with card uri on scryfall, and the image uri
def get_card_data(name):
    card_uri = ''
    image_uri = ''
    try:
        url = "https://api.scryfall.com/cards/search?q=!\"{0}\"".format(name)
        #print(url)
        r = requests.get(url)
        #print("request got")
        x = json.loads(r.text)
        card = x["data"][0]
        card_uri=card["scryfall_uri"]
        image_uri=card["image_uris"]["normal"]
    except:
        print("ERROR PROCESSING: " + card)
    #prevent bothering scryfall too much
    time.sleep(.15)
    return [card_uri, image_uri]

def format_line(line):
    result = ''
    #check to see if line even has any cards in it. Otherwise just return
    if "[[" in line:
        card_count = line.count("[[")
        print('card count: '+str(card_count))
        for n in range(card_count):
            card_name = re.search("\[\[(.*?)\]\]", line).group(1)
            card_data = get_card_data(card_name)
            card_tag = anchor_tag.format(card_data[0], card_data[1], card_name)
            line = re.sub("\[\[(.*?)\]\]", card_tag, line, 1)
        #result = line.replace('[[', begin_tag).replace(']]', end_tag)
        result = line
    else:
        result = line
    return result

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
      print('Error: articleGenerator.py -i <inputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('articleGenerator.py -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   print('Input file is '+ inputfile)
   outputfile = (inputfile.split('.')[0] + "_formatted.md")
   print('Output file is '+outputfile)
   #proceed to read input file
   input_file = open(inputfile, "r")
   output_file = open(outputfile, "w")
   for line in input_file:
       output_file.write(format_line(line))
   input_file.close()
   output_file.close()

if __name__ == "__main__":
   main(sys.argv[1:])