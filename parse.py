import json
import os
from langdetect import detect

file = os.walk('./')
text = ''
output_file = 'input.txt'
data_path = '../../full_data'

# for _, sub, files in os.walk(data_path):
# for _, sub, files in os.env('blog_data'):
# for subdir in sub:
subdir = '1'
files = os.listdir(os.path.join(data_path, './%s'%subdir))
# for i in range(0, 600):
for file in files:
    # file = files[i]
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
