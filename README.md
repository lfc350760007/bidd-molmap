![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) 
[![Documentation Status](https://readthedocs.org/projects/molmap/badge/?version=latest)](https://molmap.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.com/shenwanxiang/bidd-molmap.svg?branch=master)](https://travis-ci.com/shenwanxiang/bidd-molmap) 
[![DOI](https://zenodo.org/badge/214117402.svg)](https://zenodo.org/badge/latestdoi/214117402)

[![Paper](https://img.shields.io/badge/paper-Nature%20Machine%20Intelligence-green)](https://www.nature.com/articles/s42256-021-00301-6)
[![Codeocean](https://img.shields.io/badge/reproduction-codeocean-yellowgreen)](https://codeocean.com/capsule/2307823/tree)


For the application in the Omics Data, please follow the link in AggMap: https://github.com/shenwanxiang/bidd-aggmap

# [Out-of-the-Box Deep Learning Prediction of Pharmaceutical Properties by Broadly Learned Knowledge-Based Molecular Representations ](https://www.nature.com/articles/s42256-021-00301-6)


## MolMap
MolMap is generated by the following steps:

* Step1: Data sampling 
* Step2: Feature extraction 
* Step3: Feature pairwise distance calculation --> cosine, correlation, jaccard
* Step4: Feature 2D embedding --> umap, tsne, mds
* Step5: Feature grid arrangement --> grid, scatter
* Step5: Transform --> minmax, standard
* Step6: Get MolMap



### Construction of the MolMap Objects
![molmap](https://github.com/shenwanxiang/bidd-molmap/blob/master/paper/images/Overall.png)


### The MolMapNet Architecture

![net](https://github.com/shenwanxiang/bidd-molmap/blob/master/paper/images/net.png)

## Installation


1. install [rdkit](http://www.rdkit.org/docs/Install.html) and [tamp](https://tmap.gdb.tools/index.html#support) first(create a molmap env):
```bash
conda create -c conda-forge -n molmap rdkit
conda activate molmap
conda install -c tmap tmap
```

2. in your "molmap" env, install molmap by:

```bash
git clone https://github.com/shenwanxiang/bidd-molmap.git
cd bidd-molmap
pip install -r requirements.txt --user

# add molmap to PYTHONPATH
echo export PYTHONPATH="\$PYTHONPATH:`pwd`" >> ~/.bashrc

# init bashrc
source ~/.bashrc
```

3. [ChemBench](https://github.com/shenwanxiang/ChemBench) (optional, if you wish to use the dataset and the split induces in this paper).


4. If you have gcc problems when you install molmap, please installing g++ first:
```bash
sudo apt-get install g++
```


## Out-of-the-Box Usage

![code](https://github.com/shenwanxiang/bidd-molmap/blob/master/paper/images/code_example.png)


```python
import molmap
# Define your molmap
mp_name = './descriptor.mp'
mp = molmap.MolMap(ftype = 'descriptor', fmap_type = 'grid',
                   split_channels = True,   metric='cosine', var_thr=1e-4)
```

```python
# Fit your molmap
mp.fit(method = 'umap', verbose = 2)
mp.save(mp_name) 
```

```python
# Visulization of your molmap
mp.plot_scatter()
mp.plot_grid()
```

```python
# Batch transform 
from molmap import dataset
data = dataset.load_ESOL()
smiles_list = data.x # list of smiles strings
X = mp.batch_transform(smiles_list,  scale = True, 
                       scale_method = 'minmax', n_jobs=8)
Y = data.y 
print(X.shape)
```

```python
# Train on your data and test on the external test set
from molmap.model import RegressionEstimator
from sklearn.utils import shuffle 
import numpy as np
import pandas as pd
def Rdsplit(df, random_state = 888, split_size = [0.8, 0.1, 0.1]):
    base_indices = np.arange(len(df)) 
    base_indices = shuffle(base_indices, random_state = random_state) 
    nb_test = int(len(base_indices) * split_size[2]) 
    nb_val = int(len(base_indices) * split_size[1]) 
    test_idx = base_indices[0:nb_test] 
    valid_idx = base_indices[(nb_test):(nb_test+nb_val)] 
    train_idx = base_indices[(nb_test+nb_val):len(base_indices)] 
    print(len(train_idx), len(valid_idx), len(test_idx)) 
    return train_idx, valid_idx, test_idx 
```

```python
# split your data
train_idx, valid_idx, test_idx = Rdsplit(data.x, random_state = 888)
trainX = X[train_idx]
trainY = Y[train_idx]
validX = X[valid_idx]
validY = Y[valid_idx]
testX = X[test_idx]
testY = Y[test_idx]

# fit your model
clf = RegressionEstimator(n_outputs=trainY.shape[1], 
                          fmap_shape1 = trainX.shape[1:], 
                          dense_layers = [128, 64], gpuid = 0) 
clf.fit(trainX, trainY, validX, validY)

# make prediction
testY_pred = clf.predict(testX)
rmse, r2 = clf._performance.evaluate(testX, testY)
print(rmse, r2)
```

* [Click for More Example](https://github.com/shenwanxiang/bidd-molmap/blob/master/molmap/example/00_model_example_esol.ipynb)










## Out-of-the-Box Performances

| Dataset   | Task Metric | MoleculeNet (GCN Best Model) | Chemprop (D-MPNN model) | MolMapNet (MMNB model) |
|-----------|-------------|-----------------------------|------------------------|-----------------------|
| ESOL      | RMSE        | 0.580 (MPNN)                | 0.555                  | 0.575                 |
| FreeSolv  | RMSE        | 1.150 (MPNN)                | 1.075                  | 1.155                 |
| Lipop     | RMSE        | 0.655 (GC)                  | 0.555                  | 0.625                 |
| PDBbind-F | RMSE        | 1.440 (GC)                  | 1.391                  | 0.721                 |
| PDBbind-C | RMSE        | 1.920 (GC)                  | 2.173                  | 0.931                 |
| PDBbind-R | RMSE        | 1.650 (GC)                  | 1.486                  | 0.889                 |
| BACE      | ROC_AUC     | 0.806 (Weave)               | N.A.                   | 0.849                 |
| HIV       | ROC_AUC     | 0.763 (GC)                  | 0.776                  | 0.777                 |
| PCBA      | PRC_AUC     | 0.136 (GC)                  | 0.335                  | 0.276                 |
| MUV       | PRC_AUC     | 0.109 (Weave)               | 0.041                  | 0.096                 |
| ChEMBL    | ROC_AUC     | N.A.                        | 0.739                  | 0.750                 |
| Tox21     | ROC_AUC     | 0.829 (GC)                  | 0.851                  | 0.845                 |
| SIDER     | ROC_AUC     | 0.638 (GC)                  | 0.676                  | 0.68                  |
| ClinTox   | ROC_AUC     | 0.832 (GC)                  | 0.864                  | 0.888                 |
| BBBP      | ROC_AUC     | 0.690 (Weave)               | 0.738                  | 0.739                 |
