import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
import re
import nltk 
import ktrain
from ktrain import text
from flask  import Flask ,jsonify ,request ,render_template
import pickle


nltk.download('stopwords')
arb_stopwords = set(nltk.corpus.stopwords.words("arabic"))
arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ«»'''
english_punctuations = string.punctuation
punctuations_list = arabic_punctuations + english_punctuations

def remove_punctuations(text):
    return ''.join([char if char  not in punctuations_list else ' ' for char  in text])


def replace_numbers(text):
  numbers=['٩', '٨', '٧', '٦', '٥', '٤', '٣', '٢', '١','٠']
  return ''.join([char for char in text if char not in numbers ])


emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)

def clean(text):
    text=re.sub(r'[a-zA-Z]*',"",text)
    text = re.sub(r'[0-9]*', '', text)
    text=emoji_pattern.sub(' ', text)
    text=replace_numbers(text)
    text = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", text)
    text=text.replace('#',' ')
    text=text.replace('_',' ')
    text=' '.join([word for word in text.split() if word not in arb_stopwords])
    text=remove_punctuations(text)
    text=re.sub('\s+',' ',text)
   

    return text

def clean2(text):
    text=re.sub(r'[^ا-ي]+',' ',text)
    text=' '.join( [w for w in text.split() if len(w)>2] )
    return text      


#test_text = "سئ جدا هدا الفيلم "



loaded_model = ktrain.load_predictor('model_final')



#test_text=clean(test_text)
#test_text=clean2(test_text)
#sentiment=loaded_model.predict(test_text)

#print(sentiment)

app=Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")
    
    
@app.route('/predict',methods=['POST'])
def predict():
    if request.method == "POST":
        message = request.form['submission']
        message_clean=clean(message)
        message_clean=clean2(message_clean)
        classification=loaded_model.predict(message_clean)
        if classification== False:
            classification='Negative'
        else:
             classification='Positive'


        
        print(classification)
        
        

        return render_template('index.html', message=message, classification=classification)
    


if __name__ == '__main__':
    app.run(debug=True)