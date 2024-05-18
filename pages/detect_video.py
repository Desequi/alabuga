import cv2
import os
import str_task4
import streamlit as st
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator


st.set_page_config(layout='wide', page_title='Алабуга - 4')
st.header('Обнаружение по видео')

# def save_uploadedfile(uploadedfile):
    # with open(os.path.join("vid_input", uploadedfile.name), "wb") as f:
        # f.write(uploadedfile.getbuffer())
    # return st.sidebar.success("Файл загружен: "+uploadedfile.name+".".format(uploadedfile.name))
# cl = os.listdir('vid_input')
# vid_type = st.sidebar.selectbox(
#     'Выберите видео',
#     cl,
#     index=1,
#     format_func=lambda s: s.upper())

# datafile = st.sidebar.file_uploader("Upload")
# if datafile is not None:
   # file_details = {"FileName":datafile.name,"FileType":datafile.type}
   # save_uploadedfile(datafile)

cl = st.sidebar.text_input('введите путь к видео', 'vid_input/1')
model = st.sidebar.selectbox(
    'Выберите модель',
    os.listdir(str_task4.cl_mod),
    index=1,
    format_func=lambda s: s.upper())
name_res = cl[:len(cl)-4]
@st.cache_data
def prd_yol(model, cl):
    model = YOLO(str_task4.cl_mod+'/'+model)
    cap = cv2.VideoCapture(cl)
    ret, frame = cap.read()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    # print (name_res)
    vid_res = cv2.VideoWriter(name_res+'_res.avi', fourcc, 24, (frame.shape[0], frame.shape[1]))
    len_vid = 0
    while True:
        ret, frame =cap.read()
        if ret:
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
            len_vid+=1
        else:
            vid_res.release()
            break
    return len_vid
try:
    len_vid = prd_yol(model, cl)
    cap = cv2.VideoCapture(name_res+'_res.avi')

    sl_1 = st.slider('Текущий кадр '+ name_res+'_res.avi', 0, len_vid-1, 0)
    cap.set(cv2.CAP_PROP_POS_FRAMES, sl_1)
    res, frame = cap.read()
    st.image(frame)
except:
    st.error('Видео не найдено')
# result = model.predict(cl)







