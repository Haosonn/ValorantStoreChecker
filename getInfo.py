import asyncio
import json
import time
import aiohttp

async def fetch_skins_all():
    url = "https://valorant-api.com/v1/weapons/skins"
    headers = {'Connection': 'close'}
    params = {"language": "en-US"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            res_skin = json.loads(await response.text())['data']
            with open('skinInfo.json','w') as r:
                r.write(json.dumps(res_skin))

def showSkin(user, uuid):
    with open('save/' + time.strftime('%Y-%m-%d daily store', time.localtime(time.time())) + '-' + user + '.txt','a') as f:
        allSkins = json.load(open('skinInfo.json', 'r'))
        allBundles = json.load(open('bundleInfo.json', 'r'))
        for skin in allSkins:
            for i in skin['levels']:
                if (i['uuid']) == uuid:
                    f.write("{}\n".format(skin['displayName']))
                    f.write("{}\n".format(skin['displayIcon']))
                    print(skin['displayName'])
                    print(skin['displayIcon'])
                    for bundle in allBundles:
                        if bundle['displayName'] in skin['displayName']:
                            print('Bundle: ', bundle['displayIcon'])

async def fetch_bundles_all():
    url = "https://valorant-api.com/v1/bundles"
    headers = {'Connection': 'close'}
    params = {"language": "en-US"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            res_bundle = json.loads(await response.text())['data']
            for bundle in res_bundle:
                print(bundle['displayName'], bundle['displayIcon'])
            with open('bundleInfo.json','w') as r:
                r.write(json.dumps(res_bundle))



async def fetch_version():
    url = "https://valorant-api.com/v1/version"
    headers = {'Connection': 'close'}
    params = {"language": "en-US"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            res_version = json.loads(await response.text())['data']
            with open('versionInfo.json','w') as r:
                r.write(json.dumps(res_version))

if __name__ == '__main__':
    asyncio.run(fetch_skins_all())
    asyncio.run(fetch_bundles_all())
    asyncio.run(fetch_version())