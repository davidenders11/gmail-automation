import pandas as pd
workbook = pd.read_excel('testing.xlsx')
workbook.head()

print(workbook['Product'].iloc[0])

name = ['John', 'Mary', 'Sherlock']
age = [11, 12, 13]
df = pd.DataFrame({ 'Name': name, 'Age': age })
df.index.name = 'ID'

df.to_excel('my_file.xlsx')