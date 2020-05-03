from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score


class Similarity():
    fact = ''
    queries = []
    feature_names = []
    scores = []

    def __init__(self, fact, queries):
        self.fact = fact
        self.set_queries(queries)

    def set_queries(self, queries):
        self.queries = queries
        vectors = self.vectorize()
        
        self.scores = []
        for i in range(len(vectors)):
            if i != 0:
                vector = [vectors[i], vectors[0]]
                score = self.similarity_metrics(vector)
                self.scores.append(score)

    def vectorize(self):
        texts = [self.fact]
        for query in self.queries:
            texts.append(query)

        vectorizer = CountVectorizer()
        response = vectorizer.fit_transform(texts)

        feature_names = vectorizer.get_feature_names()
        dense = response.todense()
        denselist = dense.tolist()

        result = {}
        for sentence_idx in range(len(denselist)):
            sentence_result = {}
            for word_idx in range(len(denselist[sentence_idx])):
                sentence_result[feature_names[word_idx]] = denselist[sentence_idx][word_idx]
            result[sentence_idx] = sentence_result

        self.feature_names = feature_names
        return result

    def similarity_metrics(self, vector):
        y_true = []
        y_pred = []
        for feature in self.feature_names:
            y_true.append(vector[1][feature])
            y_pred.append(vector[0][feature])

        score = jaccard_score(y_true, y_pred, average='weighted')
        return score
