import json
import time
import auth
import aiohttp
import os
import base64


async def getDailyShop(user, passwd):
    res_auth = await auth.getAuth(user, passwd)
    access_token = res_auth.access_token
    entitlements_token = res_auth.entitlements_token
    auth_user_id = res_auth.user_id
    with open('auth/'+time.strftime('%Y-%m-%d-%H.%M.%S', time.localtime(time.time())) + '-' +user + '.txt','w') as f:
        f.write("{}\n".format(user))
        f.write("access_token: {}\n".format(access_token))
        f.write("entitlements_token: {}\n".format(entitlements_token))
        f.write("auth_user_id: {}\n".format(auth_user_id))

    url = "https://pd.ap.a.pvp.net/store/v2/storefront/" + auth_user_id
    client_platform = {
        "platformType": "PC",
        "platformOS": "Windows",
        "platformOSVersion": "10.0.19042.1.256.64bit",
        "platformChipset": "Unknown"
    }
    client_platform = base64.b64encode(json.dumps(client_platform).encode()).decode()
    with open('versionInfo.json','r') as r:
        version = json.load(r)
        version = version['version']
    headers = {
        "Content-Type": "application/json",
        "X-Riot-ClientPlatform": client_platform,
        "X-Riot-ClientVersion": version,
        "X-Riot-Entitlements-JWT": entitlements_token,
        "Authorization": "Bearer " + access_token
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            res = json.loads(await response.text())
            return res["SkinsPanelLayout"]["SingleItemOffers"]

def findAllAuthFiles():
    file_dir = 'auth/'
    for root, dirs, files in os.walk(file_dir):
        return files

def findAuth(user):
    allFile = findAllAuthFiles()
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    file = ""
    for file in allFile:
        if date in file and (user + '.txt') in file:
            print(file)
    with open('auth/'+ file,'r') as f:
        username = f.readline()
        access_token = f.readline().split()[1].strip()
        entitlements_token = f.readline().split()[1].strip()
        auth_user_id = f.readline().split()[1].strip()
        return access_token,entitlements_token,auth_user_id






