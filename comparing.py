import pandas as pd
import numpy as np

from glob import glob
from tqdm.notebook import tqdm
from datetime import datetime

import matplotlib.pyplot as plt
from PIL import Image
import pytesseract
import easyocr
import keras_ocr
#keras_ocr=''
from IPython.display import display

def getText_tesseract(image):
    print("---PYTESSERACT---")
    #print(pytesseract.image_to_string(image))
    #print(pytesseract.image_to_boxes(image))
    #print(pytesseract.image_to_data(image))
    results = pytesseract.image_to_data(Image.open(image)).split('\n')
    formatted_results = []
    for item in results[1:]:
        record=item.split('\t')
        if (record==[] or record==['']):
            continue
        level,page_num,block_num,par_num,line_num,word_num,left,top,width,height,conf,text=item.split('\t')
        if (conf=='-1'):
            continue
        left=int(left)
        right=left+int(width)
        top=int(top)
        bottom=top+int(height)
        bbox=[[left,top],[right,top],[right,bottom],[left,bottom]]
        formatted_results.append([bbox,text,conf])
    dataFrame = pd.DataFrame(formatted_results, columns=['bbox', 'text', 'conf'])
    display(dataFrame.to_string())
    return dataFrame


def getText_easyocr(image):
    print("---EASYOCR---")
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image)
    print(results)
    dataFrame = pd.DataFrame(results, columns=['bbox', 'text', 'conf'])
    display(dataFrame.to_string())
    return dataFrame


def getText_kerasocr(image):
    print("---KERAS_OCR---")
    pipeline = keras_ocr.pipeline.Pipeline()
    results = pipeline.recognize([image])
    dataFrame = pd.DataFrame(results[0], columns=['text', 'bbox'])
    display(dataFrame.to_string())


    """
    fig, ax = plt.subplots(figsize=(10, 10))
    keras_ocr.tools.drawAnnotations(plt.imread(pic), results[0], ax=ax)
    ax.set_title('Keras OCR Result Example')
    plt.show()
    """
    return dataFrame


def plot_compare(img_fn, easyocr_df, kerasocr_df):
    fig, axs = plt.subplots(1, 2, figsize=(30, 20))

    easy_results = easyocr_df[['text','bbox']].values.tolist()
    easy_results = [(x[0], np.array(x[1])) for x in easy_results]
    keras_ocr.tools.drawAnnotations(plt.imread(img_fn),
                                    easy_results, ax=axs[0])
    axs[0].set_title('easyocr results', fontsize=24)

    keras_results = kerasocr_df[['text','bbox']].values.tolist()
    keras_results = [(x[0], np.array(x[1])) for x in keras_results]
    keras_ocr.tools.drawAnnotations(plt.imread(img_fn),
                                    keras_results, ax=axs[1])
    axs[1].set_title('keras_ocr results', fontsize=24)
    plt.show()
    return plt

def displayImages():
    annot = pd.read_parquet('input/textocr-text-extraction-from-images-dataset/annot.parquet')
    imgs = pd.read_parquet('input/textocr-text-extraction-from-images-dataset/img.parquet')
    img_fns = glob('input/textocr-text-extraction-from-images-dataset/train_val_images/train_images/*')

    #display first 25 img
    fig, axs = plt.subplots(5, 5, figsize=(20, 20))
    axs = axs.flatten()
    for i in range(25):
        axs[i].imshow(plt.imread(img_fns[i]))
        axs[i].axis('off')
        image_id = img_fns[i].split('/')[-1].rstrip('.jpg')
        n_annot = len(annot.query('image_id == @image_id'))
        axs[i].set_title(f'{image_id} - {n_annot}')
    plt.show()

def displayImage(image):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 10))
    #ax.imshow(plt.imread(img_fns[0]))
    #ax.axis('off')
    ax.imshow(plt.imread(image))
    plt.show()


def savePlot(img_fn,data):
    n=1
    fig, axs = plt.subplots(1, 2, figsize=(30, 20))
    results = data[['text','bbox']].values.tolist()
    results=[(x[0],np.array(x[1])) for x in results]
    keras_ocr.tools.drawAnnotations(plt.imread(img_fn),
                                    results,ax=axs[0])
    axs[0].set_title('results',fontsize=24)
    name=datetime.now().strftime("%m_%d__%H_%M_%S")
    print(name)
    plt.savefig(f'output/result_{name}.png')
    #plt.show()

"""
    easy_results = easyocr_df[['text','bbox']].values.tolist()
    easy_results = [(x[0], np.array(x[1])) for x in easy_results]
    keras_ocr.tools.drawAnnotations(plt.imread(img_fn),
                                    easy_results, ax=axs[0])
    axs[0].set_title('easyocr results', fontsize=24)

    keras_results = kerasocr_df[['text','bbox']].values.tolist()
    keras_results = [(x[0], np.array(x[1])) for x in keras_results]
    keras_ocr.tools.drawAnnotations(plt.imread(img_fn),
                                    keras_results, ax=axs[1])
    axs[1].set_title('keras_ocr results', fontsize=24)
    return plt
"""


if __name__ == '__main__':
    image = "pictures\\img_1.png"

    getText_tesseract(image)
    dataFrame1 = getText_easyocr(image)
    dataFrame2 = getText_tesseract(image)
    savePlot(image,dataFrame2)
    #dataFrame2 = getText_kerasocr(image)
    #plot_compare(image, dataFrame1, dataFrame2).savefig('output/resultPlot.png')









