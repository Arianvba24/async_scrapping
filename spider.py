from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
import re
import asyncio
import aiohttp
from playwright.async_api import async_playwright
import json
import httpx

def buscar_numero(text):
    # pass
    # return float(re.findall("[0-9]*,[0-9]*",text)[0].replace(",","."))
    if len(text) > 0:
        
        value = re.findall("[0-9]{1,2},[0-9]{1,2}",text)
        
        value1 = value[0].replace(",",".")
        return float(value1)
    else:

        return None



def buscar_segundo_numero(text):
    value = re.findall("[0-9]*,[0-9]*",text)
    if len(value) > 1:
        return float(value[1].replace(",","."))
    else:
        return float(value[0].replace(",","."))

class Async_spider_functions():

    def __init__(self):
        pass
    """
    VERITAS-------------------------------------
    
    """

    async def javascript_multidata_extract(self,url):
        """
        This function executes Javascript function in order to return hidden data usually from
        another webpage with Playwright in JSON format
        """
        self.url = url
       
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Cargar una página web
            await page.goto(url)

            # Hacer clic en el botón que ejecuta el script de JavaScript------------------------------
            # await page.evaluate("_ProductosFoodPortlet_WAR_comerzziaportletsfood_obtenerMasResultados();")
            while 1:

                await page.evaluate("_ProductosFoodPortlet_WAR_comerzziaportletsfood_obtenerMasResultados();")

                # Esperar a que se complete la ejecución del script (ajusta el tiempo según sea necesario)-----------------------
                await page.wait_for_timeout(800)  # Espera 5 segundos (ajusta el tiempo según sea necesario)
                html = await page.content()
                soup = BeautifulSoup(html, "lxml")
                try:

                    value = soup.find("div", class_="wrap-maspagina max-width-results")
                    if value.a.text == "Ver más resultados":
                        pass

                except:
                    print("except")
                    break
            html = await page.content()

            bs = BeautifulSoup(html,"lxml")
            soup = bs.find_all("div",class_="info-articulo")
            soup_images = bs.find_all("div",class_="imgwrap")
#         Loop straight to labels(a,h1,h2,div) or go to the class
#         Defining variables to create the dictionary and afeterwards the dataframe-----------
            title_value = []
            brand_value = []
            price_value = []
            price_kg_value = []
            image_value = []
            
            for i,text in enumerate(soup):
                title = text.find("p",class_="nombre").text
                brand = text.find("p",class_="marca").text
                
                price = buscar_segundo_numero(text.find("p",class_="precio").text)
                # print(text)
                price_kg = buscar_numero(text.find("div",class_="texto-porKilo").text)
                image = soup_images[i].img.attrs["src"]
    #             Stablishing dictionary's values for Dataframe-------------------------------
                title_value.append(title)
                brand_value.append(brand)
                price_value.append(price)
                price_kg_value.append(price_kg)
                if "comerzzia" in image:
                    image_value.append("No image available")
                else:
                    image_value.append(image)

            # image_value = list(filter(lambda x: "comerzzia" not in x,image_value1))
            print(image_value)
            print(len(image_value))
            print(len(title_value))
                # print(image)
                # break
                # image_value.append(image.img.attrs["src"])
                # print(title_value)
    #         Creating Pandas Dataframe
            await browser.close()
            data = {
                
                "Title" : title_value,
                "Brand" : brand_value,
                "Price" : price_value,
                "Price_kg" : price_kg_value,
                "Image" : image_value
                
            }

            df = pd.DataFrame(data)
            
            return df

    """
    ADIDAS FIRST SCRAPPING-------------------------------------
    
    """
    async def open_browser(self,url):

        """
        This function opens a browsers with Playwright library and goes throught every link in the web page in order to extract the data from every page.
        This function uses two other async functions in order to extract the data.
        These two functions are get_data() y get_link()
        The function returns a Dataframe
        """
        self.url = url
        self.title = []
        self.price = []
        self.category = []
        self.product_id = []
        async with async_playwright() as p:
            browser =  await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.wait_for_timeout(2000)
            
            await page.goto(self.url)
            # await page.get_by_text("open new tab").click()
            
            content = await page.content()
            
            # Cambio---------------------------------------
            await page.wait_for_selector('.gl-cta.gl-cta--primary.gl-cta--full-width._text-wrap_1xzpo_29')
            await page.click('.gl-cta.gl-cta--primary.gl-cta--full-width._text-wrap_1xzpo_29')

            # await asyncio.sleep(1)

            while 1:


                task1 = asyncio.create_task(self.get_data(content))
                task2 = await asyncio.create_task(self.get_link(content))

                if task2[1] == None:

        
        
                    print("Exiting loop....")
                    await asyncio.sleep(1)
                    break
                else:

                    await page.goto(f"https://www.adidas.es/{task2[1]}")
                    content = await page.content()


        data = {

        "Title" : self.title,
        # "Price" : price,
        "Category" : self.category,
        "Product_id" : self.product_id



        }
        
        df = pd.DataFrame(data)

        return df

        



    # Cambio---------------------------------------
    async def get_data(self,html_data_source):
        """
        DO NOT USE ALONE------------------

        This function is executed in consequence of using open_browser()

        This functions is managed to extract the html code from every page


        
        
        """
        html_value = BeautifulSoup(html_data_source,"lxml")
        soup = html_value.find_all("div",class_="grid-item")
        for i in soup:
    
            try:

                title_value = i.find("p",class_="glass-product-card__title").text
                category_value = i.find("p",class_="glass-product-card__category").text
                product_id_value = i.attrs["data-grid-id"]
                # price_value = i.find("div",class_="gl-price-item notranslate").text
                self.title.append(title_value)
                # price.append(price_value)
                self.category.append(category_value)
                self.product_id.append(product_id_value)
                print(f"{title_value} | {category_value} | {product_id_value}")

            except:
                pass

    async def get_link(self,html_data_source):
        """
        DO NOT USE ALONE------------------

        This function is executed in consequence of using open_browser()

        This functions is managed to extract the links of the next pages from every page

        """
        html_value = BeautifulSoup(html_data_source,"lxml")
        soup = html_value.find("div",class_="pagination__control___3C268 pagination__control--next___329Qo pagination_margin--next___3H3Zd")
        try:
            print(soup)

            if soup.a.text == "Siguiente":
                return "next",soup.a["href"]
            else:
                return None,None
        except:

            return None,None

    # def create_async_dataframe(self,title,category,product_id):

    #     data = {

    #     "Title" : title,
    #     # "Price" : price,
    #     "Category" : category,
    #     "Product_id" : product_id



    #     }
        
    #     df = pd.DataFrame(data)

    #     return df
    
    """
    ADIDAS SECOND SCRAPPING-------------------------------------
    
    """

    async def open_and_download_multiple_browser(self,context, url):
        """
        DO NOT USE ALONE-------------------

        This function works with loop_browser()
        This function is managed to fetch the content of every tab tab openend
        
        """
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_timeout(1300)
        content = await page.content()
        await page.close()
        
        return content

    async def loop_browser(self,urls):
        """
        This function opens a browser and asynchronly opens multiple pages inheriting 'context' created object and executes the function
        open_and_download_multiple_browser().
        It returns a list with all the json/html content of every page opened
        
        """
        self.urls = urls
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            tasks = [self.open_and_download_multiple_browser(context, url) for url in self.urls]
            contents = await asyncio.gather(*tasks)
            await browser.close()
            return contents



    def find_data(self,data):
        """
        This function cleans the data of every content extracted from the loop_browser() function.
        In this case we cut parts of the data in order to create a JSON file
        """
        
        self.data = data
        # print(self.data)
        try:

            data1 = re.findall('{"_links":[\S\s]*</pre></body></html>',self.data)
            data2 = data1[0].replace("</pre></body></html>","")
            values = json.loads(data2)
            # print(values)
            return values

        except:
            return {"name" : "Producto quitado","brand" : "Producto quitado","category" : "Producto quitado","color" : "Producto quitado","modelId" : "Producto quitado","salePrice":"Producto quitado","link":"Producto quitado"}

    def final_process(self):
        """
        This is the final function managed to due to term all the previous functions.
        Reads the excel file with all the IDs of every product.
        Creates a list of urls combined with the data fetched from the previous excel file
        Pops only a part of the urls and creates a loop using the async function loop_browser() throught all the popped urls
        Loops throught the list of json/html data returned from the loop_browser() function and appends the data to the variables defined at the beginning
        Continues the process until it's over
        Created and modifies the Dataframe
        Returns finally the Dataframe
        
        
        
        """
        df_1 = pd.read_excel(r"C:\Users\Cash\Proyectos\Web Scrapping\Template\Adidas2.xlsx")
        api_values = [f"https://www.adidas.es/api/search/product/{x}" for x in list(df_1["Product_id"].values)]

        urls = api_values

        name = []
        brand = []
        category = []
        color = []
        modelID = []
        saleprice = []
        link = []

        data_json = {
            
            "Name" : name,
            "Brand" : brand,
            "Category" : category,
            "Color" : color,
            "Model ID" : modelID,
            "Price" : saleprice,
            "Link" : link
            
        }
        while 1:
            print(f"Remaining products: {len(api_values)}")

            if len(api_values) >= 80:
                urls = [api_values.pop() for i in range(80)]
                values_data = [self.find_data(value) for value in asyncio.run(self.loop_browser(urls))]
                # print(values_data)
                for i in values_data:
                    name.append(i["name"])
                    brand.append(i["brand"])
                    category.append(i["category"])
                    color.append(i["color"])
                    modelID.append(i["modelId"])
                    saleprice.append(i["salePrice"])
                    link.append(f'https://www.adidas.es{i["link"]}')

                del urls
            elif len(api_values) < 80 and len(api_values) > 0:
                urls = [api_values.pop() for i in range(len(api_values))]
                values_data = [self.find_data(value) for value in asyncio.run(self.loop_browser(urls))]
                for i in values_data:
                    name.append(i["name"])
                    brand.append(i["brand"])
                    category.append(i["category"])
                    color.append(i["color"])
                    modelID.append(i["modelId"])
                    saleprice.append(i["salePrice"])
                    link.append(f'https://www.adidas.es{i["link"]}')
            
                del urls
            
            elif len(api_values) == 0:
                print("Acabado")
                break
            else:
                print("Acabado")
                break

        df = pd.DataFrame(data_json)
        rows_remove = df.loc[df["Name"]=="Producto quitado"].index
        df.drop(rows_remove,inplace=True)

        return df


    # Scrapping aqui-------------------

    async def fetch_html(self,session,url):
        #We can use await to extract the data and the url
        """
        DO NOT USE THIS FUNCTION ALONE-----------------------
        This function is execute asynchronly in every url provided in the aiohttp_http() function

        
        """
        value = await session.get(url)
        return await value.text(),url

        #Or we can use async with rename the object and get the result we want

        # async with session.get(url) as resp:
        #     return await resp.text(),url


    async def aiohttp_http(self,urls):
        """
        This function returns a list of html files saved in a list called 'titles' that are fetched asynchronesly.
        It works only if we have the list of urls.


        
        """
        async with aiohttp.ClientSession() as client:
            tasks = [self.fetch_html(client,url) for url in urls]
            titles = await asyncio.gather(*tasks)
            
            title_data = []
            price_data = []
            url_data = []

            for i,url in titles:
                soup = BeautifulSoup(i,"lxml")
                data = soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
                for p in data:
                    title = p.h3.a.text
                    price = p.find("p",class_="price_color").text

                    title_data.append(title)
                    price_data.append(price)
                    url_data.append(url)
                    print(f"{title} | {price.strip()} | {url}")

            final_data = {

                "Title" : title_data,
                "Price" : price_data,
                "Url" : url_data

            }


            df = pd.DataFrame(final_data)

            return df


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
            tasks = [self.fetch_html(client, url) for url in urls]
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
        
urls = ['https://books.toscrape.com/', 'https://books.toscrape.com/catalogue/page-2.html', 'https://books.toscrape.com/catalogue/page-3.html', 'https://books.toscrape.com/catalogue/page-4.html', 'https://books.toscrape.com/catalogue/page-5.html', 'https://books.toscrape.com/catalogue/page-6.html', 'https://books.toscrape.com/catalogue/page-7.html', 'https://books.toscrape.com/catalogue/page-8.html', 'https://books.toscrape.com/catalogue/page-9.html', 'https://books.toscrape.com/catalogue/page-10.html', 'https://books.toscrape.com/catalogue/page-11.html', 'https://books.toscrape.com/catalogue/page-12.html', 'https://books.toscrape.com/catalogue/page-13.html', 'https://books.toscrape.com/catalogue/page-14.html', 'https://books.toscrape.com/catalogue/page-15.html', 'https://books.toscrape.com/catalogue/page-16.html', 'https://books.toscrape.com/catalogue/page-17.html', 'https://books.toscrape.com/catalogue/page-18.html', 'https://books.toscrape.com/catalogue/page-19.html', 'https://books.toscrape.com/catalogue/page-20.html', 'https://books.toscrape.com/catalogue/page-21.html', 'https://books.toscrape.com/catalogue/page-22.html', 'https://books.toscrape.com/catalogue/page-23.html', 'https://books.toscrape.com/catalogue/page-24.html', 'https://books.toscrape.com/catalogue/page-25.html', 'https://books.toscrape.com/catalogue/page-26.html', 'https://books.toscrape.com/catalogue/page-27.html', 'https://books.toscrape.com/catalogue/page-28.html', 'https://books.toscrape.com/catalogue/page-29.html', 'https://books.toscrape.com/catalogue/page-30.html', 'https://books.toscrape.com/catalogue/page-31.html', 'https://books.toscrape.com/catalogue/page-32.html', 'https://books.toscrape.com/catalogue/page-33.html', 'https://books.toscrape.com/catalogue/page-34.html', 'https://books.toscrape.com/catalogue/page-35.html', 'https://books.toscrape.com/catalogue/page-36.html', 'https://books.toscrape.com/catalogue/page-37.html', 'https://books.toscrape.com/catalogue/page-38.html', 'https://books.toscrape.com/catalogue/page-39.html', 'https://books.toscrape.com/catalogue/page-40.html', 'https://books.toscrape.com/catalogue/page-41.html', 'https://books.toscrape.com/catalogue/page-42.html', 'https://books.toscrape.com/catalogue/page-43.html', 'https://books.toscrape.com/catalogue/page-44.html', 'https://books.toscrape.com/catalogue/page-45.html', 'https://books.toscrape.com/catalogue/page-46.html', 'https://books.toscrape.com/catalogue/page-47.html', 'https://books.toscrape.com/catalogue/page-48.html', 'https://books.toscrape.com/catalogue/page-49.html',"https://books.toscrape.com/catalogue/page-50.html"]


# if __name__=="__main__":

#     spider = Async_spider_functions()
#     df = asyncio.run(spider.aiohttp_http(urls))
#     # spider.from_dataframe_to_data(df=df,extension="xlsx",adress=r"C:\Users\Cash\Proyectos\Web Scrapping\Veritas\outcome.xlsx")
#     print(df)


