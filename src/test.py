from datetime import datetime
from pathlib import Path
import os

for folder in os.listdir(Path('./content/projects').resolve()):
    a = Path(folder).resolve()
    for item in os.listdir(a):
        if 
        name = os.path.basename(item).replace('.html', '').replace('_', " ")
       
