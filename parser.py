import requests
from bs4 import BeautifulSoup
import json


def scrape_quotes():
    base_url = "http://quotes.toscrape.com"
    next_page = "/"
    quotes_data = []
    authors_data = {}
    
    while next_page:
        response = requests.get(base_url + next_page)
        if response.status_code != 200:
            print(f"Failed to fetch {base_url + next_page}")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Збираємо цитати
        quotes = soup.select(".quote")
        for quote in quotes:
            text = quote.select_one(".text").get_text(strip=True)
            author_name = quote.select_one(".author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.select(".tags .tag")]
            
            quotes_data.append({
                "quote": text,
                "author": author_name,
                "tags": tags
            })
            
            # Отримуємо детальну інформацію про автора, якщо вона ще не зібрана
            if author_name not in authors_data:
                author_url = quote.select_one("span a")["href"]
                author_details = scrape_author_details(base_url + author_url)
                authors_data[author_name] = author_details

        # Переходимо на наступну сторінку
        next_button = soup.select_one(".next a")
        next_page = next_button["href"] if next_button else None
    
    # Записуємо результати в файли JSON
    save_to_json(r"D:\GOIT_SoftEng\Module9\HW\quotes.json", quotes_data)
    save_to_json(r"D:\GOIT_SoftEng\Module9\HW\authors.json", list(authors_data.values()))


def scrape_author_details(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return {}
    
    soup = BeautifulSoup(response.text, "html.parser")
    fullname = soup.select_one(".author-title").get_text(strip=True)
    born_date = soup.select_one(".author-born-date").get_text(strip=True)
    born_location = soup.select_one(".author-born-location").get_text(strip=True)
    description = soup.select_one(".author-description").get_text(strip=True)
    
    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }


def save_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    scrape_quotes()
