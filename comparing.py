from datetime import datetime
from glob import glob
import Levenshtein
import keras_ocr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display

from OcrTools import get_text_tesseract, get_text_easyocr,get_text_keras


def save_result_plot(img_fn, data_tesseract, data_easyocr, data_kerasocr):
    figsize = [30, 20]
    fig, axs = plt.subplots(2, 2, figsize=(figsize))
    axs[0, 0].set_title('initial', fontsize=24)
    axs[0, 0].imshow(plt.imread(img_fn))
    datadata_framesrames = [data_tesseract, data_easyocr, data_kerasocr]
    titles = ["tesseract  results", "easyocr results", "keras ocr results"]
    positions = [[0, 1], [1, 0], [1, 1]]
    for idx, data in enumerate(datadata_framesrames):
        position = positions[idx]
        title = titles[idx]
        results = data[['text', 'bbox']].values.tolist()
        results = [(x[0], np.array(x[1])) for x in results]
        keras_ocr.tools.drawAnnotations(plt.imread(img_fn),
                                        results, ax=axs[*position])
        axs[*position].set_title(title, fontsize=24)
    time = datetime.now().strftime("%m_%d__%H_%M_%S")
    id = image.split("\\")[1].split(".")[0]
    plt.tight_layout()
    plt.savefig(f'output/result_{id}_{time}.png')

def result_string(records):
    words=[]
    for row in records.iterrows():
            word = row[1].values[0]
            word = word.strip()
            if word!="":
                words.append(word.upper())
    return " ".join(words)


def get_accuracy(data_frame,text_expected):
    words = data_frame[['text']]
    text_found = result_string(words)
    accuracy = Levenshtein.ratio(text_found, text_expected)
    print(f'expecting {text_expected}, found {text_found}, accuracy {accuracy}')
    return accuracy
def process_image(image):
    #ряд в таблице, относящийся к текущему изображению
    image_statistic=[]
    #id изображения
    id = image.split("\\")[1].split(".")[0]
    image_statistic.append(id)

    #получение результатов и времени распознавания
    data_frame_1, time1 = get_text_tesseract(image)
    data_frame_2, time2 = get_text_easyocr(image)
    data_frame_3, time3 = get_text_keras(image)

    #добавление времени распознавания в статистику
    image_statistic.extend([time1, time2, time3])

    #получение и добавление в статистику эталонного текста из датасета
    records = annot[annot.image_id == id][['utf8_string']]
    text_expected = result_string(records)
    #image_statistic.append(text_expected)

    #вычисление и добавление в статистику точности распознавания
    for data_frame in [data_frame_1,data_frame_2,data_frame_3]:
        accuracy = get_accuracy(data_frame,text_expected)
        image_statistic.append(accuracy)
    return [image_statistic,[data_frame_1,data_frame_2,data_frame_3]]

if __name__ == '__main__':
    # image = "pictures\\img_1.png"
    annot = pd.read_parquet('input/annot.parquet')
    imgs = pd.read_parquet('input/img.parquet')
    img_fns = glob('input/random_images/*')
    table = []
    for i in range(3, 6):
        image = img_fns[i]
        statistic,data_frames=process_image(image)
        table.append(statistic)
        save_result_plot(image,*data_frames)
    data_frame_results = pd.DataFrame(table, columns=['id','tesseract_time', 'easyocr_time', 'keras_ocr_time','tesseract_accuracy', 'easyocr_accuracy', 'keras_ocr_accuracy'])
    display(data_frame_results.to_string())
