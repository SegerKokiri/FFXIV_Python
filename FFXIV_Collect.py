#Simple tool to just copy some stuff from FFXIV  d
                                         
import requests
import json
import pandas as pd

api_url = "https://ffxivcollect.com/api/"

category_list = [
    'achievements', 'titles', 'mounts', 'minions', 'orchestrions', 'frames', 
    'spells', 'emotes', 'bardings', 'hairstyles', 'armoires', 'fashions', 
    'triad', 'records', 'survey records', 'leves', 'relics', 'tomestones', 
    'characters'
]

cat_df = pd.DataFrame(category_list, columns=['Category'])
cat_df.index += 1

print('''
      Welcome to FFXIV Collect, simple version!/n
      Below is a catagory list of collectables from FFXIV/n
      ''')
print(cat_df)
# cat_input = int(input('Go ahead and input the number associated with the category you\'d like to see more about:'))
cat_pick = cat_df.loc[3, 'Category']
print(f'You have selected {cat_pick}')

cat_url = api_url + cat_pick

#This code is going to be used to pull all items from that category
response = requests.get(f'{cat_url}')
data = response.json()

choice = 2 #int(input('Input 1 if you want to search mounts by source type and 2 for a top 10 list:'))


#This is used to show mounts from specific source types
if choice == 1:
    source_type_mount = []
    for result in data['results']:
        for source in result['sources']:
            if source['type'] == 'Raid':
                source_type_mount.append(result) 
#mount_df = pd.DataFrame(data['results'])
#print(data['count'])
    # stm_df = pd.DataFrame(source_type_mount)
#print(mount_df[['name']])
#print(stm_df['name'])

#Code to sort items with the most/least amount of owners
elif choice == 2:
    Most_Least = 'most' #input('Would you like to see the top 10 most or least owned mounts?')
    top_list = []
    if Most_Least == 'most':
        for results in data['results']:
            top_list.append({'name': results['name'], 'percentage owned':float(results['owned'].replace('%',''))})
    
    #print(top_list)
    sorted_top_list = sorted(top_list, key=lambda x: x['owned'], reverse=True)
    sorted_top_list_df = pd.DataFrame(sorted_top_list)
    print(sorted_top_list_df.head(10))
