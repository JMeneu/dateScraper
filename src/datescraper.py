import re
import pandas as pd
import numpy as np


class datescraper:
    """
    A class to scrape dates from raw text files

    ...

    Attributes
    ----------
    DEFAULT : str
        a set of date usual patterns found in raw text data

    Methods
    -------
    textExtractor(filename=None):
        Opens a text file and returns its content line by line.
    
    patternApplier(df):
        Iterates through PATTERNS to extract the dates information.
    
    dataframeColumnCleaner(df):
        Gets rid of noisy columns created after extracting information from the file.
        Returns a cleaned DataFrame, where numerically named columns are dropped.

    dataframeFiller(df, value=1):
        Fills in missing or empty values with the specified value.

    dataframeTextAppender(df, field="year", value="19"):
        Preppends an especified value to the elements that may miss it in the specified field.

    dataframeMonthFormatter(df, field="month"):
        Casts text-based formatting in an specified field (month), to numeric-based.
    exportAs(df, selected_format=1):
        Exports the parameter df to .csv, .xlsx or .json, as selected_format specifies.
    """
    DEFAULT =[r'(?P<month>[0-9]{0,2})(/|-)(?P<day>[0-9]{0,2})(/|-)(?P<year>[0-9]{2,4})',
            r'(?P<day>[0-9]{0,2})(\s||s|.|\()(?P<month>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\w{0,9}|)(\s|,\s)(?P<year>[0-9]{4})',
            r'(?P<month>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\w{0,9}|)(\s|,\s|.\s)(?P<day>[0-9]{0,2})(,|) (?P<year>[0-9]{4})',
            r'(e|\s|^|~|n|\()(?P<month>[0-9]{0,2})/(?P<year>[0-2][0-9]{3}|[0-9]{2} )'
                ]
    def __init__(self, PATTERNS = DEFAULT):
        self.DEFAULT=PATTERNS

    def textExtractor(self,filename):
        '''
        Opens a text file and returns its content line by line.
        '''
        with open (filename) as file:
            lines= file.readlines()
        return lines

    def patternApplier(self, df):
        '''
        Iterates through PATTERNS to extract the dates information.
        
        
        First, creates a temp_df. Then, it iterates through PATTERNS, applying them 
        extract information about the dates. The results are concatenated to the temp_df. 
        After the iteration ends, the indexes are sorted to their original position.
        Finally, a temp_df with the results is returned.
        '''
        temp_df = pd.DataFrame()
        for pattern in self.DEFAULT:
            temp_df=pd.concat([temp_df,df["raw"].str.extract(pattern).dropna(how = 'any')])
        temp_df.sort_index(inplace=True)
        return temp_df

    def dataframeColumnCleaner(self, df):
        '''
        Gets rid of noisy columns created after extracting information from the file.
        Returns a cleaned DataFrame, where numerically named columns are dropped.
        '''
        for column in df.columns:
            if(type(column))is not str:
                df = df.drop(columns=column, axis =0)
        return df

    def dataframeFiller(self, df, value =1):
        '''
        Fills in missing or empty values with the specified value.
        '''
        df = df.replace(r'^\s*$', np.nan, regex = True)
        df = df.fillna(value = value)
        return df

    def dataframeTextAppender(self, df, field="year", value="19"):
        '''
        Preppends an especified value to the elements that may miss it in the specified field.
        '''
        temp_lst = []
        for element in df[field]:
            if len(element)<3:
                element = str(value)+element
            temp_lst.append(element)
        df[field]= temp_lst
        return df
    
    def dataframeMonthFormatter(self, df, field="month"):
        '''
        Casts text-based formatting in an specified field (month), to numeric-based.
        
        
        First, creates a temp_lst from the parameters df[field] inserted. Then, it iterates through
        it, and also iterates through temp_dict, a dictionary with the values to substitute in the 
        specified field. If the a key in temp_dict is the same as an element in temp_lst, appends 
        the value to the temp_lst. Finally the values from temp_lst are inserted to the parameter
        df, which is returned.
        '''
        temp_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,
                    "Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,
                    "Nov":11,"Dec":12}
        temp_lst=df[field]
        for i, element in enumerate(temp_lst):
            for key,value in temp_dict.items():
                if key == element:
                    temp_lst[i-1]=value
        df[field]=temp_lst
        return df

    def exportAs(self, df, selected_format=1):
        '''
        Exports the parameter df to .csv, .xlsx or .json, as selected_format specifies.
        
        
        [0] == .csv
        [1] == .xlsx
        [2] == .json
        '''

        if selected_format == 0:
            df.to_csv("processed_dates.csv")
        elif selected_format == 1:
            df.to_excel("processed_dates.xlsx")
        elif selected_format == 2:
            df.to_json("processed_dates.json")
        else:
            print("Wrong selected_format! Check out the doctsring for more information.")