import requests

if __name__ == "__main__":
    url = 'https://www.sogou.com/'  # 指定url
    response = requests.get(url)  # 发起请求
    page_text = response.text  # 获取响应数据, 返回字符串
    print(page_text)
    with open('./sogou.html', 'w', encoding='utf-8') as fp:  # 存储
        fp.write(page_text)
    print('爬取数据结束')
