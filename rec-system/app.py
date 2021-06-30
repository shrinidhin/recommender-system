from logging import PlaceHolder
from h2o_wave import Q,main,app,site,ui
from h2o_wave.core import Page, data
import pickle
import numpy as np
from scipy import sparse
from numpy.core.fromnumeric import size
import pandas as pd
from fetch import fetch_data,get_product_data,get_model,get_recommendations
from typing import List

def initialize_ui(q:Q):
    q.page['meta']=ui.meta_card(box='',layouts=[
        ui.layout(
        breakpoint='xs',
        #width='1200px',
        zones=[
            ui.zone('header'),
            ui.zone('menu',zones=[
                ui.zone('greeting'),
                ui.zone('user'),
            ]),
            ui.zone('body', zones=[
                ui.zone('history', size='50%'),
                ui.zone('recommend', size='50%')
            ]),
            ui.zone('footer'),
        ]
    ),
        ui.layout(breakpoint='m',zones=[
            ui.zone('header', size='80px'),
            #ui.zone('user',size='60px'),
            ui.zone('menu',direction=ui.ZoneDirection.ROW,zones=[
                ui.zone('greeting',size='50%'),
                ui.zone('user',size='50%'),
            ],size='60px'),
            ui.zone('body', size='750px', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone('history', size='50%'),
                    ui.zone('recommend', size='50%')
                    ]),
                ]),
        ui.layout(breakpoint='xl',zones=[
            ui.zone('header',size='80px'),
            #ui.zone('user',size='60px'),
            ui.zone('menu',direction=ui.ZoneDirection.ROW,zones=[
                ui.zone('greeting',size='50%',align='start'),
                ui.zone('user',size='50%'),
            ],size='60px'),
            ui.zone('body', size='750px', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone('history', size='50%'),
                    ui.zone('recommend', size='50%')
                ])

        ]
        )

    ])

    q.page.add('header',ui.header_card(
        box='header',
        title='User based recommendations for E-commerce',
        icon='People',
        icon_color='white',
        subtitle=''
    )
    )
    
    q.page['user']=ui.section_card(
        box='user',
        title='',
        subtitle='',
        items=[
            
            ui.dropdown(name='select_users', label='', tooltip='Select user to fetch recommendations',
            choices=[ui.choice(name=str(x), label=str(x)) for x in list(q.client.u_dict.keys())[:50]],
            value=q.client.user,
            trigger=True
            ),
            ui.button(name='cart',icon='ShoppingCart',primary=True,tooltip='View Cart',visible=False),
            ui.expander(name='cart_info',visible=False)
        ],
    )

    q.page['recommend'] = ui.stat_list_card(
        box='recommend',
        title='Recommendations for you',
        subtitle='Here are a few products you may like.',
    items=[]
    )

    q.page['history']=ui.stat_table_card(
        box='history',
        title='Products you have rated',
        subtitle='',
        columns=['Product','Rating'],
        items=[]
    )

def show_progress(q:Q,initial=True):
    if initial:
        q.page['loading'] = ui.form_card(
         box='1 1 9 9',
         items=[
        #ui.progress(label='Indeterminate Progress', caption='Goes on forever'),
         ui.progress('Getting ready...'),
         ])
    else:
        q.page['Loading']=ui.form_card(box='1 1 12 15',items=[ui.progress('Fetching recommendations....')]) 

def show_recommendations(q:Q):
    #constructing test set:User id and item
    #Getting items already purchased by user
    purchased=[k[0] for k in q.client.u_dict[q.client.user]]
    products=[p for p in list(q.client.items.keys()) if p not in purchased and p in q.client.id_title.keys()]
    users=[q.client.user for i in range(0,len(products))]
    data=zip(users,products)
    #Constructing test frame
    X_test=pd.DataFrame(data,columns=['users','products'])
    user_indices=[q.client.user_indices[u] for u in users]
    item_indices=[q.client.items[i] for i in products]
    #Constructing sparse matrix
    X_test_sparse=sparse.coo_matrix((np.ones(len(X_test), dtype="float32"),(user_indices,item_indices)))#,shape=(len(users),len(products)))
    X_test['predictions']=get_recommendations(X_test_sparse)
    #Sorting Dataframe based on predictions
    X_test=X_test.sort_values(by=['predictions'],ascending=False)[:10]
    a=np.array(X_test['predictions'].values.tolist())
    X_test['predictions']=np.where(a>5,5,a).tolist()
    q.page['recommend'].items=[
        ui.stat_list_item(label=q.client.id_title[row['products']],caption='',
        value=str(np.round(row['predictions'])),icon='ShoppingCartSolid',icon_color='yellow')
        for k,row in X_test.iterrows()
    ]


def show_user_info(q:Q):
    q.page['history'].items=[
        ui.stat_table_item(label=q.client.id_title[k[0]], caption='',
                               values=[str(k[1])],
                            icon='Product',icon_color='blue') for k in q.client.u_dict[q.client.user]
    ]
        

@app('/rec')
async def serve(q:Q):
    if not q.client.initialized:
        show_progress(q)
        await q.page.save()
        q.client.u_dict,q.client.user_indices,q.client.items= await q.run(fetch_data)
       # q.client.u_dict,q.client.user_indices,q.client.items=fetch_data()
        q.client.meta_data,q.client.id_title=await q.run(get_product_data)
        q.client.user=list(q.client.u_dict.keys())[0]
        await q.run(get_model)
        initialize_ui(q)
        q.client.initialized=True
    if  q.args.select_users:
        q.client.user=q.args.select_users 
    show_user_info(q)
    show_recommendations(q)
    await  q.page.save()
