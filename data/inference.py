import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.layers import Dropout
import re
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from nltk.corpus import stopwords
from nltk import word_tokenize
from keras.layers import Bidirectional
from sklearn.model_selection import train_test_split
from keras import Model, Input
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dense, Embedding, CuDNNLSTM, Dropout, TimeDistributed, Reshape, Activation, Dot
from keras.layers.wrappers import Bidirectional
import numpy as np 
import pandas as pd
import random
import matplotlib.pyplot as plt; plt.rcdefaults()
from keras.models import load_model
#from IPython.core.display import display, HTML
import os
#os.chdir('/home/asus/mik_project/data')

class SentimentInference:
  def __init__(self,data,model):
    model1=f"./data/{model}"
    data1=f"./data/{data}"

    self.model=load_model(model1)
    self.data=pd.read_excel(data1)


    #self.data = self.data.dropna(how='any',axis=0) 
    #self.text_tokens = [text.split(" ") for text in self.data["Text"].values.tolist()]
    self.data.Text=self.data.Text.astype(str)
    self.text = self.data["Text"].values.tolist()
    self.labels = self.data["sentiment_type"].values.tolist()
    tokenizer = Tokenizer(num_words=20000, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
    tokenizer.fit_on_texts(self.text)
    self.word2id= tokenizer.word_index
    self.id2word = dict([(value, key) for (key, value) in self.word2id.items()])
    self.vocab_size = len(self.word2id) + 1
    self.embedding_dim = 128
    self.max_len = 85

  def predict(self,text):
    ########

    tokenizer = Tokenizer(num_words=20000, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
    seq = tokenizer.texts_to_sequences(text)
    padded = pad_sequences(seq, maxlen=self.max_len)
    label_probs = self.model.predict(padded)
    print(label_probs.shape)
    ls=label_probs.tolist()
    final_dict={}
    sen_label=['negative','positive','neutral']
    for i,k in zip(label_probs[0],sen_label):
      final_dict[k]=i
    return ls
