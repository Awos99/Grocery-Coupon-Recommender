import streamlit as st
import pandas as pd
import numpy as np

from algorithm import select_shop, get_product_recommendations

# Load data
df_grocery_products = pd.read_csv('Data/grocery_products_clean.csv')
df_shops = pd.read_csv('Data/shops.csv')
df_transactions = pd.read_csv('Data/transactions.csv')
df_user_loyalty = pd.read_csv('Data/user_loyalty.csv')
list_users = df_user_loyalty['user'].unique()

# simple app to display recommendations

# Create two columns
col1, col2 = st.columns(2)

# Use the first column to display the title
with col1:
    st.title('PricePal - Grocery Recommendation System')
    
# Use the second column to display the logo
with col2:
    st.image("./Logo.png", width=200)
         
st.write('Welcome to PricePal your grocery recommendation system. Please enter your user id and franchise to get started.')

user_id = st.selectbox('User ID', list_users, index=None)
if user_id:
    franchise = st.selectbox('Franchise', df_user_loyalty[df_user_loyalty['user']==user_id]['franchise'].unique(), index=None)
    if franchise:
        shop = select_shop(df_shops, df_transactions, df_user_loyalty, user_id, franchise)
        st.write(f'You should go to shop {shop} at franchise {franchise}')
        #n = st.number_input('Number of recommendations', min_value=1, max_value=10, value=5)
        if 'reco' + str(user_id) + str(shop) not in st.session_state:
            with st.spinner('Calculating Recommendations...'):
                recommendations_cross, recommendations_upsell, recommendations_frequent = get_product_recommendations(df_transactions, df_user_loyalty, df_grocery_products, user_id, franchise)
                st.session_state['reco' + str(user_id) + str(shop)] = [recommendations_cross, recommendations_upsell, recommendations_frequent]

        recommendation_types = ['Cross-Selling', 'Up-Selling', 'Increase frequency of visits with these']
        for index, recos in enumerate(st.session_state['reco' + str(user_id) + str(shop)]):
            st.title(f'{recommendation_types[index]} Recommendations')
            if len(recos) > 2:
                n_columns = 3
            elif len(recos) == 2:
                n_columns = 2
            else:
                n_columns = 1
            columns = st.columns(n_columns)
            for i, col in enumerate(columns):
                with col:
                    reco = df_grocery_products[df_grocery_products['SKU']==recos[i]]
                    with st.container(border=True, height=400):
                        if reco['image'].values[0] != 'No image found':
                            st.image(reco['image'].values[0], use_column_width='auto')
                        st.write(reco['PRODUCT_NAME'].values[0])
                        print(type(reco['PRICE_RETAIL'].values[0]))
                        print(reco['PRICE_RETAIL'].values[0])
                        if np.isnan(reco['PRICE_RETAIL'].values[0]):
                            st.subheader('Price not available')
                        else:
                            st.write(':red[$' + str(reco['PRICE_RETAIL'].values[0]) + ']')
                            st.subheader(':green[$' + str(np.round(reco['PRICE_RETAIL'].values[0]*0.8, decimals=2)) + ']')
            if index < 2 and len(recos) > 3:
                with st.expander(f'See more {recommendation_types[index]} recommendations'):
                    n_rows = len(recos[3:]) // n_columns
                    for i in range(n_rows):
                        recommendations = recos[3+i*n_columns:3+(i+1)*n_columns]
                        columns = st.columns(n_columns)
                        for j, col in enumerate(columns):
                            with col:
                                reco = df_grocery_products[df_grocery_products['SKU']==recommendations[j]]
                                with st.container(border=True, height=400):
                                    if reco['image'].values[0] != 'No image found':
                                        st.image(reco['image'].values[0], use_column_width='auto')
                                    st.write(reco['PRODUCT_NAME'].values[0])
                                    st.write(':red[$' + str(reco['PRICE_RETAIL'].values[0]) + ']')
                                    st.subheader(':green[$' + str(np.round(reco['PRICE_RETAIL'].values[0]*0.8, 2)) + ']')

        
        # col1, col2, col3 = st.columns(3)
        #         with col1:
        #             reco_cross_1 = df_grocery_products[df_grocery_products['SKU']==recommendations_cross[0]]
        #             print(reco_cross_1)
        #             with st.container(border=True, height=400):
        #                 if reco_cross_1['image'].values[0] != 'No image found':
        #                     st.image(reco_cross_1['image'].values[0], use_column_width='auto')
        #                 st.write(reco_cross_1['PRODUCT_NAME'].values[0])
        #                 st.title('$'+str(reco_cross_1['PRICE_RETAIL'].values[0]))
        #         with col2:
        #             reco_cross_2 = df_grocery_products[df_grocery_products['SKU']==recommendations_cross[1]]
        #             with st.container(border=True, height=400):
        #                 if reco_cross_2['image'].values[0] != 'No image found':
        #                     st.image(reco_cross_2['image'].values[0], use_column_width='auto')
        #                 st.write(reco_cross_2['PRODUCT_NAME'].values[0])
        #                 st.title('$'+str(reco_cross_2['PRICE_RETAIL'].values[0]))
        #         with col3:
        #             reco_cross_3 = df_grocery_products[df_grocery_products['SKU']==recommendations_cross[2]]
        #             with st.container(border=True, height=400):
        #                 if reco_cross_3['image'].values[0] != 'No image found':
        #                     st.image(reco_cross_3['image'].values[0], use_column_width='auto')
        #                 st.write(reco_cross_3['PRODUCT_NAME'].values[0])
        #                 st.title('$'+str(reco_cross_3['PRICE_RETAIL'].values[0]))
        #         st.button('See more1')
        
        #         col1, col2, col3 = st.columns(3)
        #         with col1:
        #             reco_cross_1 = df_grocery_products[df_grocery_products['SKU']==recommendations_upsell[0]]
        #             print(reco_cross_1)
        #             with st.container(border=True, height=400):
        #                 if reco_cross_1['image'].values[0] != 'No image found':
        #                     st.image(reco_cross_1['image'].values[0], use_column_width='auto')
        #                 st.write(reco_cross_1['PRODUCT_NAME'].values[0])
        #                 st.title('$'+str(reco_cross_1['PRICE_RETAIL'].values[0]))
        #         with col2:
        #             reco_cross_2 = df_grocery_products[df_grocery_products['SKU']==recommendations_upsell[1]]
        #             with st.container(border=True, height=400):
        #                 if reco_cross_2['image'].values[0] != 'No image found':
        #                     st.image(reco_cross_2['image'].values[0], use_column_width='auto')
        #                 st.write(reco_cross_2['PRODUCT_NAME'].values[0])
        #                 st.title('$'+str(reco_cross_2['PRICE_RETAIL'].values[0]))
        #         with col3:
        #             reco_cross_3 = df_grocery_products[df_grocery_products['SKU']==recommendations_upsell[2]]
        #             with st.container(border=True, height=400):
        #                 if reco_cross_3['image'].values[0] != 'No image found':
        #                     st.image(reco_cross_3['image'].values[0], use_column_width='auto')
        #                 st.write(reco_cross_3['PRODUCT_NAME'].values[0])
        #                 st.title('$'+str(reco_cross_3['PRICE_RETAIL'].values[0]))
        #         st.button('See more2')
        
        #         col1, col2 = st.columns(2)
        #         with col1:
        #             reco_cross_1 = df_grocery_products[df_grocery_products['SKU']==recommendations_frequent[0]]
        #             print(reco_cross_1)
        #             with st.container(border=True, height=400):
        #                 if reco_cross_1['image'].values[0] != 'No image found':
        #                     st.image(reco_cross_1['image'].values[0], use_column_width='auto')
        #                 st.write(reco_cross_1['PRODUCT_NAME'].values[0])
        #                 st.title('$'+str(reco_cross_1['PRICE_RETAIL'].values[0]))
        #         with col2:
        #             reco_cross_2 = df_grocery_products[df_grocery_products['SKU']==recommendations_frequent[1]]
        #             with st.container(border=True, height=400):
        #                 if reco_cross_2['image'].values[0] != 'No image found':
        #                     st.image(reco_cross_2['image'].values[0], use_column_width='auto')
        #                 st.write(reco_cross_2['PRODUCT_NAME'].values[0])
        #                 st.title('$'+str(reco_cross_1['PRICE_RETAIL'].values[0]))
