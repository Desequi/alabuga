import cv2
import os
import str_task4
import streamlit as st
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

st.set_page_config(layout='wide', page_title='Алабуга - 4')
st.header('Обнаружение на наборе изображений')

cl = st.sidebar.text_input('введите путь к файлам', 'vid_input/1')
cl_frm = os.listdir(cl)

model = st.sidebar.selectbox(
    'Выберите модель',
    os.listdir(str_task4.cl_mod),
    index=None,
    format_func=lambda s: s.upper())

@st.cache_data
def prd_yol(model, cl):
    model = YOLO(str_task4.cl_mod+'/'+model)

    # st.write(cl_frm)
    frame = cv2.imread(cl+'/'+cl_frm[0])
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    # print (name_res)
    vid_res = cv2.VideoWriter(cl+'res.avi', fourcc, 24, (frame.shape[0], frame.shape[1]))
    for frm in cl_frm:
        frame =cv2.imread(cl+'/'+frm)

        result = model.predict(frame)

        for r in result:

            annotator = Annotator(frame)

            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, model.names[int(c)])

        frame = annotator.result()

        vid_res.write(frame)

    vid_res.release()
try:
    prd_yol(model, cl)
    len_vid = len(cl_frm)

    cap = cv2.VideoCapture(cl+'res.avi')
    res, frame = cap.read()
    frame = frame*1.1


    sl_1 = st.slider('Текущий кадр '+ cl+'res.avi', 0, len_vid-1, 0)
    cap.set(cv2.CAP_PROP_POS_FRAMES, sl_1)
    res, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    st.image(frame)
except:
    st.error('Файлы не найдены')
