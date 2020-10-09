'''
Created on Apr 12, 2020

@author: Elif Kaya 

Rating-based movie recommendation

'''

import numpy as np
import os
import pandas as pd

def processFiles(folder_name, movie_file, critics_file, personal_ratings_file): 
    '''
    reads all user input files and returns a tuple of the datas frames for files 
    :param folder_name: name of the folder with files that user enters
    :param movie_file: name of the movie file that user enters
    :param critics_file: name of the critics file that user enters 
    :param personal_ratings_file: name of the personal ratings file that user enters 
    :return: returns a tuple of data frames for movies, critics, and personal ratings files 
    '''

    #read the main file and join the path 
    file_name = os.path.join(os.getcwd(), folder_name, movie_file)
    imdb_df = pd.read_csv((file_name), usecols = ['Title', 'Year', 'Rating', 'TotalVotes', 'Genre1', \
               'Genre2', 'Genre3','MetaCritic', 'Runtime', 'Budget'], index_col=['Title'] )
    
    #Read the ratings file
    ratings_path = os.path.join(os.getcwd(), folder_name, personal_ratings_file)
    p_rating_df = pd.read_csv(ratings_path, index_col=['Title'] )
    
    #read the critics file 
    critics_path = os.path.join(os.getcwd(), folder_name, critics_file)
    critics_df = pd.read_csv(critics_path, index_col=['Title'] )
    
    files_to_process = imdb_df, critics_df, p_rating_df
    
    return files_to_process




def findClosestCritics(critics_ratings, personal_ratings):
    '''
    :param critics_ratings: data frame of critics ratings
    :param personal_ratings: data frame of personal ratings 
    :return: list of three critics, whose ratings of movies are most similar to those provided in the personal ratings data, 
    based on Euclidean distance
    
    '''
    
    #Filter the critics data to only have the movies that the person has watched 
    critics_filtered = critics_ratings[critics_ratings.index.isin(personal_ratings.index)]
    
    #Calculate the euclidean distance 
    euclidean_dist = np.sqrt(((critics_filtered - personal_ratings.values)**2).sum(axis=0))
   
    #only filter the 3 smallest values which are the ones that are closest to the person ratings
    three_critics =  list(euclidean_dist.nsmallest(3).index)
    
    return three_critics


def recommendMovies(critics_ratings, personal_ratings, three_critics, movie ):
    '''
    recommendMovies () which will be used to generate movie recommendations based on ratings by the chosen critics. 
    The function must accept four parameters: 
    the critics and personal ratings data frames, the list of three critics most similar to the person, 
    and the movie data frame. 
    The function should determine out of the set of movies that are not rated in the personal data, 
    but are rated by the critics, which movies have the highest average of the rating 
    by the most similar critics in each movie genre (specified by the Genre1 column of movie data).
    
    :param critics_ratings: data frame of critics ratings
    :param personal_ratings: data frame of personal ratings 
    :param three_critics: list of three critics, whose ratings of movies are most similar to those provided in the personal ratings data, 
    based on Euclidean distance
    :param movie: imdb movies data frame 
    :return: list of top rated unwatched movies for the person in each Genre1 based on the average of three critics ratings 
    
    '''
    
    #Filter the critics data to only have the movies that the person has not watched 
    critics_filtered = critics_ratings[~critics_ratings.index.isin(personal_ratings.index)]
    
    movies_df = critics_filtered.loc[:, three_critics]
    
    #get the average of ratings and round them to 2 decimal points
    movie_averages = round(movies_df.mean(axis = 1), 2).to_frame()
    
    # add average column to the movie averages df
    movie_averages.columns = ['Average']

    
    #Create a new df from IMDB data with the columns we  need
    imdb_df = movie[['Year', 'Rating', 'Genre1', 'Runtime']]

    #merge movie averages and imdb dataframes on Title 
    merged_df = pd.merge(movie_averages, imdb_df, on = 'Title')

    #get the highest average of ratings per Genre1 types 
    dg_highest = merged_df.reset_index().groupby(by = 'Genre1')['Average'].max().reset_index()
    
    #merge the highest average df with the merged df of 
    recommended_movies = merged_df.reset_index().merge(dg_highest, on = ['Genre1', 'Average']).sort_values('Genre1')
    
    #return list of movie recommendations 
    return recommended_movies.reset_index(drop=True)


def printRecommendations (recommended_movies, name ):
    '''    
    :param recommended_movies: recommended movies from recommendMovies function 
    :param name: name of the person for whom the recommendation is made
    
    '''
    
    print('Recommendations for',  name)
    
    #get length of longest movie
    longest_movie = recommended_movies['Title'].map(len).max()+2
    
    for i,row in recommended_movies.iterrows():
        row.Title = '"' + row.Title + '"'
        print(f'{row.Title.ljust(longest_movie)} ({row.Genre1}), rating: {row.Average}, {row.Year}' % row,\
              ('runs ' + str(row.Runtime)) if not pd.isna(row.Runtime) else '' )
            

def main():

    #ask user input for folder and files 
    folder_name, movie_file, critics_file, personal_ratings_file = input('Please enter the name of the folder with files, the name of movies file,\n'\
                                                                         +'the name of critics file,the name of personal ratings file, separated by spaces: ').split()
    
    #process files into dataframes 
    imdb_df, critics_df, p_rating_df = processFiles(folder_name, movie_file, critics_file, personal_ratings_file)
    
    #find 3 closest critics list
    three_critics = findClosestCritics(critics_df, p_rating_df)
    
    #get list of recommended movies
    recommended_movies = recommendMovies(critics_df, p_rating_df,three_critics, imdb_df)
    print()
    print('The following critics had reviews closest to the person\'s:')
    print(', '.join(three_critics))
    print()
    name = p_rating_df.columns[0]
    printRecommendations(recommended_movies, name)
    
main()
    