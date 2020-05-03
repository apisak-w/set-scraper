from selenium import webdriver
from time import sleep


class set_crawler:
    stockCode = ""

    def __init__(self, stockCode):
        self.driver = webdriver.Chrome()
        self.stockCode = stockCode
        self.companyInfo = dict()
        self.stockInfo = dict()
        self.financial_period_cols_header = []

    def go_to_company_highlights_page(self):
        self.driver.get(
            "https://www.set.or.th/set/companyhighlight.do?symbol=" + self.stockCode + "&ssoPageId=5&language=th&country=TH")

    def get_company_info(self):
        print('Getting company info for stock code: ' + self.stockCode)

        self.driver.get(
            "https://www.set.or.th/set/companyprofile.do?symbol=" + self.stockCode + "&ssoPageId=4&language=th&country=TH")

        industryGroup = self.driver.find_element_by_xpath(
            "/html[@class='no-js']/body/div[@class='container']/div[@class='row sidebar-body-content']/div[@id='body-content']/div[@class='row']/div[@id='maincontent']/div[@class='row']/div[@class='table-reponsive']/table[@class='table']/tbody/tr[3]/td/div[@class='row']/div[@class='col-xs-12 col-md-7']/div[@class='row'][2]/div[@class='col-xs-9 col-md-5']").text
        businessType = self.driver.find_element_by_xpath(
            "/html[@class='no-js']/body/div[@class='container']/div[@class='row sidebar-body-content']/div[@id='body-content']/div[@class='row']/div[@id='maincontent']/div[@class='row']/div[@class='table-reponsive']/table[@class='table']/tbody/tr[3]/td/div[@class='row']/div[@class='col-xs-12 col-md-7']/div[@class='row'][3]/div[@class='col-xs-9 col-md-5']").text

        self.companyInfo['industryGroup'] = industryGroup
        self.companyInfo['businessType'] = businessType

        print('Getting company info success')

    def get_financial_period_column_header(self):
        print('get_financial_period_column_header')

        columnList = self.driver.find_elements_by_xpath(
            "/html[@class='no-js']/body/div[@class='container']/div[@class='row sidebar-body-content']/div[@id='body-content']/div[@class='row']/div[@id='maincontent']/div[@class='row']/div[@class='table-responsive']/table[@class='table table-hover table-info']/thead[1]/tr/th")

        # columnHeaders = []

        for index, column in enumerate(columnList):
            columnDict = dict()
            if (len(column.text) > 3):
                columnDict['index'] = index
                columnDict['text'] = column.text.replace("\n", " - ")
                self.financial_period_cols_header.append(columnDict)
                # columnHeaders.append(columnDict)
                # print("index: ", index, "text: ", column.text,
                #       " text length ", len(column.text))

        # print(columnHeaders)

        # self.financial_period_cols_header = columnHeaders

    def get_net_profit(self):
        print('get_net_profit')

    def get_company_highlights(self):
        self.go_to_company_highlights_page()
        self.get_financial_period_column_header()


    def retrieve_stock_info(self):
        self.get_company_info()
        self.get_company_highlights()

        # sleep(2)

        print("self.stockCode", self.stockCode)
        print("self.companyInfo", self.companyInfo)
        print("self.stockInfo", self.stockInfo)
        print("self.financial_period_cols_header", self.financial_period_cols_header)

stockList = open("stockList.txt", "r")
for stock in stockList:
    craw = set_crawler(stock)
    craw.retrieve_stock_info()