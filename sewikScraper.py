from sewikToDict import sewikToDict
from bs4 import BeautifulSoup

def sewikScraper(html_file_path):
    try:
        with open(html_file_path, 'r', encoding='utf-8') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')

            accident_links = soup.find_all('a', href=lambda href: href and '/accident/' in href)

            scraped_accidents = []

            for link in accident_links:
                link_href = link['href']
                accident_id = link_href.split('/')[-1]
                data = sewikToDict("https://sewik.pl/accident/"+accident_id)
                if data is not None:
                    scraped_accidents.append(data)

            return scraped_accidents

    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {html_file_path}")
    except Exception as e:
        print(f"Inny błąd: {e}")