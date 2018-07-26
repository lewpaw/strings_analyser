#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title: Simple strings statistical anazyer
Author: Pawel (infosec.pawel@gmail.com)
Description:  This tool does basic statistsical analysis of word and phrases.

Licence: Apache 2.0

Instructions: analyze -h or just ask
Tip: for 'good' wordfile, use some english books or false positives you already have, or if you analyze binaries, take strings dump from benign file this type (eg. bunch of PDFs or executables)
Example of use:
./analyze.py ./emails/bad/* --min 10 --max 30 --nocase --nopunct --good ./emails/good/out.txt


Feedback, bug reports: Create an issue on github or drop me an email
"""

import argparse
import html2text
import json
import pprint
import string

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='')
parser.add_argument("source", help="source text file or directory containig textfiles treated as \"bad\".", nargs='+')
parser.add_argument("--good", help="source text file or directory containig textfiles treated as \"good\".", nargs='+')
parser.add_argument("--nocase", help="if set, then all strings will NOT be changed to lower case",  action='store_false')
parser.add_argument("--nopunct", help="if set, then punctuation will NOT be removed",  action='store_false')
parser.add_argument("--nohtml", help="if set, then html tags will NOT be removed",  action='store_false', default=True)
parser.add_argument("--min", help="minimal phrase length to take into consideration (default 1)", nargs='?', default=1)
parser.add_argument("--max", help="maximal phrase length to take into consideration (default 10)", nargs='?', default=10)
parser.add_argument("--top", help="numbers of results to display (default 10)", nargs='?', default=10)


args = parser.parse_args()

QUOTE_MIN_LENGTH = int(args.min)
QUOTE_MAX_LENGTH = int(args.max)
TOP_VALUES = int(args.top)

### preparing files

phrases = {}

# processing bad

for filename in args.source:
	f = open(filename, "r")
	lines = f.readlines()

	for line in lines:
		if args.nohtml:
			line = html2text.html2text(line)
		if args.nopunct:
			table = str.maketrans({key: None for key in string.punctuation})  
			line = line.translate(table)
		if args.nocase:
			line = line.lower()
		words = line.split()
		
		
		for length in range(QUOTE_MIN_LENGTH, QUOTE_MAX_LENGTH+1):
			
			for i in range(0, len(words)-length):
				phrase=''
				for j in range(0, length):
					phrase+=words[i+j]+' '
				if not phrase in phrases:
					phrases[phrase] = 1
				else:
					phrases[phrase] += 1

# processing good
if args.good:
	for filename in args.good:
		f = open(filename, "r")
		
		lines = f.readlines()

		for line in lines:
			if args.nohtml:
				line = html2text.html2text(line)
			if args.nopunct:
				table = str.maketrans({key: None for key in string.punctuation})  
				line = line.translate(table)
			if args.nocase:
				line = line.lower()
			words = line.split()
			
			
			for length in range(QUOTE_MIN_LENGTH, QUOTE_MAX_LENGTH+1):
				
				for i in range(0, len(words)-length):
					phrase=''
					for j in range(0, length):
						phrase+=words[i+j]+' '
					if not phrase in phrases:
						phrases[phrase] = -10
					else:
						phrases[phrase] -= 10
					
sorted_by_value = [(k, phrases[k]) for k in sorted(phrases, key=phrases.get, reverse=True)][:TOP_VALUES]
for k, v in sorted_by_value:
	print("Quote: "+k+" Score: "+str(v))
    
