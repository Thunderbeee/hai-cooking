Instructions:
	1. Please put the raw dataset (.csv format) in the folder 'raw'
	2. In terminal, cd into the directory of the current folder (generator), and run the command (see below)
	3. The generated dataframes would be appeared in the folder 'processed'

Requirements:
	import pandas as pd
	from tqdm import tqdm
	import numpy as np
	import json
	import ast

Command (paste it to the terminal):
	python -m main --file=./raw/name-of-raw-file.csv 

# Change the file name and directory name whenever necessary