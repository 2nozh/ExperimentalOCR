import configparser
from datetime import datetime

from IPython.display import display

import OcrIntegrationModules.OcrTools as OcrTools
from OcrIntegrationModules.OcrToolsSelector import OcrToolsSelector


class Ocr():
    OCR = OcrToolsSelector.default.value
    config = configparser.ConfigParser()
    config.read("settings.ini")
    root = config.get("Paths", "work_dir_path")
    save_results_path = config.get("Paths", "save_results_path")

    def get_text(self, image):
        if self.OCR == 1:
            return OcrTools.get_text_tesseract(image)[0]
        elif self.OCR == 2:
            return OcrTools.get_text_easyocr(image)[0]
        elif self.OCR == 3:
            return OcrTools.get_text_keras(image)[0]

    def get_text_explain(self, image):
        data_frame_tesseract, time_tesseract = OcrTools.get_text_tesseract(image)
        data_frame_easyocr, time_easyocr = OcrTools.get_text_easyocr(image)
        data_frame_keras, time_keras = OcrTools.get_text_keras(image)
        print(f"-----tesseract results ({time_tesseract})-----")
        display(data_frame_tesseract)
        print(f"-----easyOcr results ({time_easyocr})-----")
        display(data_frame_easyocr)
        print(f"-----keras Ocr results ({time_keras})-----")
        display(data_frame_keras)
        if self.OCR == 1:
            return data_frame_tesseract
        elif self.OCR == 2:
            return data_frame_easyocr
        elif self.OCR == 3:
            return data_frame_keras

    def get_and_print_dataframes(self, image):
        data_frame_tesseract, time_tesseract = OcrTools.get_text_tesseract(image)
        data_frame_easyocr, time_easyocr = OcrTools.get_text_easyocr(image)
        data_frame_keras, time_keras = OcrTools.get_text_keras(image)
        print(f"-----tesseract results ({time_tesseract})-----")
        display(data_frame_tesseract)
        time = datetime.now().strftime("%m_%d__%H_%M_%S")
        data_frame_tesseract.to_csv(f"{self.save_results_path}/df_tes_{time}.csv",sep=',',index=True, encoding='utf-8')
        print("-----------------------------------------------")
        print(f"-----easyOcr results ({time_easyocr})-----")
        display(data_frame_easyocr)
        data_frame_tesseract.to_csv(f"{self.save_results_path}/df_eas_{time}.csv", sep=',', index=True, encoding='utf-8')
        print("-----------------------------------------------")
        print(f"-----keras Ocr results ({time_keras})-----")
        display(data_frame_keras)
        data_frame_tesseract.to_csv(f"{self.save_results_path}/df_ker_{time}.csv", sep=',', index=True, encoding='utf-8')
        print("-----------------------------------------------")
        results = []
        results.append([data_frame_tesseract, time_tesseract])
        results.append([data_frame_easyocr, time_easyocr])
        results.append([data_frame_keras, time_keras])
        return results
