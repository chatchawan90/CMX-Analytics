import pandas as pd 
import pyodbc
bioM2025 = pd.read_excel("1102024_NewBioM_2025 SKU LIST.xlsx", sheet_name="contour-export-08-26-2024_LA2")

print(f"Total Products: {len(bioM2025)}") 

rename = {"GLOBAL_PRODUCT_ID": "Stockcode" , "GLOBAL_PRODUCT_DESC": "Descripiton",
        "HIERARCHY_L3_DESC": "Cat", "HIERARCHY_L4_DESC": "Sub Cat", "HIERARCHY_L5_DESC": "SBU"}

bioM2025 = bioM2025.rename(columns=rename)
bioM2025['Stockcode'] = bioM2025['Stockcode'].astype(str)

# Export to csv
bioM2025.to_csv('112024_bioM2025_processed.csv', index=False)


# Testing code below 
'''

# Get the Stockcode that needs to add "." 
# 1. Length => "1014920100" = 10 
# 2. add
condition = (bioM2025['Stockcode'].str.len() == 10) & (bioM2025['Stockcode'].str.isdigit())
bioM2025.loc[condition,'Stockcode'] = bioM2025[condition]['Stockcode'].apply(lambda x: x[:-4]+"."+x[-4:])


all_goodcode = bioM2025['Stockcode'].tolist() 
all_goodcode = list(f'\'{x}\'' for x in all_goodcode)
all_goodcode_str = ','.join(all_goodcode)

bioM2025_LoD = bioM2025.to_dict('records')

def retreive_val ( query):
    """execute query and turn the data in the a list of dict

    Args:
        query (_type_): _description_

    Returns:
        list of dictionary: all data from the data as a list of dict
    """
    cursor.execute(query)
    result = cursor.fetchall()
    col = [column[0] for column in cursor.description]
    result_LoD = [dict(zip(col,x)) for x in result ]
    # LoD = list of dict
    return col,result_LoD

# Dont forget to delete this!
SERVER='sichemex.fortiddns.com,1444'
DB='dbwins_cmx'
USERNAME='chemex'
PASSWORD=r'6vQ~cDx6yCpP(CQ`'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER+';DATABASE='+DB+';UID='+USERNAME+';PWD='+ PASSWORD)
cursor = cnxn.cursor()


check_goodcode_match_query = f"""
select distinct * from emgood 
where goodcode in ({all_goodcode_str})
"""



found_in_db = retreive_val(check_goodcode_match_query)
print(f"Total Products Found: {len(found_in_db[1])}")




# print(bioM2025_LoD)'''
