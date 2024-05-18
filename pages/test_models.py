import streamlit as st
import os
from ultralytics import YOLO
import str_task4

st.set_page_config(layout='wide', page_title='Алабуга - 4')
st.header('Тест обученных моделей')
test_dir = 'data.yaml'
col1, col2, col3 = st.columns(3)
model1 = col1.selectbox(
    'Выберите модель 1',
    os.listdir(str_task4.cl_mod),
    index=None,
    format_func=lambda s: s.upper())

model2 = col2.selectbox(
    'Выберите модель 2',
    os.listdir(str_task4.cl_mod),
    index=None,
    format_func=lambda s: s.upper())

model3 = col3.selectbox(
    'Выберите модель 3',
    os.listdir(str_task4.cl_mod),
    index=None,
    format_func=lambda s: s.upper())
# print(model1)
col1, col2, col3 = st.columns(3)



def print_mod(col, model):
    model_1 = YOLO(str_task4.cl_mod+'/'+model)
    result = model_1.val(data=test_dir,imgsz=640,batch=16,conf=0.1,iou=0.6,device='cpu',save=False)
    col.subheader(model)
    col.write('Fitness')
    col.write(result.fitness)
    k = result.mean_results()
    col.write('Pressision')
    col.write(k[0])
    col.write('Recall')
    col.write(k[1])
    col.write('mAp 50')
    col.write(k[2])
    col.write('mAp')
    col.write(k[3])
    # print(result)
    result.confusion_matrix.plot(normalize=False, save_dir='img_input', names=(), on_plot=None)
    col.write('Confusion matrix')
    col.image('img_input/confusion_matrix.png')

if model1!=None:
    print_mod(col1, model1)
if model2!=None:
    print_mod(col2, model2)
if model3!=None:
    print_mod(col3, model3)



