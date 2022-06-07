from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import filefunctions

# set up main driver
path = 'C:\Program Files (x86)\chromedriver.exe'


def initiate_driver():
    return webdriver.Chrome(path)


# get paper abstract
# def get_abstract(driver, clickable):
#     link = driver.find_element(By.LINK_TEXT, str(clickable))
#     link.click()
#     abstract = driver.find_element(By.CLASS_NAME, 'research-detail-middle-section__abstract')
#     print(abstract.text)
#     driver.back()


# extract search result paper titles
def get_titles(driver):
    return driver.find_elements(By.CLASS_NAME, 'nova-legacy-v-publication-item__title')


def get_authors(driver):
    return driver.find_elements(By.CLASS_NAME, 'nova-legacy-v-publication-item__person-list')


def get_url(driver):
    items = driver.find_elements(By.CLASS_NAME, 'nova-legacy-e-link')
    links = []
    for item in items:
        link = str(item.get_attribute('href'))
        if link not in links:
            links.append(link)
    return links


# search keyword at researchgate function
def find_based_on_search(driver, string):
    driver.get('https://www.researchgate.net/')
    search = driver.find_element(By.CLASS_NAME, 'index-search-field__input')
    search.send_keys(str(string))
    search.send_keys(Keys.RETURN)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-results-container"))
        )
        titles = get_titles(driver)
        authors = get_authors(driver)
        url = get_url(driver)
        for i in range(len(titles)):
            titles_list.append(titles[i].text)
            links_list.append(url[i])
    finally:
        driver.quit()


def run_scrapper(keyword):
    driver = initiate_driver()
    find_based_on_search(driver, str(keyword))


def get_abstract(driver, link):
    driver.get(link)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "research-detail-middle-section__abstract"))
        )
        abstract = driver.find_element(By.CLASS_NAME, 'research-detail-middle-section__abstract')
        abstract_list.append(abstract.text)
    except Exception as e:
        abstract = 'none'
        abstract_list.append(abstract)
        driver.quit()


# test functions here
links_list = []
titles_list = []
abstract_list = []


def run_rsg(keywords):
    for keyword in keywords:
        try:
            run_scrapper(keyword)
        except Exception as e:
            initiate_driver()
        data = {
            'Judul': titles_list,
            'Link': links_list,
        }
        # View Dictionary
        print('Artikel {}'.format(keyword))
        print('Judul: {}'.format(data['Judul']))
        print('Link: {}'.format(data['Link']))

    for link in links_list:
        get_abstract(initiate_driver(), link)

    data['Abstrak'] = abstract_list

    #  create dataframe
    return filefunctions.create_dataframe(data)


