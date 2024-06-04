This repo is for checking daily store in valorant based on repo [riot_auth](https://github.com/floxay/python-riot-auth)(for authentication), [valapidocs.techchrism.me APIs](https://valapidocs.techchrism.me/)(for store checking) and [dash.valorant-api.com APIs](https://dash.valorant-api.com/)(for retrieving all info of bundles and skins).
# How to use
1. Clone this repo
```bash
git clone
```
2. Install requirements
```bash
pip install -r requirements.txt
```
3. Run getInfo.py to fetch all info of client version, bundles and skins
```bash
python getInfo.py
```
4. Replace your username and password in main.py, then run main.py. Your daily store will be checked and saved in dir store/ and your account info will be saved in dir auth/ to avoid re-authentication.
```bash
python main.py
```