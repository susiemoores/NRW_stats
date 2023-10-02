# setting up
import requests
response = requests.get('https://api.ffc-environment-agency.fgs.metoffice.gov.uk/api/public/v1/statements/latest_public_forecast')
response_content = response.content.decode('utf-8')
import json
data = json.loads(response_content)

# risk areas
risk_areas = data['statement']['risk_areas']
days = [block['days'] for area in risk_areas for block in area['risk_area_blocks']]
risk_levels =  [block['risk_levels'] for area in risk_areas for block in area['risk_area_blocks']]

# days and risk
dict_days = {idx+1: sublist for idx, sublist in enumerate(days)}
dict_risk = {idx+1: sublist for idx, sublist in enumerate(risk_levels)}

# counties
polys = [block['polys'] for area in risk_areas for block in area['risk_area_blocks']]
counties = {}
for i, poly in enumerate(polys):
     county_names = [county['name'] for county in poly[0]['counties']]
     counties[i+1] = county_names

wales_counties =  ['Blaenau Gwent', 'Bridgend', 'Caerphilly', 'Cardiff', 'Carmarthenshire', 'Ceredigion', 'Conwy', 'Denbighshire', 'Flintshire', 'Gwynedd', 'Isle of Anglesey', 'Merthyr Tydfil', 'Monmouthshire', 'Neath Port Talbot', 'Newport', 'Pembrokeshire', 'Powys', 'Rhondda Cynon Taff', 'Swansea', 'Torfaen', 'Vale of Glamorgan', 'Wrexham']

# threshold risks
minor = [key for key, value in dict_risk.items() if any(num[0] >= 2 for num in value.values())]
significant = [key for key, value in dict_risk.items() if any(num[0] >= 3 for num in value.values())]

# risk levels
found_risk = False
for key, value in dict_days.items():
    if key in significant and 1 in value and key in counties and any(county in wales_counties for county in counties[key]):
        print("Significant risk")

found_risk = False
for key, value in dict_days.items():
    if key in minor and 1 in value and key in counties and any(county in wales_counties for county in counties[key]):
        print("Elevated risk")
        found_risk = True
        break

if not found_risk:
    print("No elevated risk")
