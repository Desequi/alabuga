import streamlit as st
import os
import time
from ultralytics import YOLO
import str_task4

st.set_page_config(layout='wide', page_title='Алабуга - 4')
st.header('Тест обученных моделей')
st.write('Сравнивались различные модели, обученные на аугментированных исходных данных - 414 изображениях.'
         'лучше всего по характеристикам показали себя yolov5n(30n5-cars.pt) и yolov8n(30n-cars_01.pt).')
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
col = []
col = st.columns(8)
col[0].write('Name')
col[1].write('Fitness')
col[2].write('Pressision')
col[3].write('Recall')
col[4].write('mAp 50')
col[5].write('mAp')
col[6].write('Время выполнения, сек')
col[7].write('Confusion matrix')

@st.cache_data
def print_mod1(model):
    col = st.columns(8)
    start_time = time.time()
    model_1 = YOLO(str_task4.cl_mod+'/'+model)
    result = model_1.val(data=test_dir, imgsz=640, batch=16, conf=0.1, iou=0.6, device='cpu', save=False)
    col[0].write(model)
    col[1].write(round(result.fitness, 6))
    k = result.mean_results()
    col[2].write(round(k[0], 6))
    col[3].write(round(k[1], 6))
    col[4].write(round(k[2], 6))
    col[5].write(round(k[3], 6))
    result.confusion_matrix.plot(normalize=False, save_dir='img_input', names=(), on_plot=None)
    col[6].write(round(time.time() - start_time, 6))
    col[7].image('img_input/confusion_matrix.png')

@st.cache_data
def print_mod2(model):
    col = st.columns(8)
    start_time = time.time()
    model_1 = YOLO(str_task4.cl_mod+'/'+model)
    result = model_1.val(data=test_dir, imgsz=640, batch=16, conf=0.1, iou=0.6, device='cpu', save=False)
    col[0].write(model)
    col[1].write(round(result.fitness, 6))
    k = result.mean_results()
    col[2].write(round(k[0], 6))
    col[3].write(round(k[1], 6))
    col[4].write(round(k[2], 6))
    col[5].write(round(k[3], 6))
    result.confusion_matrix.plot(normalize=False, save_dir='img_input', names=(), on_plot=None)
    col[6].write(round(time.time() - start_time, 6))
    col[7].image('img_input/confusion_matrix.png')

@st.cache_data
def print_mod3(model):
    col = st.columns(8)
    start_time = time.time()
    model_1 = YOLO(str_task4.cl_mod+'/'+model)
    result = model_1.val(data=test_dir, imgsz=640, batch=16, conf=0.1, iou=0.6, device='cpu', save=False)
    col[0].write(model)
    col[1].write(round(result.fitness, 6))
    k = result.mean_results()
    col[2].write(round(k[0], 6))
    col[3].write(round(k[1],6))
    col[4].write(round(k[2],6))
    col[5].write(round(k[3],6))
    result.confusion_matrix.plot(normalize=False, save_dir='img_input', names=(), on_plot=None)
    col[6].write(round(time.time() - start_time,6))
    col[7].image('img_input/confusion_matrix.png')

if model1!=None:
    print_mod1( model1)
if model2!=None:
    print_mod2( model2)
if model3!=None:
    print_mod3( model3)

# def print_mod(col, model):
#     start_time = time.time()
#     model_1 = YOLO(str_task4.cl_mod+'/'+model)
#     result = model_1.val(data=test_dir,imgsz=640,batch=16,conf=0.1,iou=0.6,device='cpu',save=False)
#     col.subheader(model)
#     col.write('Fitness')
#     col.write(result.fitness)
#     k = result.mean_results()
#     col.write('Pressision')
#     col.write(k[0])
#     col.write('Recall')
#     col.write(k[1])
#     col.write('mAp 50')
#     col.write(k[2])
#     col.write('mAp')
#     col.write(k[3])
#     # print(result)
#     result.confusion_matrix.plot(normalize=False, save_dir='img_input', names=(), on_plot=None)
#     col.write('Время выполнения, сек')
#     col.write(time.time() - start_time)
#     col.write('Confusion matrix')
#     col.image('img_input/confusion_matrix.png')
#
# if model1!=None:
#     print_mod(col1, model1)
# if model2!=None:
#     print_mod(col2, model2)
# if model3!=None:
#     print_mod(col3, model3)



