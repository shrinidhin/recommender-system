The Data folder within the **rec-system** directory contains the following input files required by the wave app to run. 
1. **meta_data.csv**: This contains the metadata of all the products. It contains information like asin,title,feature,description,price,image.related products,salesRank,brand,categories the product belongs to,technical details of the product etc.
2. **recommend_model.pickle**: This pickle file is the final matrix factorization model trained on the entire dataset. 
3. **review_data.pickle**: This pickle file contains required user and item indices and user's purchasing history to be used by the wave application while fetching recomendations.
