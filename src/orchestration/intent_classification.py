from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

class IntentClassifier:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()
        self.intents = []

    def train(self, training_data, training_labels):
        X_train = self.vectorizer.fit_transform(training_data)
        self.model.fit(X_train, training_labels)
        self.intents = list(set(training_labels))

    def predict(self, query):
        query_vector = self.vectorizer.transform([query])
        predicted_intent = self.model.predict(query_vector)
        return predicted_intent[0]

    def save_model(self, model_path):
        joblib.dump((self.vectorizer, self.model), model_path)

    def load_model(self, model_path):
        self.vectorizer, self.model = joblib.load(model_path)