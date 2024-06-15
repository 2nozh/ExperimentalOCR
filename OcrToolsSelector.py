import enum


class OcrToolsSelector(enum.Enum):
    tesseract = 1
    easyocr = 2
    keras_ocr = 3
    default = 1
