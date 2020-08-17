import math
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
import pandas as pd


class FPGrowth():
    transactions = []
    transactions_df = None
    supports = []
    itemsets = []
    confidences = {}
    lifts = {}
    association_rules = []

    def __init__(self, transactions):
        print("Initiating FP Growth Process")
        self.reset()

        print("Setting up the Transactions")
        self.set_transactions(transactions)

        print("Calculating Support")
        self.calculate_support()

        print("Calculating Confidence")
        self.calculate_confidence()

        print("Calculating Lift")
        self.calculate_lift()

        print("Setting up the Association Rules")
        self.set_association_rules()

    def calculate_min_sup(transaction_length):
        a = -0.4
        b = -0.2
        c = 0.2
        x = transaction_length

        ax = a * x
        axb = ax + b
        axbc = axb + c
        return math.exp(axbc)

    def calculate_support(self):
        min_support = FPGrowth.calculate_min_sup(len(self.transactions))
        fp_growth = fpgrowth(self.transactions_df,min_support=min_support, use_colnames=True)
        for row in fp_growth.values.tolist():
            support = row[0]
            row_itemsets = row[1]
            self.supports.append(support)
            self.itemsets.append([item for item in row_itemsets])

    def calculate_confidence(self):
        print(f"Itemsets: {self.itemsets}")
        for association_index in range(len(self.itemsets)):
            if len(self.itemsets[association_index]) > 1:
                try:
                    itemsets = self.itemsets
                    association_itemsets = itemsets[association_index]
                    correlated_itemset = association_itemsets[-1]
                    main_itemset = association_itemsets[:-1]

                    correlated_index = itemsets.index(association_itemsets)
                    main_index = itemsets.index(main_itemset)

                    supports = self.supports
                    confidence = supports[correlated_index] / supports[main_index]

                    self.confidences[association_index] = confidence
                except:
                    print("Terjadi kesalahan pada proses perhitungan Confidence")

    def calculate_lift(self):
        for confidence_index in self.confidences:
            confidence = self.confidences[confidence_index]
            item = [self.itemsets[confidence_index][-1]]
            item_index = self.itemsets.index(item)
            support = self.supports[item_index]
            lift = confidence / support
            self.lifts[confidence_index] = lift

    def set_transactions(self, transactions):
        te = TransactionEncoder()
        encoded_transactions = te.fit(transactions).transform(transactions)
        self.transactions_df = pd.DataFrame(
            encoded_transactions, columns=te.columns_)
        self.transactions = transactions

    def get_transactions(self, is_df=False):
        if is_df:
            return self.transactions_df
        return self.transactions

    def set_association_rules(self):
        for confidence_index in self.confidences:
            confidence = self.confidences[confidence_index]
            itemsets = self.itemsets[confidence_index]
            if len(itemsets) <= 2:
                association_rule = {
                    'main_itemset': itemsets[0],
                    'correlated_itemset': itemsets[-1],
                    'confidence_value': confidence,
                    'support_value': self.supports[confidence_index],
                    'lift_value': self.lifts[confidence_index]
                }
                self.association_rules.append(association_rule)

    def reset(self):
        self.transactions = []
        self.transactions_df = None
        self.supports = []
        self.itemsets = []
        self.confidences = {}
        self.lifts = {}
        self.association_rules = []
