import os
import time
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

two_recaptcha_api = os.environ.get('2CAPTCHA_API')
googlekey = os.environ.get('GOOGLEKEY')

if __name__ == "__main__":

    post_api = "https://2captcha.com/in.php"
    get_api = "https://2captcha.com/res.php"
    r_post = requests.post(
        post_api,
        data={
            'key':
            two_recaptcha_api,
            'method':
            'userrecaptcha',
            'version': 'v3',
            'action': 'book_sendtokindle',
            'min_score': '0.7',
            'googlekey':
            googlekey,
            'pageurl':
            'https://www.epub.vn/download/da-thit-trong-cuoc-choi-1584004714/epub'
        })

    print(r_post.content)

    id = r_post.content.decode('utf-8').split('|')[-1]

    while True:
        print("processing ")
        r_get = requests.get(
            get_api + "?key={}&action=get&id={}".format(two_recaptcha_api, id))

        print(r_get.status_code)
        print(r_get.content)

        response = r_get.content.decode('utf-8')
        if "OK" in response:
            grecaptcha_response = response.split('|')[-1]
            print(grecaptcha_response)

            r_post_link = requests.post(
                'https://api.epub.vn/api/downloadebook/da-thit-trong-cuoc-choi-1584004714/mobi',
                headers={
                    'authority': 'api.epub.vn',
                    'pragma': 'no-cache',
                    'cache-control': 'no-cache',
                    'accept': '*/*',
                    'dnt': '1',
                    'api-access-token': 'epubvn-react-app-123456',
                    'withcredentials': 'true',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
                    'content-type': 'application/json',
                    'origin': 'https://www.epub.vn',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://www.epub.vn/',
                    'accept-language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7',
                },
                data=json.dumps({'recaptchaToken': grecaptcha_response}))

            result = r_post_link.json()
            print(result)
            if "data" in result.keys():
                print("downloading ...")
                url = result['data']
                filename = re.findall(r'epubvn-ebook\/(.*)\?', url)[-1]
                print(filename)
                os.system("curl \'{}\' -o {}".format(result['data'], filename))
                exit(0)
        elif "ERROR" in response:
            exit(1)
        time.sleep(5)
