import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
def get_user_input():
    url = input("Enter the URL to scrape:").strip()
    data_type = input("Enter the type of data to scrape: ").strip()
    pages = int(input("Enter the number of pages to scrape: "))
    return url, data_type, pages
def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
def parse_html(content, data_type):
    soup = BeautifulSoup(content, 'html.parser')
    data = []
    if data_type.lower() == "headlines":
        data = [headline.get_text().strip() for headline in soup.find_all('a', class_='titlelink')]  
    elif data_type.lower() == "product details":
        data = [product.get_text().strip() for product in soup.find_all(class_='product-title')] 
    elif data_type.lower() == "job listings":
        data = [job.get_text().strip() for job in soup.find_all(class_='job-title')] 
    return data
def handle_pagination(base_url, pages, data_type):
    all_data = []
    for page in range(1, pages + 1):
        paginated_url = f"{base_url}?p={page}"
        print(f"Scraping page: {paginated_url}")
        content = fetch_page_content(paginated_url)
        if content:
            page_data = parse_html(content, data_type)
            all_data.extend(page_data)
    return all_data
def save_to_csv(data, filename="scrap_data.csv"):
    df = pd.DataFrame(data, columns=["Data"])
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
def save_to_database(data, db_name="scraped_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Scrap (id INTEGER , data TEXT)")
    cursor.executemany("INSERT INTO Scrap (data) VALUES (?)", [(d,) for d in data])
    conn.commit()
    conn.close()
    print(f"Data saved to {db_name}")
def main():
    url, data_type, pages = get_user_input()
    data = handle_pagination(url, pages, data_type)
    if data:
        print(f"Scraped {len(data)} items.")
        save_option = input("Save to (1) CSV or (2) Database? Enter 1 or 2: ").strip()
        if save_option == "1":
            save_to_csv(data)
        elif save_option == "2":
            save_to_database(data)
        else:
            print("Invalid option. Exiting without saving.")
    else:
        print("No data scraped.")
if __name__ == "__main__":
    main()
