import time

import easyocr
import keras_ocr
import pandas as pd
import pytesseract
from PIL import Image


def get_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        return [result, t2 - t1]

    return wrapper


@get_time
def get_text_tesseract(image):
    # eng+rus
    results = pytesseract.image_to_data(Image.open(image), lang='eng').split('\n')
    formatted_results = []
    for item in results[1:]:
        record = item.split('\t')
        if record == [] or record == ['']:
            continue
        level, page_num, block_num, par_num, line_num, word_num, left, top, width, height, conf, text = item.split('\t')
        if conf == '-1':
            continue
        left = int(left)
        right = left + int(width)
        top = int(top)
        bottom = top + int(height)
        bbox = [[left, top], [right, top], [right, bottom], [left, bottom]]
        formatted_results.append([bbox, text, conf])
    data_frame = pd.DataFrame(formatted_results, columns=['bbox', 'text', 'conf'])
    return data_frame


@get_time
def get_text_easyocr(image):
    # 'en', 'ru'
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image)
    print(results)
    data_frame = pd.DataFrame(results, columns=['bbox', 'text', 'conf'])
    return data_frame


@get_time
def get_text_keras(image):
    pipeline = keras_ocr.pipeline.Pipeline()
    results = pipeline.recognize([image])
    data_frame = pd.DataFrame(results[0], columns=['text', 'bbox'])
    return data_frame
