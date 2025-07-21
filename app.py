import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Dictionary of product categories with corresponding URLs
categories = {
    "Mobiles": "https://priceoye.pk/mobiles?page=",
    "Wireless Earbuds": "https://priceoye.pk/wireless-earbuds?page=",
    "Smart Watches": "https://priceoye.pk/smart-watches?page=",
    "Trimmers & Shavers": "https://priceoye.pk/trimmers-shaver?page=",
    "Power Banks": "https://priceoye.pk/power-banks?page=",
    "Mobile Chargers": "https://priceoye.pk/mobile-chargers?page=",
    "Bluetooth Speakers": "https://priceoye.pk/bluetooth-speakers?page=",
    "Tablets": "https://priceoye.pk/tablets?page=",
    "Laptops": "https://priceoye.pk/laptops?page="
}

# Function to scrape data from PriceOye
def scrape_data(url, pages):
    products = []
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://google.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
    }
    for page in range(pages):
        full_url = f"{url}{page+1}"
        response = session.get(full_url, headers=headers, timeout=10)
        html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")

        for i in soup.find_all("div", class_="productBox b-productBox"):
            # Find the first <a> tag for the product link
            a_tag = i.find("a", href=True)
            link = a_tag["href"] if a_tag else None
            # Find product name
            name_tag = i.find("div", class_="p-title")
            name = name_tag.get_text(strip=True) if name_tag else None
            # Find discounted price
            price_tag = i.find("div", class_="price-box")
            discounted_price = price_tag.get_text(strip=True) if price_tag else None
            # Find original price and discount percent if available
            original_price = None
            discount_percent = None
            price_diff = i.find("div", class_="price-diff")
            if price_diff:
                original_tag = price_diff.find("div", class_="price-diff-retail")
                discount_tag = price_diff.find("div", class_="price-diff-saving")
                original_price = original_tag.get_text(strip=True) if original_tag else None
                discount_percent = discount_tag.get_text(strip=True) if discount_tag else None

            context = {
                "Name": name,
                "Discounted Price": discounted_price,
                "Original Price": original_price,
                "Discount Percent": discount_percent,
                "Product Link": link if link and link.startswith("http") else ("https://priceoye.pk" + link if link else None)
            }

            products.append(context)

    return products

# Streamlit UI
st.title("PriceOye Product Data Scraper By Muhammad Abrar")

# Select category from the dropdown
category = st.selectbox("Select Product Category", list(categories.keys()))

# Input number of pages to scrape
pages = st.number_input("Enter number of pages to scrape:", min_value=1, max_value=100, value=1)

# Scrape button
if st.button("Scrape Data"):
    st.write(f"Scraping {pages} pages of {category} data from PriceOye...")
    show_link=categories[category].split("?")
    st.write(f"Your can confirm scraping data form the following link\n{show_link[0]}")
    url = categories[category]
    data = scrape_data(url, pages)

    if data:
        # Display heading and DataFrame
        st.header(f"{pages} Pages of {category} Data from PriceOye")
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.warning("No data found, please try again later.")