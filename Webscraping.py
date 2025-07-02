import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target website
url = "http://books.toscrape.com/"

# Send HTTP request
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status
    print("🔗 Connected to", url)
except requests.exceptions.RequestException as e:
    print("❌ Error connecting:", e)
    exit()

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Extract book data
books = soup.find_all("article", class_="product_pod")

titles = []
prices = []
availability = []
ratings = []

for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text.strip()[1:]  # remove £
    stock = book.find("p", class_="instock availability").text.strip()
    rating = book.p.get("class")[1]  # class = ["star-rating", "Three"], get "Three"

    titles.append(title)
    prices.append(price)
    availability.append(stock)
    ratings.append(rating)

# Create DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Price (GBP)": prices,
    "Availability": availability,
    "Rating": ratings
})

# Save to CSV
df.to_csv("scraped_books.csv", index=False)

print(f"✅ Scraped {len(df)} books and saved to 'scraped_books.csv'")

