#import sklearn library
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import math

#dictionary with usernames the product ratings out of 5
data =pd.read_excel('dataset.xlsx')
exp =[]
dict = data.to_dict('list')
dicKeys = list(dict.keys())
dicValues = list(dict.values())[1:]
otherKeys =list(dict.values())[0]

for value in dicValues:
    actual = {otherKeys[i]: value[i] for i in range(len(otherKeys))}
    new = {key: value for (key, value) in actual.items() if not math.isnan(value)}
    exp.append(new)

dicKeys.pop(0)
dataset ={dicKeys[i]: exp[i] for i in range(len(dicKeys))}

# custom function to create unique set of products
def unique_items():
    unique_items_list = []
    for person in dataset.keys():
        for items in dataset[person]:
            unique_items_list.append(items)
    s=set(unique_items_list)
    unique_items_list=list(s)
    return unique_items_list


# custom function to implement cosine similarity between two items i.e. products
def item_similarity(item1,item2):
    both_rated = {}
    for person in dataset.keys():
        if item1 in dataset[person] and item2 in dataset[person]:
            both_rated[person] = [dataset[person][item1],dataset[person][item2]]

    number_of_ratings = len(both_rated)
    if number_of_ratings == 0:
        return 0

    item1_ratings = [[dataset[k][item1] for k,v in both_rated.items() if item1 in dataset[k] and item2 in dataset[k]]]
    item2_ratings = [[dataset[k][item2] for k, v in both_rated.items() if item1 in dataset[k] and item2 in dataset[k]]]
    cs = cosine_similarity(item1_ratings,item2_ratings)
    return cs[0][0]


#custom function to check most similar items 

def most_similar_items(target_item):
    un_lst=unique_items()
    scores = [(item_similarity(target_item,other_item),target_item+" --> "+other_item) for other_item in un_lst if other_item!=target_item]
    scores.sort(reverse=True)
    return scores

#custom function to filter the seen products and unseen products of the target user
def target_products_to_users(target_person):
    target_person_product_lst = []
    unique_list =unique_items()
    for products in dataset[target_person]:
        target_person_product_lst.append(products)

    s=set(unique_list)
    recommended_products=list(s.difference(target_person_product_lst))
    a = len(recommended_products)
    if a == 0:
        return 0
    return recommended_products,target_person_product_lst

# function to recommend based on ratings
def recommendation_phase(target_person):
    if target_products_to_users(target_person=target_person) == 0:
        print(target_person, "has seen all the products")
        return -1
    not_seen_products,seen_products=target_products_to_users(target_person=target_person)
    seen_ratings = [[dataset[target_person][products],products] for products in dataset[target_person]]
    weighted_avg,weighted_sim = 0,0
    rankings =[]
    for i in not_seen_products:
        for rate,product in seen_ratings:
            item_sim=item_similarity(i,product)
            weighted_avg +=(item_sim*rate)
            weighted_sim +=item_sim
        weighted_rank=weighted_avg/weighted_sim
        rankings.append([weighted_rank,i])

    rankings.sort(reverse=True)
    return rankings

print("Enter the target person")
tp = input()
if tp in dataset.keys():
    a=recommendation_phase(tp)
    if a != -1:
        print("Recommendation Using Item based Collaborative Filtering:  ")
        for w,m in a:
            print(m," ---> ",w)
else:
    print("Person not found in the dataset..please try again")