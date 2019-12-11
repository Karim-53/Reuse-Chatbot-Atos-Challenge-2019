#!/usr/bin/env python

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori




def association_rule(contenu, dataset, map):
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset) # TODO: nefehmou el fit wel transform 5ater y7ebou explication
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.6, use_colnames=True)

    #frequent_itemsets

    from mlxtend.frequent_patterns import association_rules

    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
    rules["antecedent_len"] = rules["antecedents"].apply(lambda x: len(x))
    #rules
    
    tab=rules[['consequents','confidence']].drop_duplicates().sort_values(by=['confidence'],ascending=False)
    #tab
    
    
    #ajouter le mappage entre la publication et le contenu de l'image
    
    result=[]
    
    for index, row in tab.iterrows():
        #sets=list(rules["consequents"][2])
        sets=list(row["consequents"])
        for j in range(len(sets)):  
            print("intersection")
            print(set(map[sets[j]]).intersection(contenu))
            if set(map[sets[j]]).intersection(contenu):
                result.append(sets[j])
                
    result=set(result)
    propositions liste(result)
    return result  ## "propositions:\n" + ", https://www.facebook.com/".join()

    #TODO: EYA bech ta3mel el task hethi:
    # cas the variable propositions is an empty list:
    # na3mlou intersection bin el map wel contenu,  w naba3thou lel user 2 random propositon wala wa7da
    #cas el intersection empty:
    #n9oulou lel user raw ma3ana 7ata tuto  using these items , be the first to post an idea



if __name__ == '__main__':
    dataset = [['2127397610646634', '2127401723979556', '2127403330646062', '2127405733979155', '2127408890645506', '2127410443978684'],
           ['2127412840645111', '2127401723979556', '2127403330646062', '2127405733979155', '2127408890645506', '2127410443978684'],
           ['2127397610646634', '2127412720645123', '2127405733979155', '2127408890645506'],
           ['2127397610646634', '2127412190645176', '2127412393978489', '2127405733979155', '2127410443978684'],
           ['2127412393978489', '2127401723979556', '2127401723979556', '2127405733979155', '2127412000645195', '2127408890645506']]
    contenu=set(["bottle"])
    map = {
    "2127401723979556" : ["bottle","tire"],
    "2127405733979155":  ["paper"],
    "2127408890645506" : ["box","paper"]    
    }
    result=association_rule(contenu, dataset, map)
    print("result")
    print(result)
