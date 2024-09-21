import streamlit as st
import aiohttp
import asyncio


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            result = await response.json()
            return result
    except Exception:
        return {}


async def main():
    st.set_page_config(page_title="Example App", page_icon="🤖")
    st.title("Get Image by Id")
    async with aiohttp.ClientSession() as session:
        with st.form("my_form"):
            index = st.number_input("ID", min_value=0, max_value=100, key="index")

            submitted = st.form_submit_button("Submit")

            if submitted:
                st.write("Result")
                data = await fetch(session, f"https://picsum.photos/id/{index}/info")
                if data:
                    st.image(data['download_url'], caption=f"Author: {data['author']}")
                else:
                    st.error("Error")


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
