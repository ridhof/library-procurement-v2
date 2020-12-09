# Library Procurement V2

## WEKA
Weka is a tool that helps user to use Machine Learning without any programming experience.
Based on someone else journal, I'd like to describe how WEKA works so that any people can use WEKA easier.

### Preprocess
- Weka provides preprocessing by clicking on `preprocess` tab, and then select the CSV file.
- Don't forget to remove a category that doesn't contain any data.
- Weka might fail on processing data, please be more careful
- User can easily calculate how many attribute are missing in transactions and how many attribute that contained in transactions 

### Associate
- Weka also provides feature to find association rules
- Available methods are Apriori, FilteredAssociation, and FPGrowth
- Apriori has requirements such as minimum support and minimum confidence to be used
- One of way to find corect requirements by trial and error
- Association result can be found on _Associator output_

### Result
Output we looks like:
```text
Minimum support: 0.05 (25 instances)
Minimum metric <confidence>: 0.5
Number of cycles performed: 19

Generated sets of large itemsets:
Size of set of large itemsets L(1): 32
Size of set of large itemsets L(2): 94

Best rules found:
1. Daging_Unggas_Ikan_Telur=Y Buah=Y 42 => Sayuran=Y 31 <conf:(0.74)> lift:(4.24) lev:(0.05) [23] conv:(2.89)
...
10. ...
```
- Weka provides confidence, support, and lift that used to evaluate the association rules
- Weka gives X strongest sorted rules

