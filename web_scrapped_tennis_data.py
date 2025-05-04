import pandas as pd
import json
import requests

#TABLE 1: Competitions & Categories

# Define API URL for fetching competitions data
url = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key=t3DQmkntThdylaEvkOIpO88IgPKVd4tBQ6ZtpuGW"
headers = {"accept": "application/json"}
competitions_response = requests.get(url, headers=headers)

# Convert JSON response to Python dictionary
competitions_data_api = json.loads(competitions_response.text)

# Initialize empty lists to store competitions and category data
competitions_data = []
categorys_data = []

# Loop through competitions to extract relevant fields
for competitions in competitions_data_api['competitions']:
    category = competitions['category']
    
    # Store competition-related information
    competitions_data.append({
        'competition_id': competitions.get('id', "N/A"),
        'competition_name': competitions.get('name', "N/A"),
        'parent_id': competitions.get('parent_id', "N/A"),
        'type': competitions.get('type', "N/A"),
        'gender': competitions.get('gender', "N/A"),
        'category_id': category.get('id', "N/A")
    })
    
    # Store category-related information
    categorys_data.append({
        'category_id': category.get('id', "N/A"),
        'category_name': category.get('name', "N/A")
    })

# Create DataFrames from the extracted data
competitions_table = pd.DataFrame(competitions_data)
categorys_table = pd.DataFrame(categorys_data).drop_duplicates(subset='category_id')

# Merge competition and category table using a left join
category_merge_table = pd.merge(
    categorys_table,
    competitions_table[['category_id', 'competition_id', 'competition_name', 'parent_id', 'type', 'gender']],
    on='category_id',
    how='left'
)

# Save merged table to CSV
category_merge_table.to_csv('category_table.csv', index=False)
# -------------------------------------------------------------------------------------------------------------------------------------------------------

#TABLE 2: Complexes & Venues

# Define API URL for fetching complexes data
url = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json?api_key=t3DQmkntThdylaEvkOIpO88IgPKVd4tBQ6ZtpuGW"
complexes_response = requests.get(url, headers=headers)

# Convert JSON response to Python dictionary
complexes_data_api = json.loads(complexes_response.text)

# Initialize lists to store complexes and venues data
complexes_data = []
venues_data = []

# Loop through each complex and extract venue data
for complexes in complexes_data_api['complexes']:
    # Store complex-level information
    complexes_data.append({
        "complex_id": complexes.get('id', "N/A"),
        'complex_name': complexes.get('name', "N/A")
    })
    
    # Extract venue details within the complex
    venues_temp = complexes.get('venues', [])
    if venues_temp:
        for venues in venues_temp:
            venues_data.append({
                'venue_id': venues.get('id', "N/A"),
                'venue_name': venues.get('name', "N/A"),
                'city_name': venues.get('city_name', "N/A"),
                'country_name': venues.get('country_name', "N/A"),
                'country_code': venues.get('country_code', "N/A"),
                'timezone': venues.get('timezone', "N/A"),
                'complex_id': complexes.get('id', "N/A")
            })

# Create DataFrames from the extracted data
complexes_table = pd.DataFrame(complexes_data)
venues_table = pd.DataFrame(venues_data)

# Merge venues with corresponding complex names
complex_merge_table = pd.merge(
    venues_table,
    complexes_table[['complex_id', 'complex_name']],
    on='complex_id',
    how='left'
)

# Save merged table to CSV
complex_merge_table.to_csv("complex_table.csv", index=False)
# -------------------------------------------------------------------------------------------------------------------------------------------------------

#TABLE 3: Doubles Competitor Rankings

# Define API URL for fetching doubles competitors rankings
url = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json?api_key=t3DQmkntThdylaEvkOIpO88IgPKVd4tBQ6ZtpuGW"
doubles_rankings_response = requests.get(url, headers=headers)

# Convert JSON response to Python dictionary
doubles_rankings_data_api = json.loads(doubles_rankings_response.text)

# Initialize lists to store rankings and competitor details
competitor_rankings_data = []
competitors_data = []

# Extract rankings and corresponding competitor information
for rankings in doubles_rankings_data_api['rankings']:
    for competitor_rankings in rankings['competitor_rankings']:
        competitor = competitor_rankings['competitor']
        
        # Store ranking-related info
        competitor_rankings_data.append({
            'rank': competitor_rankings.get('rank', "N/A"),
            'movement': competitor_rankings.get('movement', "N/A"),
            'points': competitor_rankings.get('points', "N/A"),
            'competitions_played': competitor_rankings.get('competitions_played', "N/A"),
            'competitor_id': competitor.get('id', "N/A")
        })
        
        # Store competitor-specific info
        competitors_data.append({
            'competitor_id': competitor.get('id', "N/A"),
            'name': competitor.get('name', "N/A"),
            'country': competitor.get('country', "N/A"),
            'country_code': competitor.get('country_code', "N/A"),
            'abbreviation': competitor.get('abbreviation', "N/A")
        })

# Create DataFrames
competitor_rankings_table = pd.DataFrame(competitor_rankings_data)
competitors_table = pd.DataFrame(competitors_data)

# Merge rankings with competitor details
competitor_merge_table = pd.merge(
    competitor_rankings_table,
    competitors_table[['competitor_id', 'name', 'country', 'country_code', 'abbreviation']],
    on='competitor_id',
    how='left'
)

# Set a new index starting from 1
competitor_merge_table.index = competitor_merge_table.index + 1
competitor_merge_table.index.name = 'rank_id'

# Save merged table to CSV
competitor_merge_table.to_csv('competitor_merge_table.csv', index=True)