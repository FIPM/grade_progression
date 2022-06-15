import pandas as pd
import os


# Menu
path_to_translations = os.path.join('static','translations')
df_Navbar = pd.read_csv(os.path.join(path_to_translations,'Navbar.csv'))
df_Content = pd.read_csv(os.path.join(path_to_translations,'Content.csv'))

KEY = '09ffd4f2e3095ee986f2adfb497bd952'

# Figure 1
# uploading data
db_fig1=pd.read_csv('./raw_data/Fig1_data.csv',sep=';')

# Figure 2
# uploading data
db_fig2=pd.read_csv('./raw_data/Fig2_data.csv',sep=';')

# Figure 2
# uploading data
db_fig3=pd.read_csv('./data/Fig3_data.csv',sep=',')
db_fig3 = db_fig3.sort_values(by='LastGrade',ascending=True)
db_fig3['Last Grade Observed']=db_fig3['LastGrade'].astype(str)

# Figure 2
# uploading data
db_fig4=pd.read_csv('./data/Fig4_data.csv',sep=',')
grades=[4,5,6,7,8,9]
listNames=[]
for grade in grades:
    listNames.append('PrecisionLastGrade_'+str(grade))
    listNames.append('RecallLastGrade_'+str(grade))
    listNames.append('F1LastGrade_'+str(grade))
db_fig4=db_fig4[listNames]
db_fig4=db_fig4.melt(var_name='NameIndex2',value_name='Index')
db_fig4=db_fig4.drop_duplicates(subset=['NameIndex2'],keep='first')
db_fig4.reset_index(drop=True, inplace=True)
db_fig4['LastGrade']=db_fig4['NameIndex2'].str[-1]
db_fig4['Index Name']=db_fig4['NameIndex2'].str.split('LastGrade_').str[0]
db_fig4=db_fig4[['LastGrade','Index Name','Index']].copy()



