import pandas as pd
import requests
import json, os
from datetime import datetime

## create package
def sendMetaToCkan(url_ckan, api_key, ckan_meta):
    headers = {
        'content-type': 'application/json',
        'Authorization': api_key,
    }

    url = '{}/api/action/package_create'.format(url_ckan)
    respond = requests.post(url, data=json.dumps(ckan_meta), headers=headers)
    res_text = respond.content.decode('utf-8').replace('\n','br')
    print(res_text)
    
## Upload File
def uploadFileToCkan(url_ckan, api_key, file_meta, path_input):
    headers = {'X-CKAN-API-Key': api_key}
    url = '{}/api/action/resource_create'.format(url_ckan)
    with open(path_input, "rb") as f:
        form_file = {'upload': f}
        respond = requests.post(url, data=file_meta, headers=headers, files=form_file)
        res_text = respond.content.decode('utf-8').replace('\n','br')
        print(res_text)
        print('<b>File has been uploaded</b>')

dfs = pd.read_html(os.getenv("WEB_SCRIPY","https://docs.google.com/spreadsheets/d/e/2PACX-1vQlEs3FxFPwm-dpvU1YdsfRgsbfT9WdiXJHZm9kJgGTziPnk-y3TWtftbSbxj6Fe_g0NxYgqyVHTVU5/pubhtml?gid=1397577608&amp;single=true&amp;widget=true&amp;headers=false"), header=[1])
df = dfs[0]
df.drop(df.columns[0], axis = 1, inplace=True)
df.to_csv('df.csv', index=False)

ckan_meta = json.load(open('metadata.json', encoding='utf-8'))

url_ckan = os.getenv("CKAN_URL","https://ckan.data.storemesh.com" )  # ใส่ ip ของ ckan server ตรงนี้
api_key = os.getenv("TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODI1NzcwNjMsImp0aSI6IndDbWVpamtiXzg3ZWJuc1RFb3BxTW1JZi1LcEhHbklrN21qZ1ZuNTB4d0NlNVR2dFRkY2VQbFlPUENucE8wRDI4NlNuQk90S08xc1ozeTg1In0.8uL2ToWIGoI4yl62VJI0SckFWKUR5FoC9YVJPCQqi0s") 


now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
## for upload file
file_meta = {
    'package_id': ckan_meta['name'],
    'name': f'data-scripy-{now}',
}
# path_input = './result.csv'
path_input = './df.csv'
# sendMetaToCkan(url_ckan, api_key, ckan_meta)
uploadFileToCkan(url_ckan, api_key, file_meta, path_input)
