from scrapy import cmdline

def run():
    cmdline.execute("scrapy crawl ftx".split())

if __name__ == '__main__':
    run()