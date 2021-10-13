#Import Libraries and Modules

import re
from collections import Counter
import sys

# Define Functions

"""Your code here"""

# Define Filepaths and Assign Variables

stopwords = """Your code here"""

# When a user runs this Python script from a bash shell, the first argument that they include after the script name will be assigned to this variable. For ex: python my_word_counter.py The-Yellow-Wallpaper.txt
filepath_of_text = sys.argv[1]

# Read in File

text = """Your code here"""

# Manipulate and Analyze File

tokenized_text = make_lower_and_split(text)
meaningful_words = remove_stopwords(tokenized_text)
most_frequent_meaningful_words = get_most_common(meaningful_words)

# Output Results

print(most_frequent_meaningful_words)