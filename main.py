import asyncio
import getInfo
import dailyShop
import os

async def main(user,passwd):
    print(user + ' ''s daily shop:')
    dailySkinId = await dailyShop.getDailyShop(user,passwd)
    for skin in dailySkinId:
        getInfo.showSkin(user, skin)


if __name__ == '__main__':
    os.makedirs('auth', exist_ok=True) # store auth files
    os.makedirs('save', exist_ok=True) # store daily shop files
    user = "YourUsername"
    passwd = "YourPassword"
    asyncio.run(main(user,passwd))
