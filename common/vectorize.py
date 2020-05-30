from sklearn.feature_extraction.text import CountVectorizer


class Vectorize():
    texts = []
    vectors = []
    features = []

    def __init__(self, texts):
        self.texts = texts
        self.vectorize()
    
    def vectorize(self):
        vectorizer = CountVectorizer()
        response = vectorizer.fit_transform(self.texts)

        self.features = vectorizer.get_feature_names()
        dense = response.todense()
        denselist = dense.tolist()

        result = []
        for sentence_idx in range(len(denselist)):
            sentence_result = []
            for word_idx in range(len(denselist[sentence_idx])):
                sentence_result.append(denselist[sentence_idx][word_idx])
            result.append(sentence_result)

        self.vectors = result
