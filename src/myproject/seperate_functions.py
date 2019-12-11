#!/usr/bin/env python
from database import *
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def ARM_train(dataset,min_support=0.6,min_threshold=0.7):
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset) # TODO: nefehmou el fit wel transform 5ater y7ebou explication
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    #frequent_itemsets

    #print(frequent_itemsets)
    #print(min_threshold)
    #print(frequent_itemsets.empty)
    if frequent_itemsets.empty:
        return frequent_itemsets
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_threshold)
    rules["antecedent_len"] = rules["antecedents"].apply(lambda x: len(x))
    #rules
    
    return rules

#TODO: integre ActiveUserTransactions -->  eya
def ARM_predict_list(contenu, ActiveUserTransactions, rules,mapping):
    #ajouter le mappage entre la publication et le contenu de l'image
    if not contenu :
        contenu =["tire","bottle","paper","box","candle","cutlery","can","wood","lamp","gearing","plant","glass bottle"]

    #print("dump:")
    #print(contenu)
    #print(ActiveUserTransactions)
    #print(rules)
    #print(mapping)

    pair = rules['antecedents']
    test=rules[['consequents','confidence']]
    items = [x for x in pair]
    i=0;
    num=[]
    for ant in items :
        set(ActiveUserTransactions)
        inter_ant=ant.intersection(set(ActiveUserTransactions))
        if inter_ant :
            #print(inter_ant)
            num.append(i)
        i+=1;
    tab=pd.DataFrame(test,index=num)
    tab=tab.drop_duplicates().sort_values(by=['confidence'],ascending=False)
    #tab:the consequence of the rules related to the ActiveUserTransactions ordered w.r.t confidence    

    result=[]
    
    for index, row in tab.iterrows():
        sets=list(row["consequents"])
        for j in range(len(sets)):  
            if set(mapping[sets[j]]).intersection(contenu): #TODO: if contenu is an empty list : maghir intersection
                result.append(sets[j])
                
    result=set(result)
    
    if result :
        propositions=list(result)
        
        
    else :
        inter=[]
        for key in mapping:
            #print key, 'corresponds to', mapping[key]
            if set(mapping[key]).intersection(contenu):
                    inter.append(key)
        propositions=list(inter)
        #print("inter")
        #print(inter)
   
    return propositions

def ARM_predict_sting(propositions):
    if propositions :
        speech="propositions:\nfb.com/" + "\nfb.com/".join(propositions)
    else :
        speech = "unfortunatlely we don't have any idea using these items.\nBe the first one to publish your idea :D\n Or you can also throw it in this special bin\n(adress: 8 Rue General de Gaulles...)\nOur partner, A Recycling company will take care of it for you :)"
    return speech


if __name__ == '__main__':
    tab=ARM_train(dataset)
    #print(tab)
    contenu=set(["bottle"])
    result_list=ARM_predict_list(contenu,ActiveUserTransactions,tab,mapping)
    print(result_list)
    result_string=ARM_predict_sting(result_list)
    print(result_string)
    contenu=set([])
    result_list=ARM_predict_list(contenu,ActiveUserTransactions,tab,mapping)
    print(result_list)
    result_string=ARM_predict_sting(result_list)
    print(result_string)
