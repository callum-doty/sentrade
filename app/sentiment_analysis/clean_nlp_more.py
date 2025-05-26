import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer,PorterStemmer
from nltk.corpus import stopwords
import re
import polars as pl
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob 
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer() 
df = pl.read_csv('apple_reviews.csv')
def preprocess(sentence):
    sentence=str(sentence)
    sentence = sentence.lower()
    sentence=sentence.replace('{html}',"") 
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', sentence)
    rem_url=re.sub(r'http\S+', '',cleantext)
    rem_num = re.sub('[0-9]+', '', rem_url)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(rem_num)  
    filtered_words = [w for w in tokens if len(w) > 2 if not w in stopwords.words('english')]
    stem_words=[stemmer.stem(w) for w in filtered_words]
    lemma_words=[lemmatizer.lemmatize(w) for w in stem_words]
    return " ".join(filtered_words)


nlp = spacy.load("en_core_web_sm")

nlp.add_pipe("spacytextblob")
def get_subjectivity(text):
    doc = nlp(text)
    return doc._.blob.subjectivity

def get_polarity(text):
    doc = nlp(text)
    return doc._.blob.polarity
df = df.with_columns(
    pl.col("description").map_elements(preprocess).alias("cleaned_text"),
    pl.col("cleaned_text").map_elements(get_subjectivity).alias("subjectivity"),
    pl.col("cleaned_text").map_elements(get_polarity).alias("polarity"),

)


