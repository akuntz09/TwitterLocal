import json
import nltk
import string
from pprint import pprint
from collections import Counter
from nltk.corpus import stopwords as sw
from string import maketrans
import unicodedata

def makeDataString(filePath):
  data = []
  with open(filePath) as f:
    for line in f:
      data.append(json.loads(line))
  textString = ''
  for entry in data:
    textString += (entry['text'])
  return textString

def countKeywords(textString):
  lower_string = textString.lower()
  lower_string = unicodedata.normalize('NFKD', lower_string).encode('ascii', 'ignore')
  noPunctuation = lower_string.translate(string.maketrans('',''), string.punctuation)
  tokens = nltk.word_tokenize(noPunctuation)
  filtered = [w for w in tokens if not w in sw.words('english')]
  count = Counter(filtered)
  return count

global_trump1 = countKeywords(makeDataString('trumpGlobalNoRT.json'))
local_trump1 = countKeywords(makeDataString('trumpLocalFiltered.json'))
global_nfl = countKeywords(makeDataString('nflGlobalNoRT.json'))
local_nfl = countKeywords(makeDataString('nflLocalFiltered.json'))

print global_trump1.most_common(30)
print local_trump1.most_common(30)
print global_nfl.most_common(30)
print local_nfl.most_common(30)
