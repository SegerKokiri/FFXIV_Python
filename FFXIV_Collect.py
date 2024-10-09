#Simple tool to just copy some stuff from FFXIV 
                                         
import requests
import json
import pandas as pd

#Sample character ID 2277896


api_url = "https://ffxivcollect.com/api/"
xivapi_url = "https://xivapi.com/"

category_list = [
    'mounts', 'minions', 'character info'
]

cat_df = pd.DataFrame(category_list, columns=['Category'])
cat_df.index += 1

print('''
      Welcome to FFXIV Collect, simple version!\n
      Below is a catagory list of collectables from FFXIV
      ''')
print(cat_df)
print('')
cat_input = int(input('Go ahead and input the number associated with the category you\'d like to see more about: '))
cat_pick = cat_df.loc[cat_input, 'Category']
print(f'\nYou have selected {cat_pick}\n')
character_id = '2277896'
if cat_input == 3:
    character_id = input('Go ahead and put in your character lodestone ID: ')
    cat_url = api_url + 'characters/' + character_id
else:
    cat_url = api_url + cat_pick

#This code is going to be used to pull all items from that category
response = requests.get(f'{cat_url}')
data = response.json()
choice = 0

def search_item(type):
    source_type_mount = []
    for result in data['results']:
        for source in result['sources']:
            if source['type'] == type:
                source_type_mount.append(result)
    mount_df = pd.DataFrame(data['results'])
    print(f'Total mounts that are from source {type} is {len(source_type_mount)}\n')
    stm_df = pd.DataFrame(source_type_mount)
    #print(mount_df[['name']])
    stm_df.index += 1
    print(stm_df['name'])

#If character info is selected
if cat_input == 3:
    #for key in data.keys():
        #print(key)
    # character_df = pd.json_normalize(data)
    name = data['name']
    server = data['server']
    print(f'\nThis characters\'s name is {name}, from the {server} server.\n')
    character_choice = input(f'Would you like to see more about {name}\'s achievements, mounts, or minions? ')
    print('')
    if character_choice == 'achievements':
        achievements = data['achievements']
        ranks = data['rankings']
        points_total = achievements['ranked_points']
        server_ranked = ranks['achievements']['server']
        print(f'{name} currently has {points_total} achievement points and server rank of {server_ranked}.')
    elif character_choice == 'mounts':
        mounts = data['mounts']
        ranks = data['rankings']
        points_total = mounts['count']
        server_ranked = ranks['mounts']['server']
        print(f'{name} currently has {points_total} mounts and server rank of {server_ranked}.')
    elif character_choice == 'minions':
        mounts = data['minions']
        ranks = data['rankings']
        points_total = mounts['count']
        server_ranked = ranks['minions']['server']
        print(f'{name} currently has {points_total} minions and server rank of {server_ranked}.')
else:
    type_list=[]
    for result in data['results']:
        for source in result['sources']:
            if source['type'] not in type_list:
                type_list.append(source['type'])
    type_list_df = pd.DataFrame(type_list, columns=['Name'])
    type_list_df.index += 1

    choice = int(input(f'Input 1 if you want to search {cat_pick} by source type and 2 for a top 10 list: '))


#This is used to show mounts from specific source types

    if choice == 1:
        print(type_list_df)
        source_type = int(input('\nWhat source would you like to search? '))
        source_type -= 1
        search_item(type_list[source_type])

#Code to sort items with the most/least amount of owners
    elif choice == 2:
        Most_Least = input(f'Would you like to see the top 10 most or least owned {cat_pick}? ')
        top_list = []
        a_or_d = False
        if Most_Least == 'most':
            a_or_d = True
        for results in data['results']:
            top_list.append({'name': results['name'], 'percentage owned':float(results['owned'].replace('%',''))})
    
    #print(top_list)
        sorted_top_list = sorted(top_list, key=lambda x: x['percentage owned'], reverse=a_or_d)
        sorted_top_list_df = pd.DataFrame(sorted_top_list)
        sorted_top_list_df.index += 1
        print(sorted_top_list_df.head(10))
    
