import streamlit as st
import cv2
import os

st.set_page_config(layout='wide', page_title='Алабуга - 4')
st.header('Извлечение кадров')


cl = st.sidebar.text_input('Введите директорию видео', 'vid_input/1')
cl_rep = os.listdir(cl)
cl_name = cl.replace('/', '-')
num = 1


def video_kadr (name):
    # name = "vid/vid_Al/1.mkv"

    cap = cv2.VideoCapture(name)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    res, frame = cap.read()
    frame = frame*1.1
    st.write(name)
    col1, col2 = st.columns(2)

    sl_1 = col1.slider('Начальный кадр '+ name, 0, length-50, 0)
    cap.set(cv2.CAP_PROP_POS_FRAMES, sl_1)
    res, frame = cap.read()
    col1.image(frame)
    sl_2 = col2.slider('Конечный кадр '+name, sl_1+1, length-50, length-50)
    cap.set(cv2.CAP_PROP_POS_FRAMES, sl_2)
    res, frame = cap.read()
    col2.image(frame)

    return sl_1,sl_2
try:
    start = []
    end = []
    if len(cl_rep)>0:
        for vid in cl_rep:
            sl1,sl2 = video_kadr(cl+'/'+vid)
            start.append(sl1)
            end.append(sl2)

    # st.sidebar.write(start, end)
        cap = cv2.VideoCapture(cl+'/'+cl_rep[0])
        res, frame = cap.read()



    col1,col2,col3 = st.columns(3)

    if col1.button("Запись видео"):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        name_res = 'result' + cl + '.avi'
        vid_res = cv2.VideoWriter('result/'+cl_name+'.avi', fourcc, 24, (frame.shape[0], frame.shape[1]))
        k = 0
        for vid in cl_rep:
            cap = cv2.VideoCapture(cl+'/'+vid)
            cap.set(cv2.CAP_PROP_POS_FRAMES, start[k])
            for i in range(start[k], end[k]):
                ok, frame = cap.read()

                vid_res.write(frame)
                cv2.waitKey(1)

            k +=1
        vid_res.release()

        col1.success("Видео сохранено")

    if col2.button("Запись кадров"):
        k = 0
        path = os.path.join('result\\frames', cl_name)
        os.mkdir(path)
        for vid in cl_rep:
            cap = cv2.VideoCapture(cl+'/'+vid)
            cap.set(cv2.CAP_PROP_POS_FRAMES, start[k])
            for i in range(start[k], end[k]):
                ok, frame = cap.read()

                # vid_res.write(frame)
                cv2.imwrite(path+'\\'+vid+'_'+str(i)+'.jpg',frame)
                # st.write(path+'\\'+vid+'_'+str(i)+'.jpg')

            k +=1


        col2.success("Кадры сохранены в " + 'result/frames/'+cl_name)

    if col3.button("Запись видео из кадров"):
        kadr_ = os.listdir('result/frames/'+cl_name)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        name_res = 'result' + cl + '.avi'
        vid_res = cv2.VideoWriter('result/' + cl_name + '_from_frames.avi', fourcc, 24, (frame.shape[0], frame.shape[1]))
        for kadr in kadr_:
                frame = cv2.imread('result/frames/'+cl_name+'/'+kadr)
                vid_res.write(frame)

        vid_res.release()

        col3.success("Кадры сохранены в " + cl_name + '_from_frames.avi')
except:
    st.error('Видео не найдены')






