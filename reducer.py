import pandas as pd
import pickle

infile = open('./files/fdist', 'rb')
fdist = pickle.load(infile)
infile.close()

CUTOFF = 9 # cutoff point(based on the number of references) for reducing matrix

kill = [k for k, v in fdist.items() if v <= CUTOFF]
print(len(fdist))
print(len(kill))

def ask():
    global path
    inp = int(input('\nmatrix.csv(1) or matrix_reduced.csv(2)?\n'))
    if inp == 1:
        path = './csv/matrix.csv'
    elif inp == 2:
        path = './csv/matrix_reduced.csv'
    else:
        print('wrong!')
        ask()

ask()
df_matrix = pd.read_csv(path, index_col = 0)
print('\nBEFORE')
print(df_matrix)

df_matrix.drop(kill, inplace = True, axis = 0, errors = 'ignore')
df_matrix.drop(kill, inplace = True, axis = 1, errors = 'ignore')

print('\n\nAFTER')
print(df_matrix)

# print(list(set(df_matrix.index.tolist()) - set(df_matrix.columns.tolist())))
print(df_matrix.isnull().values.any())

df_matrix.to_csv('./csv/matrix_reduced.csv', sep = ',')
