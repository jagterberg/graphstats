#!/usr/bin/env python

# omni.py

import numpy as np
import networkx
import pandas as pd
from ..ase import adj_spectral_embedding
from sklearn.preprocessing import MinMaxScaler

def omni_matrix(list_of_sim_matrices, off_diag = "mean", transform = "omni_bar", max_dim = 2, eig_scale = 0.5): #, combine = "omni_bar"):
    """
        Inputs
        list_of_sim_matrices - The adjacencies to create the omni for
        off_diag = Metric used for off diagonals

    Returns
        omni - The omni matrix of the list
    """

    M = len(list_of_sim_matrices)
    n = len(list_of_sim_matrices[0])
    omni = np.zeros(shape = (M*n, M*n))

    for i in range(M):
        for j in range(i, M):
            for k in range(n):
                for m in range(k + 1, n):
                    if i == j:
                        omni[i*n + k, j*n + m] = list_of_sim_matrices[i][k, m] 
                        omni[j*n + m, i*n + k] = list_of_sim_matrices[i][k, m] # symmetric
                    else:
                        if off_diag == "mean":
                            omni[i*n + k, j*n + m] = (list_of_sim_matrices[i][k,m] + list_of_sim_matrices[j][k,m])/2
                            omni[j*n + m, i*n + k] = (list_of_sim_matrices[i][k,m] + list_of_sim_matrices[j][k,m])/2

    Y = omni.copy()

    if transform == "ase":
        Y = adj_spectral_embedding(Y, max_dim = max_dim, eig_scale = eig_scale)[0]
    elif transform == "omni_bar":
        Y = adj_spectral_embedding(Y, max_dim = max_dim, eig_scale = eig_scale)[0]
        for i in range(1, M):
            for j in range(n):
                Y[int(j % n), :] += Y[i*n + j, :]
        Y = Y[:n, :].copy() / M

    return Y

def get_attributes(G):
    if type(G) != networkx.classes.graph.Graph:
        raise TypeError("networkx.classes.graph.Graph only")

    if len(G) == 0:
        raise ValueError("Graph has no nodes")

    attributes = list(G.nodes[0])
    attr_values = []
    to_int = []
    for attr in attributes:
        temp = list(networkx.get_node_attributes(G, attr).values())
        if temp[0] == int(temp[0]) and temp[-1] == int(temp[-1]):
            to_int.append(attr)
        else:
            temp = np.array([float(i) for i in temp])
        attr_values.append(temp)

    attr_values = np.array(attr_values).T

    attr_df = pd.DataFrame(data = attr_values, columns = attributes)
    attr_df[to_int] = attr_df[to_int].astype(int)

    return attr_df

def similarities(attributes_df, columns, joint = False, metric = "eucl_dist"):
    """
    Generates a list of similarity matrices

    Inputs
        attributes_df - A dataframe of node attributes
        columns - A list of column indices or names
        joint - Function generates len(columns) similarity matrices if False
        metric - The metric used to calculate the similarity matric

    Outputs
        sims - A list of similarity matrices

    """
    if len(columns) == 0:
        return None
    if len(attributes_df) == 0:
        return None

    if type(columns[0]) == float or type(columns[0]) == int:
        columns = [int(i) for i in columns]
        column_names = list(attributes_df)
        column_names = [column_names[i] for i in columns]
    elif type(columns[0]) == str:
        column_names = columns
    else:
        raise ValueError("Unsupported column type")
        return None

    n = len(np.array(attributes_df[column_names[0]]))

    sims = []

    if joint:
        feature_array = []
        for c in column_names:
            scaler = MinMaxScaler()
            temp = np.array(attributes_df[c])
            temp = temp.reshape(-1, 1)
            scaler.fit(temp)
            scaled = scaler.transform(temp)
            feature_array.append(scaled)
        scaler = MinMaxScaler
        scaler.fit(attributes_df[column_names])
        feature_array_2 = scaler.transform(attributes_df[column_names])


        feature_array = np.array(feature_array)

        print(feature_array, feature_array_2)
        return



        # TODO
        scaler = MinMaxScaler()
        scaler.fit()
        print("")
    else:
        for c in column_names:
            try:
                temp = np.array(attributes_df[c])
            except:
                raise ValueError("Unsupported or inconsistent column type")
                return None

            s2 = np.var(temp, ddof = 1)
            temp_sim = np.zeros(shape = (n, n))

            for i in range(n):
                for k in range(i + 1, n):
                    if metric == "eucl_dist" or metric == "fuzzy_subset":
                        dist = (temp[i] - temp[k])**2
                        temp_sim[i,k] = np.exp(-dist/s2)
                        temp_sim[k,i] = temp_sim[i,k]

            sims.append(temp_sim)

    return sims