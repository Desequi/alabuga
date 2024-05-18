import streamlit as st
import os

st.set_page_config(layout='wide', page_title='Алабуга - 4')
st.header('Обнаружение на изображениях с камеры')

if st.button("Запуск видеокамеры"):
    os.system("cam.py")
