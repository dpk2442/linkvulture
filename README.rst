SiteMapper
==========

SiteMapper crawls a given url, and creates a tree of the site. Dead links stop
the crawl, which resumes from the parent. The tree can be reformatted using the
options specified below.

.. code-block:: none

	usage: sitemapper [-h] [-n | -t chars] [-e] [-p] [-m depth] url

	positional arguments:
	  url                   The url to map

	optional arguments:
	  -h, --help            show this help message and exit
	  -n, --no-tree         Use this option to disable the printing of the tree
	  -t chars, --tree chars
	                        Set the characters for the tree. Defaults to "| -- "
	  -e, --errors          Show only errors
	  -p, --parents         Show the parents of pages with errors
	  -m depth, --max-depth depth
	                        Set the max recursion depth. Defaults to infinite.
