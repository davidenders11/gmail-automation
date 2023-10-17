import pandas as pd
workbook = pd.read_excel('Network.xlsx')
workbook.head()



for el in workbook['Email']:
    if isinstance(el, str): print(el)
