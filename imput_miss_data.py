# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 23:36:31 2021

@author: orkun
"""

from tkinter import filedialog
import tkinter as tk
import pandas as pd
from sklearn.impute import SimpleImputer
from pandas.api.types import is_numeric_dtype
import numpy as np

root = tk.Tk()
root.wm_attributes('-topmost', 1)
root.withdraw()


class file_read(object):
    def __init__(self, file_path, miss_format, delimiter):
        self.file_path = file_path
        self.miss_format = miss_format
        self.delimiter = delimiter


class miss_columns(file_read):
    def __init__(self, file_path, miss_format, delimiter):
        super().__init__(file_path, miss_format, delimiter)

    def missing_cols_get(self):
        df = pd.read_csv(self.file_path, delimiter=self.delimiter, na_values=self.miss_format)
        self.df = df
        self.missing_col_list = [column for column in df.columns if df[column].isnull().any()]
        return self.missing_col_list

    def imput_data_get(self):
        num_imp = SimpleImputer(missing_values=np.nan, strategy='mean')
        cat_imp = SimpleImputer(missing_values=np.nan, strategy='most_frequent')

        imputed_data = self.df
        for col_name in self.missing_col_list:
            if is_numeric_dtype(self.df[col_name].dtypes):
                imputer = num_imp.fit_transform(pd.DataFrame(self.df[col_name]))
                imputed_data[col_name] = pd.DataFrame(data=imputer)
            else:
                imputer = cat_imp.fit_transform(pd.DataFrame(self.df[col_name]))
                imputed_data[col_name] = pd.DataFrame(data=imputer)

        return imputed_data


if __name__ == '__main__':
    # ---Read File Path
    file_path = filedialog.askopenfilename(parent=root, initialdir="/", title='Please select a file')
    missing_formats = ["NA", "nan", "NAN", ""]
    delimeter = ","
    missing_object = miss_columns(file_path, missing_formats, delimeter)
    missing_columns = missing_object.missing_cols_get()
    print(file_path + " has missing columns : " + ",".join(missing_columns))
    imput_data = missing_object.imput_data_get()
    print(imput_data)
