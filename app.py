import streamlit as st
from spider import *
import nest_asyncio

nest_asyncio.apply()

urls = ['https://books.toscrape.com/', 'https://books.toscrape.com/catalogue/page-2.html', 'https://books.toscrape.com/catalogue/page-3.html', 'https://books.toscrape.com/catalogue/page-4.html', 'https://books.toscrape.com/catalogue/page-5.html', 'https://books.toscrape.com/catalogue/page-6.html', 'https://books.toscrape.com/catalogue/page-7.html', 'https://books.toscrape.com/catalogue/page-8.html', 'https://books.toscrape.com/catalogue/page-9.html', 'https://books.toscrape.com/catalogue/page-10.html', 'https://books.toscrape.com/catalogue/page-11.html', 'https://books.toscrape.com/catalogue/page-12.html', 'https://books.toscrape.com/catalogue/page-13.html', 'https://books.toscrape.com/catalogue/page-14.html', 'https://books.toscrape.com/catalogue/page-15.html', 'https://books.toscrape.com/catalogue/page-16.html', 'https://books.toscrape.com/catalogue/page-17.html', 'https://books.toscrape.com/catalogue/page-18.html', 'https://books.toscrape.com/catalogue/page-19.html', 'https://books.toscrape.com/catalogue/page-20.html', 'https://books.toscrape.com/catalogue/page-21.html', 'https://books.toscrape.com/catalogue/page-22.html', 'https://books.toscrape.com/catalogue/page-23.html', 'https://books.toscrape.com/catalogue/page-24.html', 'https://books.toscrape.com/catalogue/page-25.html', 'https://books.toscrape.com/catalogue/page-26.html', 'https://books.toscrape.com/catalogue/page-27.html', 'https://books.toscrape.com/catalogue/page-28.html', 'https://books.toscrape.com/catalogue/page-29.html', 'https://books.toscrape.com/catalogue/page-30.html', 'https://books.toscrape.com/catalogue/page-31.html', 'https://books.toscrape.com/catalogue/page-32.html', 'https://books.toscrape.com/catalogue/page-33.html', 'https://books.toscrape.com/catalogue/page-34.html', 'https://books.toscrape.com/catalogue/page-35.html', 'https://books.toscrape.com/catalogue/page-36.html', 'https://books.toscrape.com/catalogue/page-37.html', 'https://books.toscrape.com/catalogue/page-38.html', 'https://books.toscrape.com/catalogue/page-39.html', 'https://books.toscrape.com/catalogue/page-40.html', 'https://books.toscrape.com/catalogue/page-41.html', 'https://books.toscrape.com/catalogue/page-42.html', 'https://books.toscrape.com/catalogue/page-43.html', 'https://books.toscrape.com/catalogue/page-44.html', 'https://books.toscrape.com/catalogue/page-45.html', 'https://books.toscrape.com/catalogue/page-46.html', 'https://books.toscrape.com/catalogue/page-47.html', 'https://books.toscrape.com/catalogue/page-48.html', 'https://books.toscrape.com/catalogue/page-49.html',"https://books.toscrape.com/catalogue/page-50.html"]


def extract_data():
    spider = Async_spider_functions()
    df = asyncio.run(spider.httpx_http(urls))
    return df








def main():
    st.title("Hola mundo")
    value = st.button("Click me to scrape")
    if value:
        st.dataframe(extract_data())















if __name__=="__main__":
    main()