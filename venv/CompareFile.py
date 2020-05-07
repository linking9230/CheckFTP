import pandas as pd
import numpy as np
import openpyxl
import os
import difflib

class comparefile():


    def __init__(self,today_file,latest_file,code,today):


        mylist1 = []

        for chunk in pd.read_table(latest_file, 'r', delimiter="|", chunksize=20000):
            mylist1.append(chunk)
        df1 = pd.concat(mylist1, axis=0)
        del mylist1
        
        mylist2=[]

        for chunk in pd.read_table(today_file,'r',delimiter="|",chunksize=20000):
            mylist2.append(chunk)
        df2=pd.concat(mylist2,axis=0)
        del mylist2





        df1=df1[df1['Global ID investment'].isin(['Equity','ETF','Warrant','Equity-Right'])]
        df2=df2[df2['Global ID investment'].isin(['Equity','ETF','Warrant','Equity-Right'])]

        df1=df1[df1['Security Type']==1]
        df2=df2[df2['Security Type']==1]


        df1=df1.iloc[:,[2,5]]
        df2=df2.iloc[:,[2,5]]

        df1.columns=['Symbol', 'Last Day Company Name']
        df2.columns=['Symbol', 'Today Company Name']
        df3=pd.merge(df1,df2,how="left",on='Symbol')

        def revise(a):
            if pd.isnull(a) is False:
                a = a.lower().replace('co.,', '').replace('.', '').replace('ltd', '').replace('limited', '').replace(
                    'inc', ''). \
                    replace('corporation', '').replace('corp', '').replace(',', '')
            return a

        def comp(a, b):
            if pd.isnull(a) and pd.isnull(b):
                return True
            elif pd.isnull(a):
                return 'Last Day is Empty'
            elif pd.isnull(b):
                return 'Today is Empty'
            else:
                a=revise(a)
                b=revise(b)
                ratio=difflib.SequenceMatcher(None,a,b).quick_ratio()
                if ratio>=0.8:
                    return True
                else:
                    return round(ratio,2)



        df3['diff']=df3.apply(lambda x: comp(x['Last Day Company Name'],x['Today Company Name']),axis=1)
        df3=df3[df3['diff']!=True]

        #df3 = df3.sort_values(axis=0, ascending=True, by=['diff'])

        diff_path='O:\\Content\\Daily workflow\\Morningstar CBOE Market Data\\diff_' + today +'.xlsx'
        if os.path.exists(diff_path):
            with pd.ExcelWriter(diff_path,mode='a') as writer:
                df3.to_excel(writer, sheet_name=code)
        else:
            with pd.ExcelWriter(diff_path) as writer:
                df3.to_excel(writer, sheet_name=code)

        wb = openpyxl.load_workbook(diff_path)
        sheet = wb[code]

        sheet.column_dimensions['B'].width = 15
        sheet.column_dimensions['C'].width = 50
        sheet.column_dimensions['D'].width = 50

        wb.save(diff_path)
        wb.close()


