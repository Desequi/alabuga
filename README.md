VideoFrameProcessor
Для запуска требуется установить пакеты из файла requirements.txt, сменить абсолютный путь val в файле data.py и запустить в терминале из папки проекта командой

streamlit run str_task4.py

Данный веб-сервис позволяет пользователю загружать видео, разбивать его на кадры и обрабатывать каждый кадр. Сервис также предоставлять возможность объединения обработанных кадров обратно в видеофайл и сохранения его в указанную директорию, а также поддерживать режим реального времени для обработки видео с камеры.

Сервис разделен на 7 частей:

str_task4 - описательная часть сервиса. Здесь можно задать путь к обученным моделям

chg_img - приложение для работы с изображениями и набором кадров с просмотром результата.При его выборе в окне браузера будет возможность подгрузить изображение. При загрузке появляется возможность просмотреть изменения и влияние изменений на обнаружение
![chg_img](/vid_input/gif/Video1.gif)
detect_frames - приложение для обработки с помощью обученной модели набора кадров. Для получения результирующего набора требуется выбрать путь до набора кадров, выбрать модель для обработки и в основном поле появится слайдер с выбором номера кадра и под ним его обработанное представление. Видео с обработанными кадрами сохранено в каталоге выше.

![detect_frames](/vid_input/gif/Video2.gif)
detect_video - приложение для обработки видео с помощью обученной модели. На экране можно выбрать модель и ввести путь до видео. После обработки появится слайдер с кадрами и обработанное видео. Результат сохранен там же, где и оригинал видео.

![detect_video](/vid_input/gif/Video3.gif)
get_frames - приложение для извлечения кадров из набора видео. При выборе папки с видеоданными для каждого файла доступен выбор начального и конечного кадра для извлечения. По нажатию на кнопку "запись видео" формируется видеофайл с выбранными фрагментами. По нажатию на кнопку "запись кадров" создается подкаталог и записывается набор выбранных кадров в формате .pngПо нажатию на кнопку "запись видео из кадров" формируется видеофайл из изображений из каталога

![get_frames](/vid_input/gif/Video4.gif)
test_models - приложение сравнения обученных моделей по тестовым данным. Позволяет выбрать до трех моделей и сравнить характеристики в блочном виде

detect_cam - запускает многопоточное приложение для обнаружения с подключенной видеокамеры в реальном времени
![detect_cam](/vid_input/gif/Video5.gif)

