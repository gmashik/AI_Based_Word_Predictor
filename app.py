import flask
from flask import Flask, request, render_template
import json
#import main
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np


app = Flask(__name__)
tokenizer = pickle.load(open('tokenizer.pkl', 'rb'))
model=tf.keras.models.load_model('model11.h5',compile=False)
def recommendation(text,model,tokenizer,n):
  token_list = tokenizer.texts_to_sequences([text])[0]
  token_list = pad_sequences([token_list], maxlen=130, padding='pre')
  predicted=model.predict(token_list,verbose=0)[0]
  predicted_index=np.argsort(predicted)[-n:]
  predicted_index=list(predicted_index)
  predicted_index.reverse()
  output=[]
  for i in predicted_index:
    for w,ind in tokenizer.word_index.items():
      if ind==i:
        output.append(w)
        break
  text=""
  text="\n".join(output)
  return text
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
