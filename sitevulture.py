#!/usr/bin/python3

from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import os, re, argparse

IS_LOCAL          = None
IS_VALID_URL      = re.compile("^https?://")
EMPTY_OUTPUT_LINE = None

args = None

VISITED = []

class Site(object):

	def __init__(self, url, remote=False, depth=0):
		self.url = url
		VISITED.append(url)
		try:
			resp = urlopen(url)
		except HTTPError as e:
			self.code = e.code
			self.children = None
			return
		if remote or depth >= args.max_depth:
			self.code = resp.getcode()
			self.children = None
			return
		self.url = resp.geturl()
		self.code = resp.getcode()
		self.children = []
		soup = BeautifulSoup(resp.read())
		toProcess = []
		for link in soup.find_all("a"):
			link = link.get("href")
			theURL = urljoin(self.url, link)
			if theURL not in VISITED and IS_VALID_URL.match(theURL) != None:
				toProcess.append(theURL)
				VISITED.append(theURL)		
		for theURL in toProcess:
			self.children.append(Site(theURL, IS_LOCAL.match(theURL) == None, depth + 1))

	def has404Children(self):
		if self.children:
			for child in self.children:
				if child.code != 200:
					return True
				else:
					if child.has404Children():
						return True
		return False

	def __str__(self):
		ret = ""
		if self.code != 200 or not args.errors or (args.parents and self.has404Children()):
			ret += str(self.code) + " => " + self.url
		if self.children:
			for child in self.children:
				carr = str(child).split("\n")
				carr = [i for i in carr if EMPTY_OUTPUT_LINE.match(i) == None]
				carr.insert(0, "")
				ret += ("\n" + args.tree).join(carr)
		return ret

def main():
	global IS_LOCAL, EMPTY_OUTPUT_LINE, args
	if args.url[:4] != "http":
		args.url = "http://" + args.url
	try:
		resp = urlopen(args.url)
		args.url = resp.geturl()
	except HTTPError as e:
		print("The page returned a " + e.code + " error.")
		exit(1)
	IS_LOCAL = re.compile(r"^" + os.path.dirname(args.url))
	if args.no_tree:
		args.tree = ""
	EMPTY_OUTPUT_LINE = re.compile(r"^(" + args.tree + r")*$")
	site = Site(args.url)
	print(site)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	tree_group = parser.add_mutually_exclusive_group()
	tree_group.add_argument("-n", "--no-tree", action="store_true", help="Use this option to disable the printing of the tree")
	tree_group.add_argument("-t", "--tree", metavar="chars", default="| -- ", help="Set the characters for the tree. Defaults to \"| -- \"")
	parser.add_argument("-e", "--errors", action="store_true", help="Show only errors")
	parser.add_argument("-p", "--parents", action="store_true", help="Show the parents of pages with errors")
	parser.add_argument("-m", "--max-depth", type=int, metavar="depth", default=float("inf"), help="Set the max recursion depth. Defaults to infinite.")
	parser.add_argument("url", help="The url to map")
	args = parser.parse_args()
	main()