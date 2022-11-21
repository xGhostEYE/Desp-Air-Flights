    soup=BeautifulSoup(driver.page_source, 'lxml')
    data = soup.find_all('div', attrs={'class': 'inner-grid keel-grid'})
    urls = []
    for link in soup.find_all('a', href=True):
        urls.append(link['href'])
    data_seperated = []
    print(urls)