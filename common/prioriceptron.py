import numpy as np
import pandas as pd
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


class Prioriceptron():
    priorities = {}

    def __init__(self, transactions):
        print("Initiating Perceptron")
        self.reset()

        print("Setting up the transactions")
        df = self.set_transactions(transactions)

        print("Setting up the features and labels (X & Y)")
        transaksi_X, transaksi_Y, df_y = self.set_XY(df)

        print("Calculating priority using Perceptron")
        priorities = self.calculate_priority(transaksi_X, transaksi_Y, df_y)

        print("Setting up the Priorities Result")
        self.priorities = self.set_priorities(priorities)

    def reset(self):
        self.transactions = []
        self.priorities = {}

    def set_transactions(self, transactions):
        vectorizer = CountVectorizer()
        response = vectorizer.fit_transform(transactions)

        features = vectorizer.get_feature_names()
        dense = response.todense()
        denselist = dense.tolist()
        result = []
        for row_idx in range(len(denselist)):
            row_result = []
            for col_idx in range(len(denselist[row_idx])):
                row_result.append(denselist[row_idx][col_idx])
            result.append(row_result)

        df = pd.DataFrame(result, columns=features)
        return df

    def set_XY(self, df):
        df_copy = df.copy(deep=True)
        features_end_index = df_copy.shape[1]

        global_top_cluster_id = []
        top_cluster_id = []
        for row in df.iterrows():
            sorted_row = row[1].sort_values(ascending=False)
            row_top_cluster = [index for index in sorted_row[:10].index]
            top_cluster_id.append(row_top_cluster)
            global_top_cluster_id.extend(row_top_cluster)
        global_top_cluster_id = list(set(global_top_cluster_id))

        transaksi_Y = []
        for global_index in range(len(global_top_cluster_id)):
            looping_top_cluster = global_top_cluster_id[global_index]
            is_anys = []

            for local_index in range(len(top_cluster_id)):
                top_cluster_row = top_cluster_id[local_index]
                is_any = 0

                if looping_top_cluster in top_cluster_row:
                    is_any = 1
                is_anys.append(is_any)
            transaksi_Y.append(np.array(is_anys))
            df_copy[f"is_{looping_top_cluster}"] = is_anys

        transaksi_X = df.values
        df_y = df_copy.iloc[:, features_end_index:]
        return (transaksi_X, transaksi_Y, df_y)

    def calculate_priority(self, transaksi_X, transaksi_Y, df_y):
        priorities = {}
        for top_index in range(len(transaksi_Y)):
            try:
                # Create training / test split
                X_train, X_test, Y_train, Y_test = train_test_split(
                    transaksi_X,
                    transaksi_Y[top_index],
                    test_size=0.5,
                    random_state=1,
                    stratify=transaksi_Y[top_index]
                )

                # Perform feature scaling
                sc = StandardScaler()
                sc.fit(X_train)
                X_train_std = sc.transform(X_train)
                X_test_std = sc.transform(X_test)
                transaksi_X_std = sc.transform(transaksi_X)

                # Fit / train the model
                ppn = Perceptron(eta0=0.1, random_state=1)
                ppn.fit(X_train_std, Y_train)

                # Check the accuracy of the model
                Y_predict_std = ppn.predict(X_test_std)
                print(f"{df_y.columns[top_index].split('_')[1]} has Accuracy Score %.3f" % accuracy_score(Y_test, Y_predict_std))

                # Predict the rest
                transaksi_label = ppn.predict(transaksi_X_std)
                print(f"{df_y.columns[top_index].split('_')[1]} has {len(transaksi_label)} label {transaksi_label}")

                amount = 0
                for label in transaksi_label:
                    if label == 1:
                        amount = amount + 1
                priority = amount / len(transaksi_label)
                print(f"Priority of {df_y.columns[top_index].split('_')[1]} is {priority}")
                priorities[df_y.columns[top_index].split('_')[1]] = priority
            except:
                print(f"{df_y.columns[top_index].split('_')[1]} has too small sample, skipping current loop")
        return priorities
    
    def set_priorities(self, priorities):
        priorities_result = []
        for cluster_id in priorities:
            itemset = {
                'cluster_id': cluster_id,
                'priority_value': priorities[cluster_id]
            }
            priorities_result.append(itemset)
        return priorities_result
