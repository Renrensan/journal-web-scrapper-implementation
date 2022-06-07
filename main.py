import ugm_scrapper as ugm
import researchgate_scrapper as rsg
import filefunctions

keywords_list = ['sosiologi', 'labor', 'digital', 'budaya', 'sosiologi', 'korupsi', 'demokrasi', 'ilmu', 'prabowo', 'ahok', 'jokowi', 'politik', 'megawati', 'anies', 'sosial', 'ekonomi', 'dinamika', 'demokrasi']
# keywords_list = ['politik']


# Scrape for JurnalSosPol UGM web
def ugm_scrape(keywords):
    ugm_df = ugm.run_ugm(keywords)
    print(ugm_df.head())
    print(ugm_df.tail())
    return filefunctions.create_tsv(ugm_df, filename='ugm_results_test_3.tsv')


def rsg_scrape(keywords):
    rsg_df = rsg.run_rsg(keywords)
    print(rsg_df.head())
    print(rsg_df.tail())


# run the code
ugm_scrape(keywords_list)
# rsg_scrape(keywords_list)


# testing
# ugm_df = ugm.run_ugm(keywords_list)
# print(ugm_df.head())
# print(ugm_df.tail())
