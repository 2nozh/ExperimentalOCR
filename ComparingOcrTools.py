from glob import glob

import pandas as pd
from IPython.display import display

from DataProcessingModules.AnalyzeTools import *

config = configparser.ConfigParser()
config.read("settings.ini")
root = config.get("Paths", "work_dir_path")
save_results_path = config.get("Paths", "save_results_path")


def process_images_from_dataset():
    annot = pd.read_parquet(f'{root}/input/annot.parquet')
    img_fns = glob(f'{root}/input/random_images/*')
    table = []
    for i in range(1, 3):
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


if __name__ == '__main__':
    process_images_from_folder(f'{root}/input/interface')
