import numpy as np
import pandas as pd
from collections import Counter
from mlxtend.preprocessing import TransactionEncoder
from sklearn.metrics.pairwise import cosine_similarity as cos
import joblib

ingredients = ['almonds',
 'alum powder',
 'amaranth leaves',
 'apricots',
  'arrowroot powder',
 'axone',
 'basmati rice',
 'beef',
 'besan flour',
 'bhatura',
 'bhuna chana',
 'biryani masala powder',
 'boiled pork',
 'boiled potatoes',
 'bombay duck',
 'bombay rava',
 'boondi',
 'brown rice flour',
 'butter',
 'cardamom pods',
 'cardamom powder',
  'carrots',
 'cashews and raisins',
 'cauliflower',
 'chana daal',
  'chenna cheese',
 'chhena',
 'chia seed',
 'chicken thighs',
 'chickpeas',
 'chole',
 'citric acid',
 'coconut flakes',
 'dahi',
 'dal',
 'dates',
 'dharwadi buffalo milk',
 'dried fruits',
 'dried rose petals',
 'drumstick',
 'dry chilli',
 'dry coconut',
 'dry dates',
 'dry roasted',
 'edible gum',
 'egg yolks',
 'eggplant',
 'elachi',
 'elephant foot yam',
 'firm white pumpkin',
 'fish fillets',
 'fish roe',
 'flour',
 'forbidden black rice',
 'fried milk power',
 'fry',
 'garlic',
 'ghee',
 'ginger and garlic',
 'green beans',
 'green bell pepper',
 'green cardamom',
 'green garlic chutney',
 'green moong beans',
 'heavy cream',
 'hot water',
 'jaggery syrup',
 'kala chana',
 'kala jeera',
 'kala masala',
 'kewra',
 'khoa',
 'kitchen lime',
 'ladies finger',
 'lentil flour',
 'litre milk',
 'loaf bread',
 'long beans',
 'maida flour',
 'malvani masala',
 'mashed potato',
 'masoor dal',
 'mawa',
 'milk powder',
 'molu leaf',
 'mung bean',
 'musk melon seeds',
 'naan bread',
 'orange rind',
 'peanuts',
 'pigeon peas',
 'pistachio',
 'plain flour',
 'poppy seeds',
 'pork',
 'potol',
 'raw banana',
 'red chili',
 'red chilli',
 'reduced milk',
 'refined flour',
 'rose water',
 'sauce',
 'sesame',
 'skimmed milk powder',
 'skinless chicken breasts',
 'slivered almonds',
 'soaked rice',
 'spices',
 'spinach',
 'split pigeon peas',
 'sticky rice',
 'sugar syrup',
 'sweetened milk',
 'tamarind paste',
 'tindora',
 'tomato paste',
 'tomato sauce',
 'vermicelli pudding',
 'vinegar',
 'water',
 'whipping cream',
 'white bread slices',
 'white flour',
 'whole egg',
 'whole wheat bread',
 'whole wheat rava',
 'wine vinegar',
 'yellow mustard',
 'yoghurt',]


data = pd.read_csv("processed_indian_food.csv", encoding='latin-1')
te = joblib.load("trans_encoder.sav")
enc = joblib.load("label_encoder.sav")
recom_trans_data = pd.read_csv("processed_data.csv")
trans_data = recom_trans_data.drop(["recomm"],axis=1)


def food_recommendation(in_ing):
    in_x = te.transform([in_ing]).astype("int")
    values = []
    for i in trans_data.index: 
        x = np.array(in_x).reshape(1,-1)
        y = trans_data.iloc[i].values.reshape(1,-1)
        cosine = cos(x,y)
        values.append(cosine[0][0])
    result = list(zip(recom_trans_data["recomm"].values,values))
    fin = sorted(result,key= lambda x : x[1],reverse=True)
    fin = list(filter(lambda x : x[1] != 1.0 and x[1] != 0,fin))
    if len(fin)>9:
            rec = 9
    else:
            rec = len(fin)
    neighbours = []
    for n in range(rec):
            neighbours.append(enc.inverse_transform([fin[n][0]])[0])
    neighbours
    output_recom = []
    for i in neighbours:
        total_op = data[data["name"]==i]
        time = total_op["prep_time"].values[0]+total_op["cook_time"].values[0]
        c = f'''
{"*"*50}
"{total_op["name"].values[0]}"
---------------------------------------------
ingredients: {total_op["ingredients"].values[0]}
diet: {total_op["diet"].values[0]}
flavor_profile: {total_op["flavor_profile"].values[0]}
course: {total_op["course"].values[0]}
from location: {total_op["state"].values[0]} state,{total_op["region"].values[0]} region
total time to create recipe: {time if time else "not possible to calculate time in"} mins
instructions: {total_op["instructions"].values[0]}

'''+"*"*50
        output_recom.append(c)
    return "\n".join(output_recom)

if __name__ == "__main__":
    print(food_recommendation(["all purpose flour", "aloo"]))
