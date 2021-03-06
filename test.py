import numpy as np
import pickle as pkl
from sklearn.preprocessing import StandardScaler
from GVAE import Model
import sys

 
data_path = './guacamol_graph.pkl'
save_path = './guacamol_model.ckpt'

print(':: load data')
with open(data_path,'rb') as f:
    [DV, DE, DY, Dsmi] = pkl.load(f)

n_node = DV.shape[1]
dim_node = DV.shape[2]
dim_edge = DE.shape[3]
dim_y = DY.shape[1]

atom_list = ['B','C','N','O','F','Si','P','S','Cl','Se','Br','I']
bond_list = ['SINGLE', 'DOUBLE', 'TRIPLE']
bpatt_dim = [3, 3, 2, 1, 2, 1]

print(':: preprocess data')
scaler = StandardScaler()
scaler.fit(DY)
DY = scaler.transform(DY)

mu_prior = np.mean(DY,0)   
cov_prior = np.cov(DY.T)             

model = Model(n_node, dim_node, dim_edge, dim_y, atom_list, bpatt_dim, mu_prior, cov_prior)

print(':: generate molecular graphs')
with model.sess:
    model.saver.restore(model.sess, save_path)
    total_count, valid_count, novel_count, unique_count, genmols = model.test(10000, 0, Dsmi)

valid=valid_count/total_count
unique=unique_count/valid_count
novel=novel_count/valid_count

print(':: Valid:', valid*100, 'Unique:', unique*100, 'Novel:', novel*100, 'GMean:', 100*(valid*unique*novel)**(1/3))
