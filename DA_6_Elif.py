import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#Define Constants 

TITLE = 'Title'
RATING = 'Rating'
GENRE1 = 'Genre1'
VOTESU18 = 'VotesU18'
VOTESU1829 = 'Votes1829'
VOTESU3044 = 'Votes3044'
VOTESU45A = 'Votes45A'
CVOTESU18M = 'CVotesU18M'
CVOTESU18F = 'CVotesU18F'
CVOTESU1829F = 'CVotes1829F'
CVOTESU1829M = 'CVotes1829M'
CVOTESU3044F = 'CVotes3044F'
CVOTESU3044M = 'CVotes3044M'
CVOTESU3045F = 'CVotes45AF'
CVOTESU3045M = 'CVotes45AM'



def processFiles(folder_name): 
    '''
    reads user input 
    :param folder_name: name of the subfolder  
    '''
    global TITLE, RATING, GENRE1, VOTESU18 ,VOTESU1829, VOTESU3044, VOTESU45A, CVOTESU18M, CVOTESU18F, \
        CVOTESU1829F, CVOTESU1829M, CVOTESU3044F,  CVOTESU3044M, CVOTESU3045F, CVOTESU3045M

    #read the main file and join the path 
    file_name = os.path.join(os.getcwd(),folder_name,"IMDB.csv" )
    imdb_df = pd.read_csv((file_name), usecols = [TITLE, RATING, GENRE1, VOTESU18 ,VOTESU1829, VOTESU3044, VOTESU45A, CVOTESU18M, CVOTESU18F, \
        CVOTESU1829F, CVOTESU1829M, CVOTESU3044F,  CVOTESU3044M, CVOTESU3045F, CVOTESU3045M], index_col=[TITLE] )

    return imdb_df

 def pickMovieWithKeyword(imdb_df, movie_keyword):
    '''
    :param imdb_df: IMDB movies data frame
    :param movie_keyword: movie keyword entered by the user
    '''
    global TITLE

    filtered_df = imdb_df[imdb_df[TITLE].str.contains(movie_keyword, na = False)]
    movie_list = pd.DataFrame(filtered_df[TITLE].reset_index(drop=True) )
    movie_list.index = movie_list.index + 1
    print(movie_list)
    

def pickMovieNumber(movie_number, movie_list):
    print('Movie #1: ', movie_list.loc[movie_number][TITLE])

def plot1(imdb_df, movie_list):
    global TITLE, RATING, GENRE1, VOTESU18 ,VOTESU1829, VOTESU3044, VOTESU45A
    
    #x = imdb_df[TITLE]
    y = imdb_df.loc[imdb_df.index.isin(movie_list), [VOTESU18 ,VOTESU1829, VOTESU3044, VOTESU45A]].transpose()
#     x = y.index
#     print(y)
#     plt.plot(x, y, 'o')
    print(y)
    y.plot(marker='o'), #xticks = ['<18', '18-29', '30-44','>45', 'lasa'])
#     plt.plot(y, y.transpose(), 'o')
    plt.grid(True)
    plt.xlabel('Age range')
    plt.ylabel('Rating')
    plt.title('Ratings by age group')
    plt.xticks = (['<18', '18-29', '30-44','>45'])
    plt.show()

#Test
df=processFiles("data")
y=plot1(df, ["12 Years a Slave","The Girl with the Dragon Tattoo", 'The Hunger Games: Catching Fire'])
print(y)
