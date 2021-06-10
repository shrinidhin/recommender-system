import pickle
import pandas as pd
import h2o4gpu

def fetch_data():
    with open('Data/review_data.pickle', 'rb') as f:
        master_dict=pickle.load(f)
    user_dict=master_dict['user']
    users=master_dict['user_indices']
    items=master_dict['item_indices']
    return user_dict,users,items

def get_model():
    with open('Data/recommend_model.pickle','rb') as m:
        global model
        model=pickle.load(m)

def get_product_data():
    m_data=pd.read_csv('./Data/meta_data.csv',usecols=['asin', 'title'])
    i_ti=dict(zip(m_data.asin,m_data.title))
    return m_data,i_ti

def get_recommendations(df):
    predictions=model.predict(df).data
    return predictions


