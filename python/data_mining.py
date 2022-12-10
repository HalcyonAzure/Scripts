import requests
import csv
from pyquery import PyQuery


class JobInfo:
    def __init__(self, company, position, salary):
        self.company = company
        self.position = position
        self.salary = salary


# 获取HTML文本
def get_html(url):
    headers = {
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'host': 'sou.zhaopin.com',
    }
    response = requests.get(url, headers=headers)
    return response.text


# 传入需要的城市、学历、职位对应的变量，limit是要爬取的页数，设置为3则返回3条url用于抓取数据
def get_urls(city, degree, position, limit):
    template = 'https://sou.zhaopin.com/?jl={city_code}&kw={position}&el={degree}&p={page}'
    urls = []
    city_code_dict = {'北京': '530',
                      '上海': '538',
                      '广州': '763',
                      '深圳': '765'}
    degree_dict = {'本科': '4',
                   '硕士': '3',
                   '博士': '1'}

    for p in range(1, limit+1):
        url = template.format(city_code=city_code_dict.get(
            city), degree=degree_dict.get(degree), position=position, page=p)
        urls.append(url)
    return urls


#  传入返回的html信息，提取出包含的JobInfo
def get_job_info(html):
    doc = PyQuery(html)
    items = doc('.positionlist a').items()
    # 创建一个JobInfo的字典
    job_info_data = []
    for item in items:
        job_position = item(
            'div[class = iteminfo__line1__jobname] span[title]').text()
        job_company = item(
            'div[class = iteminfo__line1__compname] span[title]').text()
        job_salary = item(
            'div[class = iteminfo__line2__jobdesc] p').text()

        # 将数据封装为JobInfo对象，并存入字典当中
        job_info = JobInfo(job_company, job_position,  job_salary)
        job_info_data.append(job_info)
    return job_info_data


# 循环遍历所有的url，将所有的JobInfo存入字典当中，保存在csv文件中
if __name__ == '__main__':
    # 传入需要的城市、学历、职位对应的变量，返回limit页对应的url
    urls = get_urls('北京', '本科', '财务主管', 5)
    # 创建一个JobInfo的字典
    job_info_data = []
    cnt = 0
    for url in urls:
        html = get_html(url)
        job_info_data.extend(get_job_info(html))
    # 将数据按照 公司名称、职位、薪资 保存在csv文件中
    with open('job_info.csv', 'w', encoding='utf-8') as f:
        f.write('公司名称,职位,薪资\n')
        for job_info in job_info_data:
            f.write(job_info.company + ',' +
                    job_info.position + ',' + job_info.salary + ',\n')
            cnt += 1
    print('共爬取{}条数据'.format(cnt))
    # 测试爬取
