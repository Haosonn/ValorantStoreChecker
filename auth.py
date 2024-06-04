import asyncio
import json
from urllib.parse import parse_qsl, urlsplit
import aiohttp
import riot_ssl
from base64 import urlsafe_b64decode
from secrets import token_urlsafe

class Auth:
    def __init__(self, access_token, entitlements_token, user_id):
        self.access_token = access_token
        self.entitlements_token = entitlements_token
        self.auth_user_id = user_id

async def getAuth(user, passwd):
    with open('versionInfo.json','r') as r:
        version = json.load(r)
        val_version = version['riotClientBuild']
    RIOT_CLIENT_USER_AGENT = (
        f"RiotClient/{val_version} %s (Windows;10;;Professional, x64)"
    )
    res = Auth('','','')
    conn = aiohttp.TCPConnector(ssl = riot_ssl.RiotSSL.create_ssl_ctx())
    async with aiohttp.ClientSession(
        connector=conn, raise_for_status=True, cookie_jar = aiohttp.CookieJar()
    ) as session:
        headers = {
            "Accept-Encoding": "deflate, gzip, zstd",
            "user-agent": RIOT_CLIENT_USER_AGENT % "rso-auth",
            "Cache-Control": "no-cache",
            "Accept": "application/json",
        }
        body = {
            "acr_values": "",
            "claims": "",
            "client_id": "riot-client",
            "code_challenge": "",
            "code_challenge_method": "",
            "nonce": token_urlsafe(16),
            "redirect_uri": "http://localhost/redirect",
            "response_type": "token id_token",
            "scope": "openid link ban lol_region account",
        }
        async with session.post(
            "https://auth.riotgames.com/api/v1/authorization",
            json=body,
            headers=headers,
        ) as r:
            data = await r.json()

        body = {
            "language": "en_US",
            "password": passwd,
            "region": None,
            "remember": False,
            "type": "auth",
            "username": user,
        }
        async with session.put(
                "https://auth.riotgames.com/api/v1/authorization",
                json=body,
                headers=headers,
        ) as r:
            data = await r.json()
            mode = data["response"]["mode"]
            uri = data["response"]["parameters"]["uri"]
            data = getattr(urlsplit(uri), mode)
            data = dict(parse_qsl(data))
            res.access_token = data['access_token']
            headers["Authorization"] = "{} {}".format(data['token_type'], data['access_token'])
        async with session.post(
            "https://entitlements.auth.riotgames.com/api/token/v1",
            headers=headers,
            json={},
        ) as r:
            data = await r.json()
            res.entitlements_token = data["entitlements_token"]
        payload = res.access_token.split(".")[1]
        decoded = urlsafe_b64decode("{}===".format(payload))
        res.user_id = json.loads(decoded)['sub']
        return res


