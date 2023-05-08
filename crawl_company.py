import requests
from bs4 import BeautifulSoup

def wiki_info(company):
    try:
        url = "https://en.wikipedia.org/wiki/" + company
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find('span', attrs = {'class':'mw-page-title-main'})
        table = soup.find('table', attrs = {'class':'infobox vcard'})
        company_info = {'Company Name':title.text, 'Number of employees':None, 'sub':None, 'parent':None}
        for row in table.findAll('tr'):
            if row.find('th') != None:
                if row.find('th').text == 'Number of employees':
                    company_info['Number of employees'] = row.find('td').text
                elif row.find('th').text == 'Subsidiaries':
                    company = []
                    for sub in row.findAll('a'):
                        company.append(sub.text)
                    company_info['sub'] = company[1:]
                elif row.find('th').text == 'Parent':  
                    company_info['parent'] = row.find('td').text
        return company_info
    except:
        return None