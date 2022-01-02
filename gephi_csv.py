import pandas as pd
import pickle

# makes node & edges csv file for detailed gephi graphing

# nodes csv file #########################################################

infile = open('./files/fdist', 'rb')
fdist = pickle.load(infile)
infile.close()

df_nodes = pd.DataFrame({'Id' : [i for i in range(1, len(fdist) + 1)],
                         'Name' : [k for k, v in fdist.items()],
                         'Count' : [v for k, v in fdist.items()],
                         })


df_nodes.to_csv('./csv/nodes.csv', sep = ',', index = False)
print('saved nodes.csv')

# edges csv file #########################################################

df_matrix = pd.read_csv("./csv/matrix.csv", index_col = 0)

def finder(q): # finding the matching indexes in df_nodes (gephi format)
    try:
        return df_nodes['Name'][df_nodes['Name'] == q].index[0]
    except:
        print("<finder>: can't find")
        quit()



df_edges = pd.DataFrame({'Source' : [],
                         'Target' : [],
                         'Type' : ['Undirected' for x in range(len(df_matrix))],
                         'Weight' : [],
                         })


df_edges.to_csv('./csv/edges.csv', sep = ',', index = False)
print('saved nodes.csv')


print(finder('http'))
