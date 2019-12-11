# https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.LeaveOneOut.html
from sklearn.model_selection import LeaveOneOut
from database import *
from seperate_functions import * # association rule mining UDF
import numpy

# ARM_train ARM_predict   -> eya
# ARM_test -> kim : code ok, mezel ntesteha
# n7otou data set fi un seul fichier -> kim DONE
# map id bel img -> eya
# formulaire 3al google like dislike: -> eya DONE
# we copy entries from google forms to our data set -> eya
# du coup 3ana star statique fih j'aime bta3 notre user -> eya , fel le5er ena 3maltha
# what can i do with a bottle , ne5dmoha b list -> kim  DONE
# integre fazet el ken ma3anech el object XXXXXXXX ma5doum
# w ken bech tlawa7ha haw lehne b3ida 500 m -> eya
# ARM_hyperparametreOptimisation grid search -> kim
# run LeaveOneOut_test w 7ot score w kol -> kim
# result graph 7keyet -> kim
# n9oulou enehom a7sen results wel score bte3hom
# how can i reuse donald trump ?



# nsajlgou el video 7keya m3al chat bot en fonction meli mawjoud fel senario ------------- jeudi


# dilog flow: how does it work ? -> you can ask me how to recycle .... or a photo    -> eya

# description lel procedure fel doc   -> kim

# ba3d ma na3mlou el map, n7otou les obj el kol fel dialogflow fel entities




#return 0 or 1
def ARM_test(rules, ActiveUserTransactions):
    contenu=set([])
    prediction = ARM_predict_list(contenu,ActiveUserTransactions,rules,mapping)  # nestana eya trod func hethi haka ARM_predict(contenu,tab,mapping): # ARM_predict(oneUserTransactions,rules)
    #print("ARM_test")
    #print(prediction)
    #print(ActiveUserTransactions)
    attempt = 0
    for pred in prediction:
        if ( pred in ActiveUserTransactions ):
            return 1
        attempt += 1
        if (attempt == 1): break
    return 0

# return accuracy
def LeaveOneOut_test(dataset,min_support,min_threshold):
    score = 0
    tot = 0
    loo = LeaveOneOut()
    loo.get_n_splits(dataset)

    dataset = numpy.array(dataset)

    for train_index, test_index in loo.split(dataset):
        dataset_train = dataset[train_index] # train
        dataset_test =  dataset[test_index] # ActiveUserTransactions
        rules = ARM_train(dataset_train,min_support,min_threshold)
        if not rules.empty:
            score += ARM_test(rules, dataset_test[0])

        tot = tot + 1
        #print(score)

    return float(score)/tot # this is accuracy

#return tuple of best  param
def ARM_hyperparameterOptimisation(dataset): # grid search
    best_min_support = -1
    best_min_threshold = -1
    best_score = -1

    min_support_range = numpy.linspace(0.3, 1.0, 10)
    min_threshold_range = numpy.linspace(0.3, 1.0, 10)

    print("hyperparameterOptimisation:")
    print("min_support_range")
    print( min_support_range)
    print("min_threshold_range")
    print( min_threshold_range)

    for min_support in min_support_range:
        for min_threshold in min_threshold_range:
            localScore = LeaveOneOut_test(dataset,min_support,min_threshold)
            print(localScore)
            if localScore>best_score:
                best_min_support = min_support
                best_min_threshold = min_threshold
                best_score = localScore
        print(" _ \n")
    print("best_min_support= ")
    print(best_min_support)
    print("best_min_threshold= ")
    print( best_min_threshold)
    print("best_score= ")
    print( best_score)

    return best_min_support, best_min_threshold



if __name__ == '__main__':
    rules=ARM_train(dataset)
    #print(tab)
    contenu=set(["bottle"])
    result_list=ARM_predict_list(contenu,ActiveUserTransactions,rules,mapping)
    #print(result_list)
    print(ARM_test(rules, ActiveUserTransactions))




    print("(pre test) LeaveOneOut_test:")
    print(LeaveOneOut_test(dataset,min_support=0.6,min_threshold=0.7))

    ARM_hyperparameterOptimisation(dataset)
    #TODO:  visualisation excel  --> kim

