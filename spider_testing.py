from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
import re
import asyncio
import aiohttp
from playwright.async_api import async_playwright
import json
import httpx



class Async_spider_functions():

    def __init__(self):
        pass


    async def fetch_httpx_html(self, client, url):
        """
        Esta función se ejecuta asincrónicamente en cada URL proporcionada
        en la función `aiohttp_http()`. Utiliza httpx para obtener el HTML.
        """
        response = await client.get(url)
        return response.text, url

    async def httpx_http(self, urls):
        """
        Esta función devuelve una lista de archivos HTML guardados en una lista llamada 'titles',
        que se recuperan de manera asíncrona. Funciona solo si tenemos una lista de URLs.
        """
        async with httpx.AsyncClient() as client:
            # Crear las tareas asíncronas para cada URL
            tasks = [self.fetch_httpx_html(client, url) for url in urls]
            titles = await asyncio.gather(*tasks)

            title_data = []
            price_data = []
            url_data = []

            # Analiza el HTML y extrae los datos
            for html, url in titles:
                soup = BeautifulSoup(html, "lxml")
                data = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

                for p in data:
                    title = p.h3.a.text
                    price = p.find("p", class_="price_color").text

                    title_data.append(title)
                    price_data.append(price.strip())  # Limpiar el precio
                    url_data.append(url)

                    print(f"{title} | {price.strip()} | {url}")

            # Crear un DataFrame con los datos extraídos
            final_data = {
                "Title": title_data,
                "Price": price_data,
                "Url": url_data
            }

            df = pd.DataFrame(final_data)
            return df

            

    # Scrapping aqui-------------------














    async def get_cookies(self,url,adress_cookies,seconds,clean_cookies=None):
        """
        This function executes Javascript function in order to return hidden data usually from
        another webpage with Playwright in JSON format
        Parameters:
        url = The web page we want to get the cookies from
        seconds = The number of seconds we need to wait to finally get the cookies
        clean_cookies = If we want to clean the cookies we will mark True

        """
        self.seconds = seconds
        self.adress_cookies = adress_cookies
        if clean_cookies == True:

            self.url = url
        
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto(url)
                await asyncio.sleep(self.seconds)
                cookies_data = await context.cookies()
                clean_cookies = {cookie["name"] : cookie["value"] for cookie in cookies_data}
                with open(self.adress_cookies,"w") as j:
                    cookies = [json.dump(clean_cookies,j)]



        else:

            self.url = url
        
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto(url)
                await asyncio.sleep(self.seconds)
                cookies_data = await context.cookies()
                with open(self.adress_cookies,"w") as j:
                    cookies = json.dump(cookies_data,j)
            
               
        # asyncio.get_event_loop().run_until_complete(main())

        # return asyncio.run(self.javascript_multidata_extract())
        
    # def run_javascript_multidata_extract(self):
    #     """
    #     This function 
        
    #     """
    #     return asyncio.run(self.javascript_multidata_extract())
        
# urls = ['https://books.toscrape.com/', 'https://books.toscrape.com/catalogue/page-2.html', 'https://books.toscrape.com/catalogue/page-3.html', 'https://books.toscrape.com/catalogue/page-4.html', 'https://books.toscrape.com/catalogue/page-5.html', 'https://books.toscrape.com/catalogue/page-6.html', 'https://books.toscrape.com/catalogue/page-7.html', 'https://books.toscrape.com/catalogue/page-8.html', 'https://books.toscrape.com/catalogue/page-9.html', 'https://books.toscrape.com/catalogue/page-10.html', 'https://books.toscrape.com/catalogue/page-11.html', 'https://books.toscrape.com/catalogue/page-12.html', 'https://books.toscrape.com/catalogue/page-13.html', 'https://books.toscrape.com/catalogue/page-14.html', 'https://books.toscrape.com/catalogue/page-15.html', 'https://books.toscrape.com/catalogue/page-16.html', 'https://books.toscrape.com/catalogue/page-17.html', 'https://books.toscrape.com/catalogue/page-18.html', 'https://books.toscrape.com/catalogue/page-19.html', 'https://books.toscrape.com/catalogue/page-20.html', 'https://books.toscrape.com/catalogue/page-21.html', 'https://books.toscrape.com/catalogue/page-22.html', 'https://books.toscrape.com/catalogue/page-23.html', 'https://books.toscrape.com/catalogue/page-24.html', 'https://books.toscrape.com/catalogue/page-25.html', 'https://books.toscrape.com/catalogue/page-26.html', 'https://books.toscrape.com/catalogue/page-27.html', 'https://books.toscrape.com/catalogue/page-28.html', 'https://books.toscrape.com/catalogue/page-29.html', 'https://books.toscrape.com/catalogue/page-30.html', 'https://books.toscrape.com/catalogue/page-31.html', 'https://books.toscrape.com/catalogue/page-32.html', 'https://books.toscrape.com/catalogue/page-33.html', 'https://books.toscrape.com/catalogue/page-34.html', 'https://books.toscrape.com/catalogue/page-35.html', 'https://books.toscrape.com/catalogue/page-36.html', 'https://books.toscrape.com/catalogue/page-37.html', 'https://books.toscrape.com/catalogue/page-38.html', 'https://books.toscrape.com/catalogue/page-39.html', 'https://books.toscrape.com/catalogue/page-40.html', 'https://books.toscrape.com/catalogue/page-41.html', 'https://books.toscrape.com/catalogue/page-42.html', 'https://books.toscrape.com/catalogue/page-43.html', 'https://books.toscrape.com/catalogue/page-44.html', 'https://books.toscrape.com/catalogue/page-45.html', 'https://books.toscrape.com/catalogue/page-46.html', 'https://books.toscrape.com/catalogue/page-47.html', 'https://books.toscrape.com/catalogue/page-48.html', 'https://books.toscrape.com/catalogue/page-49.html',"https://books.toscrape.com/catalogue/page-50.html"]


# if __name__=="__main__":

#     spider = Async_spider_functions()
#     df = asyncio.run(spider.aiohttp_http(urls))
#     # spider.from_dataframe_to_data(df=df,extension="xlsx",adress=r"C:\Users\Cash\Proyectos\Web Scrapping\Veritas\outcome.xlsx")
#     print(df)


