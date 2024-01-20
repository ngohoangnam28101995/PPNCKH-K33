import pandas as pd
import warnings
import re

class TextGenerator:
    def __init__(self, data, gloss_column, text_column):
        self.data = data
        self.translate = data
        self.gloss = gloss_column
        self.text = text_column
        
        self.handle_prefix()
        #self.handle_two_meaning()
        #self.handle_compound()
        
    def handle_prefix(self):
        
        '''
            This code handle and clean some glosses like: ns-AMERICA, ns-nat-VN, ns-DO+fs-DO, .....
            And generate that gloss to text form likes: america, vn, do do, ....
            The ns and the nat always go together so just need to find the ns and the fs index.
            
            Parameter:
                self: the data that has been read by the DataReader class
            Output:
                The data that contains the cleaned gloss column (Class Label) and the Text of label that contains prefix.
        '''
        #Tìm các index mà chuỗi thoả điều kiện có 'ns' hoặc 'fs'
        prefix_id = self.data[(self.data[self.gloss].str.contains('ns')) |(self.data[self.gloss].str.contains('fs'))].index

        # special prefix likes (A)MEXICO -> MEXICO
        self.data[self.gloss] = self.data[self.gloss].apply(lambda x: re.sub("\(.*?\)|\[.*?\]","", x))
        self.data.loc[prefix_id, self.gloss] = self.data.loc[prefix_id, self.gloss].str.replace('[a-z -]', ' ', regex = True)
        
        #when handle ns there are some problems like ns-COSTA-RICA however the second '-' cannot be eliminated.
        self.data[self.gloss] = self.data[self.gloss].apply(lambda x: x.replace(' ', '') if '+' in x else x.strip())
        
        self.data.loc[prefix_id, self.gloss] = self.data.loc[prefix_id, self.gloss].str.replace(' ', '-')

        #Nam add
        self.data[self.text] = self.data[self.gloss]
        self.data[self.text] = self.data[self.text].str.lower()
        self.data[self.text] = self.data[self.text].str.replace("#","")   
        self.data[self.text] = self.data[self.text].apply(self.clean_text)
        self.data[self.text] = self.data[self.text].apply(self.choose_word)
        
    def clean_text(self,text):
        modified_string = re.sub(r'\\[^\\]+\\', '',text)
        modified_string = modified_string.replace('"','')
        return modified_string
    def choose_word(self,text):
        text = text.split("+")
        result = []
        for word in text:
            word = word.split("/")
            word = word[0]
            result.append(word)            
        return ' '.join(result)
            

    def get_data(self):
        
        return self.data