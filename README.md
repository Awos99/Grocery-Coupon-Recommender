# Grocery Coupon Recommender

This repository contains the core algorithms for a grocery coupon recommendation system designed to enhance customer engagement and increase revenue for grocery store franchises.

## Algorithm Overview

### 1. Selecting a Shop

The `select_shop` function determines the most relevant shop for a user based on their transaction history and loyalty card usage. This ensures recommendations are tailored to the user's preferred shopping location.

```python
def select_shop(df_shops, df_transactions, df_user_loyalty, user_id, franchise):
    ...
```

### 2. Top Associations

The top_associations function identifies products frequently bought together with a given product. This helps in creating effective cross-selling strategies by suggesting complementary products.

```python
def top_associations(df_transactions, df_user_loyalty, franchise, product_id, n=10):
    ...
```

### 3. Top Products for User

The get_top_products_user function finds the top products a user has purchased. This information is used to personalize recommendations, ensuring they align with the user's preferences.

```python
def get_top_products_user(df_transactions, df_user_loyalty, user_id, franchise, n=10):
    ...
```

### 4. Similar Products
   
The get_similar_products function uses a pre-trained sentence transformer model to identify products similar to a given product based on their names. This is crucial for upselling by recommending higher-value but similar items.

```python
def get_similar_products(df_grocery_products, product_id, n=10):
    ...
```

### 5. Product Recommendations

The get_product_recommendations function integrates the previous algorithms to provide comprehensive recommendations for cross-selling, upselling, and encouraging more frequent visits. It generates personalized and effective product suggestions for users.

```python
def get_product_recommendations(df_transactions, df_user_loyalty, df_grocery_products, user_id, franchise, n=10):
    ...
```

## Potential Benefits

### Effective Discounts

 - Personalized Offers: Tailored discounts based on individual purchase history increase the likelihood of coupon redemption.
 - Targeted Promotions: Cross-selling and upselling recommendations introduce customers to relevant products, driving additional sales.
   
### Increased Revenue

 - Boost in Sales: Effective cross-selling and upselling strategies can increase the average basket size, directly boosting revenue.
 - Customer Retention: Personalized and relevant recommendations enhance customer satisfaction and loyalty, encouraging repeat business.

### Optimized Inventory Management

 - Demand Forecasting: Insights into purchasing patterns help in predicting demand, leading to better inventory management and reduced wastage.

### Competitive Advantage

 - Enhanced Shopping Experience: Providing a tailored shopping experience differentiates the franchise from competitors, attracting and retaining customers.

Implementing these algorithms in a grocery store franchise can lead to more effective discounts, increased sales, optimized inventory management, and a significant competitive advantage.

Please try the app here:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://grocery-coupon-recommender.streamlit.app/)
