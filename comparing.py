import pandas as pd
import numpy as np

from glob import glob
from tqdm.notebook import tqdm

import matplotlib.pyplot as plt
from PIL import Image
import pytesseract
import easyocr
import keras_ocr
from IPython.display import display


def plot_compare(img_fn, easyocr_df, kerasocr_df):
    fig, axs = plt.subplots(1, 2, figsize=(15, 10))

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

if __name__ == '__main__':
    print("start")
    pic = "pictures\\img_1.png"
    plt.style.use('ggplot')
    #annot = pd.read_parquet('input/textocr-text-extraction-from-images-dataset/annot.parquet')
    #imgs = pd.read_parquet('input/textocr-text-extraction-from-images-dataset/img.parquet')
    #img_fns = glob('input/textocr-text-extraction-from-images-dataset/train_val_images/train_images/*')

    fig, ax = plt.subplots(figsize=(10, 10))
    #ax.imshow(plt.imread(img_fns[0]))
    #ax.axis('off')
    ax.imshow(plt.imread(pic))
    plt.show()
    """ display first 25 img
    fig, axs = plt.subplots(5, 5, figsize=(20, 20))
    axs = axs.flatten()
    for i in range(25):
        axs[i].imshow(plt.imread(img_fns[i]))
        axs[i].axis('off')
        image_id = img_fns[i].split('/')[-1].rstrip('.jpg')
        n_annot = len(annot.query('image_id == @image_id'))
        axs[i].set_title(f'{image_id} - {n_annot}')
    plt.show()
    """
    print("---PYTESSERACT---")
    print(pytesseract.image_to_data(Image.open(pic)))
    print("---EASYOCR---")
    reader = easyocr.Reader(['en'], gpu=True)
    results = reader.readtext(pic)
    dataFrame1 = pd.DataFrame(results, columns=['bbox', 'text', 'conf'])
    display(dataFrame1.to_string())
    print("---KERAS_OCR---")
    pipeline = keras_ocr.pipeline.Pipeline()
    results = pipeline.recognize([pic])
    dataFrame2 = pd.DataFrame(results[0], columns=['text', 'bbox'])
    display(dataFrame2.to_string())
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    keras_ocr.tools.drawAnnotations(plt.imread(pic), results[0], ax=ax)
    ax.set_title('Keras OCR Result Example')
    plt.show()
    """

    plot_compare(pic,dataFrame1,dataFrame2)







