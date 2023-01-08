from multiprocessing.dummy import Pool
import requests
import random
import re
from lxml import etree

urls = []


def get_url():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
    }
    url = 'https://www.pearvideo.com/category_5'
    page_text = requests.get(url=url, headers=header).text
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//ul[@id="listvideoListUl"]/li')
    for li in li_list:
        detail_url = 'https://www.pearvideo.com/' + li.xpath('./div/a/@href')[0]
        name = li.xpath('./div/a/div[2]/text()')[0] + '.mp4'
        print(detail_url, name)
        contId = re.findall('_(.*)', detail_url)[0]
        # print(contId)
        mrd = random.random()
        params = {
            "contId": contId,
            "mrd": mrd
        }
        video_url = "https://www.pearvideo.com/videoStatus.jsp"
        header["Referer"] = detail_url
        video_response = requests.get(url=video_url, headers=header, params=params).text
        # print(video_response)
        fake_video_url = re.findall('"srcUrl":"(.*?)"', video_response)[0]
        # print(fake_video_url)
        url1 = re.findall('https://.*?/.*?/.*?/.*?/(.*?)-', fake_video_url)[0]
        real_video_url = re.sub(url1, 'cont-' + contId, fake_video_url)
        print(real_video_url)
        dic = {
            'name': name,
            'url': real_video_url
        }
        urls.append(dic)


def get_video(dic2):
    url2 = dic2['url']
    header2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
    }
    data = requests.get(url=url2, headers=header2).content
    with open(dic2['name'], 'wb') as fp:
        fp.write(data)
        print(dic2['name'])


get_url()
pool = Pool(4)
pool.map(get_video, urls)
