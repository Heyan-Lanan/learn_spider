from fastapi import FastAPI
import json,requests,re
from lxml import etree
import random
app = FastAPI()
allHeader=["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"]

@app.get("/{word}")
async def transWord(word):
    return {"message": translateV2(word)}

def translateV2(words=None):
    if words==None:
        return {'Msg':'缺少查询单词','Status':1}
    try:
        header={'User-Agent':random.choice(allHeader)}
        res=requests.get(f'https://cn.bing.com/dict/search?q={words}',headers=header)
        if str(res) =='<Response [200]>':
            dom=etree.HTML(res.text)
            #音标
            pronunciation=dom.xpath('//*[@class=" contentPadding"] /div/div/div/div/div/div/div/div/text()')[:2]
            #中英文读音
            us_en_prons=[re.findall("this,'(.*?)'",i) for i in dom.xpath('//@onmouseover') if i !='']
            lists_us_en=[us_en_prons[0][0],us_en_prons[1][0]]
            #中文用法翻译
            characteristic=dom.xpath('/html/body/div[1]/div/div/div[1]/div[1]/ul//li/span')
            meaning=dom.xpath('//*[@class=" contentPadding"] /div/div/div/div/ul/li/span[2]/span/text()')
            #词性
            characteristic=[i.text for i in characteristic if i.text !=None]
            #return----------------------------
            return  {'msg':'请求成功',
                     'word':words,
                     'Pronunciation':[{'symbolUs':pronunciation[0].replace('\xa0','').strip(),'pronun':lists_us_en[0]},
                                      {'symbolEn':pronunciation[1].replace('\xa0','').strip(),'pronun':lists_us_en[1]}],
                      'Meaning':{i:j for i,j in zip(characteristic,meaning)},
                      'Status':200}
        else:
            return {'msg':res,'Status':''}
    except ConnectionError as e:
        return {'msg':'服务器繁忙','Status':e}
    except Exception as e:
        return {'msg':'请检查单词拼写','Status':e}
    finally:
        pass
