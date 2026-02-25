import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def get_recommendations(file):

    try:
        # convert uploaded file into pandas dataframe
        df = pd.read_csv(file)

        df.columns = df.columns.str.strip()

        if 'Transaction' not in df.columns or 'Item' not in df.columns:
            return [{
                "if_you_buy": "Invalid CSV format",
                "you_may_buy": "Required columns: Transaction, Item",
                "support": 0,
                "confidence": 0
            }]

        basket = df.pivot_table(index='Transaction',
                                columns='Item',
                                aggfunc=len,
                                fill_value=0)

        basket = (basket > 0).astype(int)

        frequent = apriori(basket, min_support=0.2, use_colnames=True)
        rules = association_rules(frequent, metric="confidence", min_threshold=0.1)

        results = []

        for _, row in rules.iterrows():
            results.append({
                "if_you_buy": list(row['antecedents']),
                "you_may_buy": list(row['consequents']),
                "support": round(row['support'], 2),
                "confidence": round(row['confidence'], 2)
            })

        return results

    except Exception as e:
        return [{
            "if_you_buy": "Error",
            "you_may_buy": str(e),
            "support": 0,
            "confidence": 0
        }]