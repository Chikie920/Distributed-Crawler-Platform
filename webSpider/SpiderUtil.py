import os
import redis
import time
import requests

def get_log(url):
    res = requests.get(url)
    # res.encoding = res.apparent_encoding
    return res.text

def kill_driver():
    os.system('taskkill /f /t /im chromedriver.exe')

def add_url(spiderName ,url):
    redis_connection = redis.Redis(host='127.0.0.1', port= 6379, db= 0) # 连接redis数据库
    redis_connection.rpush(spiderName+':urls', url) # 新增目标链接
    redis_connection.close()

def create_spider(job_name, job_url):
    if(os.getcwd().split('\\')[-1]!='spider'):
        os.chdir('spider')
    os.system('scrapy genspider -t mycrawl '+job_name+' '+job_url)
    os.chdir('../')

def run_spider(spiderName, options):
    if(os.getcwd().split('\\')[-1]!='spider'):
        os.chdir('spider')
    # rules_flag = False
    # midd_flag = False
    # if 'rules' in options:
    #     rules_key, rules_value = options.popitem()
    #     rules_flag = True
    # print('**********')
    # print(options)
    flag = False
    if 'DOWNLOADER_MIDDLEWARES' in options:
        midd_key, midd_value = options.popitem()
        flag = True
    keys = options.keys()
    options_param = "";
    if len(keys)>=1:
        for key in keys:
            options_param = options_param+" -d "+str(key)+"="+str(options[key])
    # if rules_flag==True and midd_flag==False:
    #     print('curl http://localhost:6800/schedule.json -d project=spider -d spider='+spiderName+' -d rules='+rules_value)
    #     os.system('curl http://localhost:6800/schedule.json -d project=spider -d spider='+spiderName+' -d rules='+rules_value)
    #     # os.system('scrapy crawl '+spiderName+' -a rules='+rules_value+options_param)
    # elif rules_flag==False and midd_flag==True:
    #     print('scrapy crawl '+spiderName+' -d middleWare="'+midd_value+'"'+options_param)
    #     # os.system('scrapy crawl '+spiderName+' -a middleWare="'+midd_value+'"'+options_param)
    # elif rules_flag==True and midd_flag==True:
    #     print('scrapy crawl '+spiderName+' -d rules='+rules_value+' -d middleWare="'+midd_value+'"'+options_param)
    #     # os.system('scrapy crawl '+spiderName+' -a rules='+rules_value+' -a middleWare="'+midd_value+'"'+options_param)
    # else:
    #     print('scrapy crawl '+spiderName+options_param)
        # os.system('scrapyd-deploy')
        # time.sleep(1)
    #     print('curl http://localhost:6800/schedule.json -d project=spider -d spider='+spiderName+options_param)
    #     os.system('curl http://localhost:6800/schedule.json -d project=spider -d spider='+spiderName+options_param)
        # os.system('scrapy crawl '+spiderName+options_param)
        # os.system('scrapy crawl '+spiderName+options_param)
    # os.system('scrapy crawl '+spiderName+options_param)
    os.system('scrapyd-deploy')
    if flag==True:
        print('curl http://localhost:6800/schedule.json -d project=spider -d spider='+spiderName+options_param+' -d DOWNLOADER_MIDDLEWARES="'+midd_value+'"')
        os.system('curl http://localhost:6800/schedule.json -d project=spider -d spider='+spiderName+options_param+' -d DOWNLOADER_MIDDLEWARES="'+midd_value+'"')
    else:
        print('curl http://localhost:6800/schedule.json -d project=spider -d spider='+spiderName+options_param)
        os.system('curl http://localhost:6800/schedule.json -d project=spider -d spider='+spiderName+options_param)

    if(os.getcwd().split('\\')[-1]=='spider'):
        os.chdir('../')