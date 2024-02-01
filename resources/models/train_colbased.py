"""

    Single Value Decomposition plus plus (SVDpp) model training.

    Author: Explore Data Science Academy.

    Description: Simple script to train and save an instance of the
    SVDpp algorithm on MovieLens data.

"""
# Script dependencies
import numpy as np
import pandas as pd
from surprise import SVD
import surprise
import pickle

# Importing datasets
ratings = pd.read_csv('ratings.csv')
ratings.drop('timestamp',axis=1,inplace=True)

# Reconstruct model
# Create a list of split parts
split_parts = ['svd_model_af', 'svd_model_am', 'svd_model_at', 'svd_model_ba',
                'svd_model_ag', 'svd_model_an', 'svd_model_au', 'svd_model_bb',
                'svd_model_aa',  'svd_model_ah', 'svd_model_ao', 'svd_model_av', 'svd_model_bc',
                'svd_model_ab',  'svd_model_ai', 'svd_model_ap', 'svd_model_aw', 'svd_model_bd',
                'svd_model_ac', 'svd_model_aj', 'svd_model_aq', 'svd_model_ax', 'svd_model_be',
                'svd_model_ad', 'svd_model_ak', 'svd_model_ar', 'svd_model_ay', 'svd_model_bf',
                'svd_model_ae', 'svd_model_al', 'svd_model_as', 'svd_model_az']

# Specify the output path for the reconstructed model
output_path = 'svd_model.pkl'

# Combine split parts into the reconstructed model
with open(output_path, 'wb') as output_file:
    for part in split_parts:
        with open(part, 'rb') as input_file:
            output_file.write(input_file.read())

def svd_pp(save_path):
    # Check the range of the rating
    min_rat = ratings['rating'].min()
    max_rat = ratings['rating'].max()
    # Changing ratings to their standard form
    reader = surprise.Reader(rating_scale = (min_rat,max_rat))
    # Loading the data frame using surprise
    data_load = surprise.Dataset.load_from_df(ratings, reader)
    # Instantiating surprise
    method = SVD(n_factors = 300 , verbose=True, n_epochs = 30 , init_std_dev = 0.05, random_state=42)
    # Loading a trainset into the model
    model = method.fit(data_load.build_full_trainset())
    print (f"Training completed. Saving model to: {save_path}")

    return pickle.dump(model, open(save_path,'wb'))

if __name__ == '__main__':
    svd_pp('svd_model.pkl')
