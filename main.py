

from DataReader import DataReader
from TextGenerator import TextGenerator
import pandas as pd
import argparse



parser = argparse.ArgumentParser(description='')
#Input argument
parser.add_argument('input_file', type=str, help='Path to the input file.')


#Break argument input
args = parser.parse_args()
input_file = args.input_file


if __name__ == "__main__":
    
    columns_add = ['Vid_name', 'Signer', 'Frame', 'Text']
    column_adjust = 'full video file'
    gloss_column = 'Class Label'
    
    reader_data = DataReader(filename = input_file, columns_use = [6, 7, 12, 13, 14],columns_add = columns_add,column_adj = column_adjust).get_data()
    data = TextGenerator(data = reader_data,gloss_column = gloss_column,text_column = columns_add[3]).get_data()
    data.to_csv('Result.csv')

        