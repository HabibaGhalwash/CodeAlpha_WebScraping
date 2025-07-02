import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target website
url = "http://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Scrape titles and prices
books = soup.find_all("article", class_="product_pod")
titles = [book.h3.a["title"] for book in books]
prices = [book.find("p", class_="price_color").text[2:] for book in books]

# Create DataFrame and save to CSV
df = pd.DataFrame({"Title": titles, "Price": prices})
df.to_csv("scraped_books.csv", index=False)

print("✅ Scraped", len(df), "books.")
