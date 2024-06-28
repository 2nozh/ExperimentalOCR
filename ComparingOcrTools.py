from glob import glob

import pandas as pd
from IPython.display import display

from DataProcessingModules.AnalyzeTools import *

"""

config = configparser.ConfigParser()
config.read("settings.ini")
root = config.get("Paths", "work_dir_path")
save_results_path = config.get("Paths", "save_results_path")
"""
root = "C://Users//aseslavinskaya//PycharmProjects//TextRecog"
save_results_path ="C://Users//aseslavinskaya//PycharmProjects//TextRecog"


def process_images_from_dataset(path_to_annot=f'{root}/input/annot.parquet',path_to_images=f'{root}/input/random_images/*',range_start=0,range_end=2):
    annot = pd.read_parquet(path_to_annot)
    img_fns = glob(path_to_images)
    table = []
    for i in range(range_start, range_end):
        image = img_fns[i]
        statistic, data_frames = process_image(image, annot)
        table.append(statistic)
        save_result_plot(image, *data_frames)
    data_frame_results = pd.DataFrame(table, columns=['id', 'tesseract_time', 'easyocr_time', 'keras_ocr_time',
                                                      'tesseract_accuracy', 'easyocr_accuracy', 'keras_ocr_accuracy'])
    display(data_frame_results.to_string())


def process_images_from_folder(folder):
    img_fns = glob(f'{folder}/*')
    table = []
    for i in range(0, len(img_fns)):
        image = img_fns[i]
        statistic, data_frames = process_image(image)
        table.append(statistic)
        save_result_plot(image, *data_frames)
    data_frame_results = pd.DataFrame(table, columns=['id', 'tesseract_time', 'easyocr_time', 'keras_ocr_time',
                                                      'tesseract_accuracy', 'easyocr_accuracy', 'keras_ocr_accuracy'])
    display(data_frame_results.to_string())

def optionalInput():
    answer=input()
    if answer=='':
        return None
    else:
        return answer

if __name__ == '__main__':
    print("приложение запущено в режиме сравнительного анализа инструментов распознавания тескста.\n"
          "Доступные опции:\n"
          "1 - Анализ изображений из датасета (потребуется путь файла annot.parquet с описанием изображений, и сами изображения)\n"
          "2 - Анализ изображений из директории (потребуется путь до директории с изображениями)\n"
          "Введите вариант:\n"
          "")
    selected=int(input())
    if selected==1:
        print("введите путь до файла annot.parquet (0 для default значений)"
              "\n" )
        path_to_parquet=input()
        if path_to_parquet=='0':
            path_to_parquet=f'{root}/input/annot.parquet'
        print("введите путь до директории с изображениями (0 для default значений)"
              "\n")
        path_to_images = input()
        if path_to_images=='0':
            path_to_images=f'{root}/input/random_images/*'
        print("введите начало интервала обработки (0 для default значений)"
              "\n")
        range_start = int(input())
        if range_start==0:
            range_start=0
        print("введите конец интервала обработки (0 для default значений)"
              "\n")
        range_end = int(input())
        if range_end==0:
            range_end=2
        process_images_from_dataset(path_to_parquet,path_to_images,range_start,range_end)
    if selected==2:
        print("введите путь до директории с изображениями (0 для default значений)"
              "\n")
        path_to_images = input()
        if path_to_images=='0':
            path_to_images=f'{root}/input/toTest'
        process_images_from_folder(path_to_images)
