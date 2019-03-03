# kinect.js

## To run  
Install requirements  
`pip install -r requirements.txt `  
(I might of forgotten something, if you crash add it or raise an issue)

Download data at https://webhose.io/free-datasets/popular-blog-posts/

Preprocess Data
`cd data`
`python parse.py path_to_data`

Train it
`python train.py -rnn_size 512 --data data --seq_length 512`
I don't know how the best parameters, but these worked decently well

Run server on localhost:8000
`python server.py`


based on https://github.com/nawb/chat-rnn-tensorflow
