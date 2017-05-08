# Introduction
Implementation of AKE (http://www.tiernok.com/posts/automated-keyword-extraction-tf-idf-autoke-and-textrank.html)

# Usage
```
from autoke.autoke import Engine, StopList


test_text = '...'

stop_list = StopList('data/stoplist.txt')
engine = Engine(stop_list)

print engine.analyse(test_text)
```

# Stoplists

A list of stop-words to be removed from the text, to yield better results.