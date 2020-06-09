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
        self.reset()
        self.set_transactions(transactions)
        self.calculate_support()
        self.calculate_confidence()
        self.calculate_lift()
        self.set_association_rules()

    def calculate_support(self):
        fp_growth = fpgrowth(self.transactions_df,
                             min_support=0.6, use_colnames=True)
        for row in fp_growth.values.tolist():
            support = row[0]
            row_itemsets = row[1]
            self.supports.append(support)
            self.itemsets.append([item for item in row_itemsets])

    def calculate_confidence(self):
        for association_index in range(len(self.itemsets)):
            if len(self.itemsets[association_index]) > 1:
                itemsets = self.itemsets
                association_itemsets = itemsets[association_index]
                correlated_itemset = association_itemsets[-1]
                main_itemset = association_itemsets[:-1]

                correlated_index = itemsets.index(association_itemsets)
                main_index = itemsets.index(main_itemset)

                supports = self.supports
                confidence = supports[correlated_index] / supports[main_index]

                self.confidences[association_index] = confidence

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
