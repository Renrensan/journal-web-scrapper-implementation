from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import filefunctions

# set up main driver
path = 'C:\Program Files (x86)\chromedriver.exe'


def initiate_driver():
    return webdriver.Chrome(path)


def search_keyword(string, links_list, page):
    driver = initiate_driver()
    driver.get('https://jurnal.ugm.ac.id/jsp/search/'
               'search?query={}&searchJournal=84&authors=&'
               'title=&abstract=&galleyFullText=&suppFiles=&'
               'discipline=&subject=&type=&coverage=&indexTerms=&'
               'dateFromMonth=&dateFromDay=&dateFromYear=&dateToMonth='
               '&dateToDay=&dateToYear=&orderBy=&orderDir=&search'
               'Page={}#results'.format(string, page))
    # search = driver.find_element(By.ID, 'query')
    # search.send_keys(str(string))
    # search.send_keys(Keys.RETURN)
    try:
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "listing"))
        )
        # Get the search results text
        search_results = results.text
        paper_links = results.find_elements(By.CLASS_NAME, 'file')

        # Separate the links to each paper
        for item in paper_links:
            paper_link = str(item.get_attribute('href'))
            if paper_link not in links_list:
                links_list.append(paper_link)
    finally:
        driver.quit()
    return search_results


def clean_search(results):
    clean_abs_regex = r'ABSTRACT'
    replace_pdf_regex = r'PDF'
    replace_colon_regex = r'\):'
    replace_whitespace_regex = r'\r\n|\r|\n'
    clean_search_results = re.sub(clean_abs_regex, '', results)
    clean_search_results = re.sub(replace_pdf_regex, ';', clean_search_results)
    clean_search_results = re.sub(replace_colon_regex, ');', clean_search_results)
    clean_search_results = re.sub(replace_whitespace_regex, ';', clean_search_results)
    # clean_search_results = re.sub(remove_navigation, '', clean_search_results)
    print(clean_search_results)
    print(clean_search_results)
    return clean_search_results


def split_results(clean_results):
    # Create results list by splitting the string with ';' as separator
    splitter = r';'
    split_results_list = re.split(splitter, clean_results)

    # Remove 'ISSUE TITLE' from results list
    split_results_list.remove('  ISSUE TITLE')

    # # Append the navbar into the nav_list and remove it from the results list
    # nav_list.append(split_results_list[len(split_results_list) - 1])
    split_results_list.remove(split_results_list[len(split_results_list) - 1])

    # Remove all empty elements in the results list
    while '' in split_results_list:
        split_results_list.remove('')
    while ' ' in split_results_list:
        split_results_list.remove(' ')

    # Re-split results list into smaller list per paper
    split_results_list = [split_results_list[x:x + 3] for x in range(0, len(split_results_list), 3)]
    print(split_results_list)
    return split_results_list


def extract_paper_info(titles_list, authors_list, results_list):
    # Extract paper volumes, titles, and authors from the results list
    for items in results_list:
        # Clean titles before appending
        month_regex = 'JANUARI \\([a-zA-Z, ]+\\)|FEBRUARI \\([a-zA-Z, ]+\\)' \
                      '|MARET \\([a-zA-Z, ]+\\)|APRIL \\([a-zA-Z, ]+\\)|MEI \\([a-zA-Z, ]+\\)' \
                      '|JUNI \\([a-zA-Z, ]+\\)|JULI \\([a-zA-Z, ]+\\)' \
                      '|AGUSTUS \\([a-zA-Z, ]+\\)|SEPTEMBER \\([a-zA-Z, ]+\\)' \
                      '|OKTOBER \\([a-zA-Z, ]+\\)|NOVEMBER \\([a-zA-Z, ]+\\)' \
                      '|DESEMBER \\([a-zA-Z, ]+\\)|January \\([a-zA-Z, ]+\\)' \
                      '|February \\([a-zA-Z, ]+\\)|March \\([a-zA-Z, ]+\\)' \
                      '|April \\([a-zA-Z, ]+\\)|May \\([a-zA-Z, ]+\\)' \
                      '|June \\([a-zA-Z, ]+\\)|July \\([a-zA-Z, ]+\\)' \
                      '|Juli \\([a-zA-Z, ]+\\)|August \\([a-zA-Z, ]+\\)' \
                      '|September \\([a-zA-Z, ]+\\)|October \\([a-zA-Z, ]+\\)|' \
                      'November \\([a-zA-Z, ]+\\)|December \\([a-zA-Z, ]+\\)|JANUARI|' \
                      'FEBRUARI|MARET|APRIL|MEI|JUNI|JULI|AGUSTUS|SEPTEMBER|OKTOBER|' \
                      'NOVEMBER|DESEMBER|Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|' \
                      'September|Oktober|November|Desember|January|February|March|April|May|June|July|August' \
                      '|October|December'
        t = re.sub(month_regex, '', items[1])
        if t not in titles_list:
            titles_list.append(t)
            authors_list.append(items[2])
        else:
            continue
    return titles_list, authors_list


def get_abstract(driver, abstract_links_list):
    abstract_list = []
    for abstract_link in abstract_links_list:
        driver.get(abstract_link)
        try:
            abstract = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "articleAbstract"))
            )
            abstract_text = abstract.text
            # Clean abstract text
            abstract_cleaner_regex = 'Abstract\\n\\n'
            abstract_text = re.sub(abstract_cleaner_regex, '', abstract_text)
            abstract_list.append(abstract_text)
        except Exception as e:
            driver.quit()
    return abstract_list


def split_links(links_list):
    abstract_links_list = links_list[::2]
    pdf_links_list = links_list[1::2]
    return abstract_links_list, pdf_links_list


def run_ugm(keywords):
    links = []
    titles = []
    authors = []
    pages_limit = 5
    for keyword in keywords:
        for page in range(1,5):
            results = search_keyword(keyword, links, page)
            if re.search('No Results', results):
                print('Paper Not Found')
                continue
            clean_results = clean_search(results)
            final_results = split_results(clean_results)
            extract_paper_info(titles, authors, final_results)
            print(len(titles))
            print(len(authors))
            print(len(links))
            print(titles)
    abstract_links, pdf_links = split_links(links)
    abstract = get_abstract(initiate_driver(), abstract_links)

    ugm_dictionary = {
        'Judul': titles,
        'Penulis': authors,
        'PDF_Link': pdf_links,
        'Abstrak': abstract
    }
    print(len(titles))
    print(len(authors))
    print(len(pdf_links))
    print(len(abstract))
    df = filefunctions.create_dataframe(ugm_dictionary)
    return df
