import argparse
from reddit.reddit_classes import *
from datetime import *

parser = argparse.ArgumentParser(description='Download useful stories associated with a Reddit JSON file')
parser.add_argument('file')

args = parser.parse_args()

file = args.file

ss = SubredditSnapshot(datetime.now())
ss.load_from_file(file)

