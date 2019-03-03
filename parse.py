import json
import os
from langdetect import detect

file = os.walk('./')
text = ''
output_file = 'data/input.txt'
data_path = '/'

files = os.listdir(os.path.join(data_path, './%s'%subdir))
for file in files:
    path = os.path.join(data_path, subdir, file)
    with open(path) as json_data:
        d = json.load(json_data)
        file_text = d['text']
        try:
            lang = detect(file_text)
        except:
            continue
        if lang == "en":
            text += file_text

with open(output_file, 'w+') as f:
    f.write(text)
