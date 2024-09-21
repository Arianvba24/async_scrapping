import nest_asyncio
import asyncio
import aiohttp
import streamlit as st

# Habilitar bucles de eventos anidados
nest_asyncio.apply()

# Función asincrónica para realizar la solicitud
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Ejecutar la función asincrónica en Streamlit
async def run_fetch_data(url):
    return await fetch_data(url)

st.title("Ejemplo con aiohttp y nest_asyncio")

url = "https://jsonplaceholder.typicode.com/todos/1"

# Ejecutar el bucle asincrónico
loop = asyncio.get_event_loop()
result = loop.run_until_complete(run_fetch_data(url))

st.write(result)
