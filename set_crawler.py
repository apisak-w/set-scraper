from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import re


class set_crawler:
    stock_code = ""

    def __init__(self, stock_code):
        # Init webdriver with headless
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)

        # Init constructor for crw
        self.stock_code = stock_code
        self.company_info = dict()
        self.stock_info = dict()
        self.financial_period_cols_header = []
        self.financial_statistics_cols_header = []

    def go_to_company_highlights_page(self):
        self.driver.get(
            "https://www.set.or.th/set/companyhighlight.do?symbol=" + self.stock_code + "&ssoPageId=5&language=th&country=TH")

    def get_company_info(self):
        print('Getting company info for stock code: ' + self.stock_code)

        self.driver.get(
            "https://www.set.or.th/set/companyprofile.do?symbol=" + self.stock_code + "&ssoPageId=4&language=th&country=TH")

        industry_group = self.driver.find_element_by_xpath(
            "/html[@class='no-js']/body/div[@class='container']/div[@class='row sidebar-body-content']/div[@id='body-content']/div[@class='row']/div[@id='maincontent']/div[@class='row']/div[@class='table-reponsive']/table[@class='table']/tbody/tr[3]/td/div[@class='row']/div[@class='col-xs-12 col-md-7']/div[@class='row'][2]/div[@class='col-xs-9 col-md-5']").text
        business_type = self.driver.find_element_by_xpath(
            "/html[@class='no-js']/body/div[@class='container']/div[@class='row sidebar-body-content']/div[@id='body-content']/div[@class='row']/div[@id='maincontent']/div[@class='row']/div[@class='table-reponsive']/table[@class='table']/tbody/tr[3]/td/div[@class='row']/div[@class='col-xs-12 col-md-7']/div[@class='row'][3]/div[@class='col-xs-9 col-md-5']").text

        self.company_info['industry_group'] = industry_group
        self.company_info['business_type'] = business_type

        print('Getting company info success')

    def get_financial_period_column_header(self):
        column_list = self.driver.find_elements_by_xpath(
            "/html[@class='no-js']/body/div[@class='container']/div[@class='row sidebar-body-content']/div[@id='body-content']/div[@class='row']/div[@id='maincontent']/div[@class='row']/div[@class='table-responsive']/table[@class='table table-hover table-info']/thead[1]/tr/th")

        for index, column in enumerate(column_list):
            column_dict = dict()
            if (column.text.startswith("งบปี")):
                column_dict['index'] = index + 1
                column_dict['text'] = column.text.replace("\n", " - ")
                self.financial_period_cols_header.append(column_dict)

    def get_financial_statistics_column_header(self):
        column_list = self.driver.find_elements_by_xpath(
            "/html[@class='no-js']/body/div[@class='container']/div[@class='row sidebar-body-content']/div[@id='body-content']/div[@class='row']/div[@id='maincontent']/div[@class='row']/div[@class='table-responsive']/table[@class='table table-hover table-info']/thead[2]/tr/th")

        for index, column in enumerate(column_list):
            column_dict = dict()
            date_pattern = re.compile("^\d{1,2}\/\d{1,2}\/\d{4}$")
            if (date_pattern.match(column.text)):
                column_dict['index'] = index + 1
                column_dict['text'] = column.text
                self.financial_statistics_cols_header.append(column_dict)

    def get_net_profit(self):
        profit_list = []
        for index, column in enumerate(self.financial_period_cols_header):
            profit = self.driver.find_element_by_xpath(
                "/html[@class='no-js']/body/div[@class='container']/div[@class='row sidebar-body-content']/div[@id='body-content']/div[@class='row']/div[@id='maincontent']/div[@class='row']/div[@class='table-responsive']/table[@class='table table-hover table-info']/tbody[1]/tr[7]/td[" + str(column.get("index")) + "]").text
            profit_list.append(profit.strip())
        self.stock_info['profit_list'] = profit_list

    def get_pe_value(self):
        pe_list = []
        for index, column in enumerate(self.financial_statistics_cols_header):
            pe = self.driver.find_element_by_xpath(
                "/html[@class='no-js']/body/div[@class='container']/div[@class='row sidebar-body-content']/div[@id='body-content']/div[@class='row']/div[@id='maincontent']/div[@class='row']/div[@class='table-responsive']/table[@class='table table-hover table-info']/tbody[2]/tr[4]/td[" + str(column.get("index")) + "]").text
            pe_list.append(pe)
        self.stock_info['pe_list'] = pe_list

    def get_bv_value(self):
        bv_list = []
        for index, column in enumerate(self.financial_statistics_cols_header):
            bv = self.driver.find_element_by_xpath(
                "/ html[@class='no-js']/body/div[@class='container']/div[@class='row sidebar-body-content']/div[@id='body-content']/div[@class='row']/div[@id='maincontent']/div[@class='row']/div[@class='table-responsive']/table[@class='table table-hover table-info']/tbody[2]/tr[6]/td[" + str(column.get("index")) + "]").text
            bv_list.append(bv)
        self.stock_info['bv_list'] = bv_list

    def get_company_highlights(self):
        self.go_to_company_highlights_page()
        self.get_financial_period_column_header()
        self.get_financial_statistics_column_header()
        self.get_net_profit()
        self.get_pe_value()
        self.get_bv_value()

    def retrieve_stock_info(self):
        self.get_company_info()
        self.get_company_highlights()

        # sleep(2)

        print("\n ")
        print("✅ self.stock_code", self.stock_code)
        print("✅ self.company_info", self.company_info)
        print("📈 self.stock_info", self.stock_info)
        # print("✅ self.financial_period_cols_header", self.financial_period_cols_header)
        # print("✅ self.financial_statistics_cols_header", self.financial_statistics_cols_header)
        print("\n ")


# Get list of stock
stock_list = open("stockList.txt", "r")
for stock in stock_list:
    craw = set_crawler(stock)
    craw.retrieve_stock_info()
