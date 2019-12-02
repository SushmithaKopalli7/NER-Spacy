import pandas as pd

# return the wordnet object value corresponding to the POS tag
from nltk.corpus import wordnet
import string
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# create doc2vec vector columns
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# add tf-idfs columns
from sklearn.feature_extraction.text import TfidfVectorizer

class reviewModel:
    def __int__(self):
        self.value="process successful"
    def process(self,path=None):
        # read data
        reviews_df = pd.read_csv(path)
        # append the positive and negative text reviews
        reviews_df["review"] = reviews_df["Negative_Review"] + reviews_df["Positive_Review"]
        # create the label
        reviews_df["is_bad_review"] = reviews_df["Reviewer_Score"].apply(lambda x: 1 if x < 5 else 0)
        #reviews_df["is_good_review"] = reviews_df["Reviewer_Score"].apply(lambda x: 1 if x <= 5 else 0)
        # select only relevant columns
        reviews_df = reviews_df[["review", "is_bad_review"]]
        #reviews_df = reviews_df[["review", "is_good_review"]]
        print("printing reviews_df.head()------------------------------------------------------------------->")
        print(reviews_df.head())

        reviews_df = reviews_df.sample(frac = 0.1, replace = False, random_state=42)

        # remove 'No Negative' or 'No Positive' from text
        reviews_df["review"] = reviews_df["review"].apply(lambda x: x.replace("No Negative", "").replace("No Positive", ""))

        def get_wordnet_pos(pos_tag):

            if pos_tag.startswith('J'):
                return wordnet.ADJ
            elif pos_tag.startswith('V'):
                return wordnet.VERB
            elif pos_tag.startswith('N'):
                return wordnet.NOUN
            elif pos_tag.startswith('R'):
                return wordnet.ADV
            else:
                return wordnet.NOUN
        def clean_text(text):

            # lower text
            text = text.lower()
            # tokenize text and remove puncutation
            text = [word.strip(string.punctuation) for word in text.split(" ")]
            # remove words that contain numbers
            text = [word for word in text if not any(c.isdigit() for c in word)]
            # remove stop words
            stop = stopwords.words('english')
            text = [x for x in text if x not in stop]
            # remove empty tokens
            text = [t for t in text if len(t) > 0]
            # pos tag text
            pos_tags = pos_tag(text)
            # lemmatize text
            text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
            # remove words with only one letter

            text = [t for t in text if len(t) > 1]
            # join all
            text = " ".join(text)
            return(text)

        # clean text data
        reviews_df["review_clean"] = reviews_df["review"].apply(lambda x: clean_text(x))



        sid = SentimentIntensityAnalyzer()
        reviews_df["sentiments"] = reviews_df["review"].apply(lambda x: sid.polarity_scores(x))
        reviews_df = pd.concat([reviews_df.drop(['sentiments'], axis=1), reviews_df['sentiments'].apply(pd.Series)], axis=1)

        # add number of characters column
        reviews_df["nb_chars"] = reviews_df["review"].apply(lambda x: len(x))

        # add number of words column
        reviews_df["nb_words"] = reviews_df["review"].apply(lambda x: len(x.split(" ")))



        documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(reviews_df["review_clean"].apply(lambda x: x.split(" ")))]

        # train a Doc2Vec model with our text data
        model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)

        # transform each document into a vector data
        doc2vec_df = reviews_df["review_clean"].apply(lambda x: model.infer_vector(x.split(" "))).apply(pd.Series)
        doc2vec_df.columns = ["doc2vec_vector_" + str(x) for x in doc2vec_df.columns]
        reviews_df = pd.concat([reviews_df, doc2vec_df], axis=1)


        tfidf = TfidfVectorizer(min_df = 10)
        tfidf_result = tfidf.fit_transform(reviews_df["review_clean"]).toarray()
        tfidf_df = pd.DataFrame(tfidf_result, columns = tfidf.get_feature_names())
        tfidf_df.columns = ["word_" + str(x) for x in tfidf_df.columns]
        tfidf_df.index = reviews_df.index
        reviews_df = pd.concat([reviews_df, tfidf_df], axis=1)

        print(reviews_df.head())
        print(reviews_df.shape)
        print("------------------------------------------------------------------------->")
        print(reviews_df[reviews_df["nb_words"] >= 5].sort_values("pos", ascending=False)[["review", "pos"]].head(10))
        print(reviews_df["is_bad_review"].value_counts(normalize = True))




        # highest positive sentiment reviews (with more than 5 words)
        #print(reviews_df[reviews_df["nb_words"] >= 5].sort_values("pos", ascending = False)[["review", "pos"]].head(10))
        self.value="process completed successfully"
        return reviews_df[reviews_df["nb_words"] >= 5].sort_values("pos", ascending=False)[["review", "pos"]].head(10)

