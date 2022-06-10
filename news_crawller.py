import requests
from bs4 import BeautifulSoup

from datetime import datetime
import pandas as pd
import re
from openpyxl import Workbook

title_text = []
link_text = []
source_text = []
date_text = []
# contents_text = []
result = {}
maxpage = 10
workbook = Workbook()


def date_cleansing(text):
    try:
        pattern = '\d+.(\d+).(\d+).'  # regular expression : 정규표현식
        r = re.compile(pattern)
        match = r.search(text).group(0)
        date_text.append(match)

    except AttributeError:
        pattern = '\w* (\d\w*)'
        r = re.compile(pattern)
        match = r.search(text).group(1)
        date_text.append(match)


# going to get all the needed values through discord

def crawler(keyword, sort, start_date, end_date):
    start_from = start_date.replace(".", "")
    end_to = end_date.replace(".", "")
    # gonna set up maxpage as I want the discord user to control the number of links they receive instead of setting the page they want to do the crolling
    page = 1
    maxpage_t = (maxpage - 1) * 10 + 1
    while page <= maxpage_t:
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + keyword + "&sort=" + sort + "&ds=" + start_date + "&de=" + end_date + "&nso=so%3Ar%2Cp%3Afrom" + start_from + "to" + end_to + "%2Ca%3A&start=" + str(
            page)

        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        atags = soup.select('.news_tit')

        # getting the title and link from the atag
        for atag in atags:
            title_text.append(atag.text)
            link_text.append(atag['href'])

        # getting the source of the newspaper
        source_lists = soup.select('.info_group > .press')
        for source_list in source_lists:
            source_text.append(source_list.text)

        date_lists = soup.select('.info_group > span.info')
        for date_list in date_lists:
            if date_list.text.find("면") == -1:
                date_text.append(date_list.text)

        result = {'title': title_text, 'source': source_text, 'link': link_text}
        df = pd.DataFrame(result)
        page += 10

    if start_date == end_date:
        outputFileName = start_date + '_' + keyword + '_merging.xlsx'
    else:
        outputFileName = start_date + '-' + end_date + '_' + keyword + '_merging.xlsx'

    #  need to add the excel_writer parameter below
    # df.to_excel(sheet_name="sheet1")
    writer = pd.ExcelWriter(outputFileName)   #this creates a CSV file
    df.to_excel(writer, sheet_name='sheet1')

    # Dynamically adjust the widths of all columns
    # for column in ('title', 'link'):
    #     column_width = max(df[column].astype(str).map(len).max(), len(column))
    #     col_idx = df.columns.get_loc(column)
    #     writer.sheets['sheet1'].set_column(col_idx, col_idx, column_width)

    # # Manually adjust the wifth of column 'this_is_a_long_column_name'
    # column_width = max(df[column].astype(str).map(len).max(), len(column))
    # col_idx = df.columns.get_loc('title')
    # writer.sheets['sheet1'].set_column(col_idx, col_idx, colum_width)

    writer.save()


def main():
    """
    gets all the neccessary input values
    :return:
    """
    # maxpage = input("number of pages do you want to croll: ")
    query = input("What do you want to search: ")
    sort = input("How do you want the news to sort(relation=0, latest=1, oldest=2: ")
    start_date = input("Enter the start date(ex) 2019.01.04): ")
    end_date = input("Enter the end date(ex) 2019.01.04): ")
    crawler(query, sort, start_date, end_date)


main()









