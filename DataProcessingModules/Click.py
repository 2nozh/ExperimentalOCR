import lackey
from DataProcessingModules import BboxProcessing
from PIL import ImageGrab
from OcrIntegrationModules import Ocr


def by_text(text,num):
    snapshot = ImageGrab.grab()
    save_path = "../screen.png"
    snapshot.save(save_path)
    ocr= Ocr.Ocr()
    result=ocr.get_text(save_path)
    bboxes = BboxProcessing.get_matching_bboxes(result, text)
    box = BboxProcessing.get_bbox(bboxes, num)
    match = lackey.Match(0.9, lackey.Location(10, 10), [box[0], [(box[1][0] - box[0][0]), (box[2][1] - box[0][1])]])
    match.highlight(3, "green")
    match.click()
