import ast
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import random
from tqdm import tqdm

def select_shop(df_shops, df_transactions, df_user_loyalty, user_id, franchise):
    user_cards = df_user_loyalty[(df_user_loyalty['user']==user_id) & (df_user_loyalty['franchise']==franchise)]['loyalty_card'].values
    user_transactions = df_transactions[df_transactions['loyalty_card'].isin(user_cards)]
    shops = user_transactions['shop'].value_counts()
    shop=shops.keys()[0]
    return shop


def top_associations(df_transactions, df_user_loyalty, franchise, product_id, n=10):
    # we should filter by year, but maybe later
    cards_franchise = df_user_loyalty[df_user_loyalty['franchise']==franchise]['loyalty_card'].values
    df_transactions_filter_franchise = df_transactions[df_transactions['loyalty_card'].isin(cards_franchise)]
    #transactions_merged_users = pd.merge(df_transactions, df_user_loyalty, how='inner', on='loyalty_card')
    #total_users = transactions_merged_users['user'].nunique()
    number_transactions = df_transactions_filter_franchise.shape[0]
    count_products = {}
    appeared_together = {}
    for i, row in df_transactions_filter_franchise.iterrows():
        for purchase in ast.literal_eval(row['products']):
            
            if purchase[0] not in count_products.keys() and purchase[0] not in appeared_together.keys():
                count_products[purchase[0]] = 0
                appeared_together[purchase[0]] = 0
            count_products[purchase[0]] += 1
            if product_id in [p[0] for p in ast.literal_eval(row['products'])]:
                appeared_together[purchase[0]] += 1
    for product in count_products.keys():
        count_products[product]=count_products[product]/number_transactions
        appeared_together[product]=appeared_together[product]/number_transactions

    support_products = count_products
    list_products = list(support_products.keys())
    list_products.remove(product_id)
    results = pd.DataFrame(index= list_products,columns=['Lift'])
    support_product_id = support_products[product_id]
    for other_product in list_products:
        support_other = support_products[other_product]
        
        support_both = appeared_together[other_product]
        results.at[other_product, 'Lift'] = support_both/(support_product_id*support_other) if support_product_id > 0 and support_other > 0 else 0
    return results.sort_values(by='Lift', ascending=False).head(n)


def get_top_products_user(df_transactions, df_user_loyalty, user_id, franchise, n=10):
    # we should do tfidf, but maybe later
    cards_franchise = df_user_loyalty[(df_user_loyalty['user']==user_id) & (df_user_loyalty['franchise']==franchise)]['loyalty_card'].values
    df_transactions_filter_franchise = df_transactions[df_transactions['loyalty_card'].isin(cards_franchise)]
    number_transactions = df_transactions_filter_franchise.shape[0]
    #print(number_transactions)
    count_products = {}
    for i, row in df_transactions_filter_franchise.iterrows():
        for purchase in ast.literal_eval(row['products']):
            if purchase[0] not in count_products.keys():
                count_products[purchase[0]] = 0
            count_products[purchase[0]] += 1
    for product in count_products.keys():
        count_products[product]=count_products[product]/number_transactions
    return pd.DataFrame.from_dict(count_products, orient='index', columns=['Support']).sort_values(by='Support', ascending=False).head(n)




# Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_similar_products(df_grocery_products, product_id, n=10):
    # Ensure the product_id exists in the dataframe
    if product_id not in df_grocery_products['SKU'].values:
        return None  # Return an empty DataFrame if product_id is not found
    
    # Find the product name for the given product_id
    product_name = df_grocery_products.loc[df_grocery_products['SKU'] == product_id, 'PRODUCT_NAME'].values[0]
    
    # Generate embeddings for the target product name
    product_embedding = model.encode([product_name])
    
    # Generate embeddings for all product names in the dataframe
    product_names = df_grocery_products['PRODUCT_NAME'].tolist()
    embeddings = model.encode(product_names)
    
    # Calculate cosine similarity between the target product and all products
    similarities = cosine_similarity(product_embedding, embeddings).flatten()
    
    # Add similarity scores to the dataframe
    df_grocery_products['similarity'] = similarities
    
    # Sort by similarity and return the top n similar products
    return df_grocery_products.sort_values(by='similarity', ascending=False).head(n + 1).iloc[1:]



def get_product_recommendations(df_transactions, df_user_loyalty, df_grocery_products, user_id, franchise, n=10):

    # recommendations for cross-selling

    # Step 1: Get the top products for the user
    top_products = get_top_products_user(df_transactions, df_user_loyalty, user_id, franchise, n=25)
    print('Top products')
    # Step 2: Find the top associations for 10 of those products
    recommendations_cross = []
    for product_id in top_products.sample(10).index:
        recommendations_cross.extend(top_associations(df_transactions, df_user_loyalty, franchise, product_id, n=10).index)
    
    # filter products already bought by user
    recommendations_cross = list(set(recommendations_cross))
    recommendations_cross = [product for product in recommendations_cross if product not in top_products.index]

    recommendations_cross = random.sample(recommendations_cross, n) if len(recommendations_cross) > n else recommendations_cross 
    print('Cross recommendations')
    # recommendation for upselling

    recommendations_upsell = []
    for product_id in top_products.sample(10).index:
        #print(product_id)
        similar_products = get_similar_products(df_grocery_products, product_id, n=3)['SKU'].tolist()
        # filter products with heigher price
        #print('Similar:', similar_products)
        similar_products = [product for product in similar_products if df_grocery_products.loc[df_grocery_products['SKU'] == product, 'PRICE_RETAIL'].values[0] > df_grocery_products.loc[df_grocery_products['SKU'] == product_id, 'PRICE_RETAIL'].values[0]]
        recommendations_upsell.extend(similar_products)
    
    # filter products already bought by user
    recommendations_upsell = list(set(recommendations_upsell))
    recommendations_upsell = [product for product in recommendations_upsell if product not in top_products.index]

    recommendations_upsell = random.sample(recommendations_upsell, n) if len(recommendations_upsell) > n else recommendations_upsell
    print('Upsell recommendations')
    # recommendation for more frequent visits
    recommendation_frequent = top_products[5:15].sample(2).index.tolist()
    print('Frequent recommendations')
    
    
    return recommendations_cross, recommendations_upsell, recommendation_frequent