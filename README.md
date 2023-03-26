### HAI (Cooking Setting)

##### Generate Data
 
Instruction:
	1. please put the raw dataset (csv) in the file 'raw'
	2. In terminal, cd to the directory of the file (generator), and run the command line 
	replace the file name and its directory
	3. The generated dataframes would be appeared in the file 'processed'

Requirement:
	import pandas as pd
	from tqdm import tqdm
	import numpy as np
	import json
	import ast

Command (paste it to the terminal):
	python -m main --file=./raw/raw-intervention-final.csv  
