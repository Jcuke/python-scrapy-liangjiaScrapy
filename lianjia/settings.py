BOT_NAME = 'lianjia'
SPIDER_MODULES = ['lianjia.spiders']
NEWSPIDER_MODULE = 'lianjia.spiders'
ITEM_PIPELINES={
    'lianjia.pipelines.LianjiaPipeline':300
}
LOG_LEVEL='DEBUG'

DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
COOKIES_ENABLED = True



# start MySQL database configure setting
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'lianjia'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
# end of MySQL database configure setting

imageStoredPath = 'd:/d/lianjia'