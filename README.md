# User based product recommendations

![](https://github.com/shrinidhin/recommender-system/blob/main/images/screenshot.JPG?raw=true)

A Recommendation engine for an e-commerce use case that provides recommendations to users based on their purchase history. It has been built using the matrix factorization algorithm. 

**Installation**

The dependencies required to run the code at your end can be installed from the requirements.txt file within your virtual environment using 

```pip install -r requirements.txt ```

The app has been developed using H2o.ai Wave. Please refer to their [detailed documentation](https://wave.h2o.ai/docs/installation) to setup and run the Wave server on your machine. Once that's done, you can easily run any wave app . 

**Development**

[Data Engineering](https://github.com/shrinidhin/recommender-system/blob/main/Gathering%20data.ipynb)

This notebook converts the raw data stored in json.gz of different categories into a single csv file. It also combines the metadata of different categories which is required by our wave application for displaying recommendations to the user.

[Model building and training](https://github.com/shrinidhin/recommender-system/blob/main/recommendation-system-using-matrix-factorization.ipynb)

This is where the model is trained,hyperparameters are tuned and the final model is saved to be used by the wave app to provide recommendations. The model has been trained using the Matrix Factorization module of the h2o4gpu package.

[Wave App](https://github.com/shrinidhin/recommender-system/tree/main/rec-system)

The web application uses the model built in the previous notebook and other output files to provide product recommendations relevant for each selected user. 

**Running your Wave app**\
After setting up your environment with the dependencies installed, navigate to the ```rec-system``` directory and execute the following command

```wave run app.py```

Now use any web browser of your choice to view the app at : [localhost:10101/rec]()

**Citations**

Justifying recommendations using distantly-labeled reviews and fined-grained aspects
Jianmo Ni, Jiacheng Li, Julian McAuley
Empirical Methods in Natural Language Processing (EMNLP), 2019 [pdf](http://cseweb.ucsd.edu/~jmcauley/pdfs/emnlp19a.pdf)


