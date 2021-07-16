import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib.request
from datetime import datetime

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
    }

WeekArr = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MonthArr = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def request_magazine(url):
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def get_date():
    day = datetime.now().date()
    day_Week = datetime.now().weekday()
    print("Today is:" + str(day) + ', ' + str(WeekArr[day_Week]))
    if (day_Week == 3 or day_Week == 6):
        day = str(day)
        monthIndex = int(day.split('-')[1].split('0')[-1]) - 1
        res = day.split('-')[2] + '-' + MonthArr[monthIndex] + '-' + day.split('-')[0]
        return res


def download_and_extract(filepath, save_dir):
    """根据给定的URL地址下载文件

    Parameter:
        filepath: list 文件的URL路径地址
        save_dir: str  保存路径
    Return:
        None
    """
    for url, index in zip(filepath, range(len(filepath))):
        filename = url.split('/')[-1]
        save_path = os.path.join(save_dir, filename)
        urllib.request.urlretrieve(url, save_path)
        sys.stdout.write('\r>> Downloading %.1f%%' % (float(index + 1) / float(len(filepath)) * 100.0))
        sys.stdout.flush()
    print('\nSuccessfully downloaded')


def main():
    # url = 'https://freemagazines.top/?s=The+Economist'
    url1 = 'https://freemagazines.top/the-economist-uk-edition-' + get_date()
    url2 = 'https://freemagazines.top/the-economist-uk-' + get_date()

    html = request_magazine(url1)
    if html is None:
        print("Not found latest magazine!")
    else:
        soup = BeautifulSoup(html, 'lxml')
        for k in soup.find_all('a'):
            if 'https://app.blackhole.run' in k['href']:
                print(k['href'])
                # download_and_extract(k['href'], 'D:/downloads')


if __name__ == '__main__':
    main()
