#!/usr/bin/python

import sys, getopt
import re

begin_tag = '\n<a\n\tclass="accented-link"\n\ttarget="_blank"\n\thref=""\n\tdata-toggle="popover"\n\tdata-placement="top"\n\tdata-content="<img src=\'\' width=100% height=100%>">\n\t'
end_tag = '\n</a>'


def format_line(line):
    result = ''
    #check to see if line even has any cards in it. Otherwise just return
    if "[[" in line:
        result = line.replace('[[', begin_tag).replace(']]', end_tag)
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
       print(line)
   input_file.close()
   output_file.close()

if __name__ == "__main__":
   main(sys.argv[1:])