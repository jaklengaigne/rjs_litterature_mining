class RawDf:
    # Constructor
    def __init__(self, raw_df):
        self.raw = raw_df
    # Methods
    # Mutator
    def preprocess(self):  
        # Removing duplicates if needed
        # creating a new column in the data frame. All the colums are considered
        # because any subset are specified. The first occurence of a row is keep
        # by writing False in the new column at this row (not a duplicate). Else,
        # True is writed.
        self.raw['dup'] = self.raw.duplicated(subset=None, keep='first')
        
        # Counting the number of duplicates (number of true). Return the number
        # of False and True.
        self.raw['dup'].value_counts()
        
        # Creating a new data frame without the duplicates
        raw_data_noDup = self.raw[self.raw['dup'] == False]
    
        # Deleting the column with the True and False because it is no more useful
        del raw_data_noDup['dup']
            
        # Removing useless columns (All articles have written nothing in those fields)
        raw_data_useField = raw_data_noDup.dropna(axis=1, how='all')
     
        # Changing the type of NaN to string
        # (For text cleaning everything need to be string)
        raw_data_str = raw_data_useField.fillna("NaN")
        clean_df = raw_data_str
        
        return clean_df