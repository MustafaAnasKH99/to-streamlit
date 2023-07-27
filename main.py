import streamlit as st
import streamlit.components.v1 as com
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from supabase import create_client

css = '''
<style>
*{
font-family: "Source Sans Pro", sans-serif;
}
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}

tr:nth-child(odd) {
  background-color: #9aeb8f;
}
.red-line{
    color: #9aeb8f;
}
</style>
'''

supa_url = 'https://qppfxrvobiivsmmgounc.supabase.co'
supabase = create_client(supa_url, st.secrets['api'])

st.set_page_config(
    page_title="Milton Electrical App",
)

st.title("Milton Auto Electric App ⚡")
st.sidebar.success("Home page")

response = supabase.table('agricultural').select("*").execute()
data_len = len(response.data)
data_len_str = "<p>There are <b>" + str(data_len) + "</b> items in this database from Agricultural Category - DB Electrical</p>"
st.markdown(data_len_str, unsafe_allow_html=True)
skip = 0
for row in response.data:
    if skip < 1:
      skip += 1
      continue
    html_string = ""
    # split images
    images_arr = row['images'].split(" ")
    with st.expander(str(row['title'])):
        # title_str = "<h1 style=\"color:white;\">" + row['title'] + "</h1>"
        price_str = "<h2 style=\"color:white;\">" + "Price: " + row['price'] + "</h2>"
        new_specs = str(row['specs']).replace('Critical Note', '')
        styled_specs = css + new_specs
        html_string += price_str
        html_string += styled_specs
        # com.html(str(row['specs']))
        # st.write(str(row['specs']))
        images_html= ""
        images_title = "<h2 style=\"color:#9aeb8f;\">" + "PRODUCT IMAGES" + "</h2>"
        html_string += images_title
        for image in images_arr:
            with st.container():
                print(image)
                img_src = "<a href=\""+image+"\"><img src=\"" + image + "\" width=\"300px\"; /></a>"
                images_html += img_src
                html_string += images_html
        com.html(html_string, scrolling=True)
