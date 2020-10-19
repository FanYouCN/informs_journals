import requests
from bs4 import BeautifulSoup
import os

class papercrawler:
    def __init__(self):
        urls = ['https://pubsonline.informs.org/toc/opre/0/0',
                'https://pubsonline.informs.org/toc/mnsc/0/0',
                'https://pubsonline.informs.org/toc/msom/0/0',
                'https://pubsonline.informs.org/toc/opre/current',
                'https://pubsonline.informs.org/toc/mnsc/current',
                'https://pubsonline.informs.org/toc/msom/current']

        self.list_of_url_lists = []

        for url in urls:
            responselist = requests.get(url)
            soup = BeautifulSoup(responselist.text, 'html.parser')
            pdf_url_list = []
            for link in soup.find_all('a'):
                _url = link.get('href')
                if _url is not None and 'doi/pdf' in _url:
                    pdf_url_list.append('https://pubsonline.informs.org'+_url)
            self.list_of_url_lists.append(pdf_url_list)



    def download(self):
        for url_list in self.list_of_url_lists:
            for paper in url_list:
                for i in range(len(paper)):
                    if paper[i:i+4] == 'opre':
                        title = paper[i:]
                        break
                    elif paper[i:i+4] == 'mnsc':
                        title = paper[i:]
                        break
                    elif paper[i:i+4] == 'msom':
                        title = paper[i:]
                        break
                title = title.replace('.', '_') + '.pdf'
                if 'opre' in title:
                    paper_dir = '~/Dropbox/INFORMS_Papers/OR/' + title
                elif 'mnsc' in title:
                    paper_dir = '~/Dropbox/INFORMS_Papers/MS/' + title
                elif 'msom' in title:
                    paper_dir = '~/Dropbox/INFORMS_Papers/MSOM/' + title
                paper_dir = os.path.expanduser(paper_dir)
                if not os.path.exists(paper_dir):
                    print(title, 'Downloading...')
                    responsepage = requests.get(paper)
                    with open(paper_dir, 'wb') as f:
                        f.write(responsepage.content)
                else:
                    print(title, 'Downloaded')


if __name__ == '__main__':
    crawler = papercrawler()
    crawler.download()