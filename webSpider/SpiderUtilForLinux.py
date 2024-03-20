import os
import redis

def kill_driver():
    os.system('taskkill /f /t /im chromedriver.exe')

def create_spider(job_name, job_url):
    if(os.getcwd().split('\\')[-1]!='spider'):
        os.chdir('spider')
    os.system('scrapy genspider -t mycrawl '+job_name+' '+job_url)
    os.chdir('../')

def run_spider(spiderName, options):
    if(os.getcwd().split('\\')[-1]!='spider'):
        os.chdir('spider')
    flag = False
    if 'DOWNLOADER_MIDDLEWARES' in options:
        midd_key, midd_value = options.popitem()
        flag = True
    keys = options.keys()
    options_param = "";
    if len(keys)>=1:
        for key in keys:
            options_param = options_param+" -d "+str(key)+"="+str(options[key])
    os.system('scrapyd-deploy')
    if flag==True:
        print('curl http://localhost:6800/schedule.json -d project=spider -d spider='+spiderName+options_param+' -d DOWNLOADER_MIDDLEWARES="'+midd_value+'"')
        os.system('curl http://localhost:6800/schedule.json -d project=spider -d spider='+spiderName+options_param+' -d DOWNLOADER_MIDDLEWARES="'+midd_value+'"')
    else:
        print('curl http://localhost:6800/schedule.json -d project=spider -d spider='+spiderName+options_param)
        os.system('curl http://localhost:6800/schedule.json -d project=spider -d spider='+spiderName+options_param)

    if(os.getcwd().split('\\')[-1]=='spider'):
        os.chdir('../')