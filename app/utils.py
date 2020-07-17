from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import csv
from datetime import date, timedelta


class WebDriver:
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def get_download_link(company_name: str):
    with WebDriver(webdriver.Remote("http://chromedriver:4444/wd/hub", DesiredCapabilities.CHROME)) as driver:
        driver.get(f'https://finance.yahoo.com/quote/{company_name}/history?p={company_name}')
        if driver.current_url != f'https://finance.yahoo.com/quote/{company_name}/history?p={company_name}':
            return
        delay = 10  # seconds
        try:
            datepicker = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                            '.drop-down-selector.historical'
                                                                                            ' div div div div div')))
            datepicker.click()
        except TimeoutException:
            print("Loading took too much time!")
            exit()
        driver.find_element_by_id('dropdown-menu').find_element_by_xpath('//button[@data-value="MAX"]').click()
        link = driver.find_element_by_xpath(f'//a[@download="{company_name}.csv"]').get_attribute('href')
        return link


def download_file(company_name: str, link: str):
    response = requests.get(link)
    if response.status_code == 200:
        with open(f'../files/{company_name}.csv', 'wb') as f:
            f.write(response.content)


def calculate_before_change(filename: str, days: int):
    rows = []
    with open(filename) as file:
        file.readline()
        for line in file:
            row = line.strip().split(',')
            rows.append(row)
    with open(filename, 'w') as file:
        file.write('Date,Open,High,Low,Close,Adj Close,Volume,3day_before_change\n')
        file.write(','.join(rows[0]) + ',-\n')

        for i in range(1, days):
            for n in range(1, days):
                if date.fromisoformat(rows[i][0]) - date.fromisoformat(rows[i-n][0]) == timedelta(days=3):
                    ratio = float(rows[i][4]) / float(rows[i-n][4])
                    file.write(','.join(rows[i]) + f',{ratio}\n')
                    break
            else:
                file.write(','.join(rows[i]) + ',-\n')

        for i in range(days, len(rows)):
            for n in range(1, days + 1):
                if date.fromisoformat(rows[i][0]) - date.fromisoformat(rows[i-n][0]) == timedelta(days=3):
                    ratio = float(rows[i][4]) / float(rows[i-n][4])
                    file.write(','.join(rows[i]) + f',{ratio}\n')
                    break
            else:
                file.write(','.join(rows[i]) + ',-\n')


def get_news(company_name: str):
    with WebDriver(webdriver.Remote("http://chromedriver:4444/wd/hub", DesiredCapabilities.CHROME)) as driver:
        driver.get(f'https://finance.yahoo.com/quote/{company_name}/')
        if driver.current_url != f'https://finance.yahoo.com/quote/{company_name}/':
            return
        news = []
        for elem in driver.find_elements_by_xpath('//div[@id="quoteNewsStream-0-Stream"]/ul/*'):
            news.append(
                (
                    elem.find_element_by_xpath('.//div/div/div/h3/a').get_attribute('href'),
                    elem.find_element_by_xpath('.//div/div/div/h3').text,

                )
            )
        return news


def write_news_to_file(company_name: str, news: list):
    with open(f'../files/{company_name}-news.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        csvwriter.writerow(['link', 'title'])
        for elem in news:
            csvwriter.writerow(elem)
