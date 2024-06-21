import lackey
from PIL import ImageGrab

from DataProcessingModules import BboxProcessing
from OcrIntegrationModules import Ocr


def by_text(text, num):
    snapshot = ImageGrab.grab()
    save_path = "./DataProcessingModules/screen.png"
    snapshot.save(save_path)
    ocr = Ocr.Ocr()
    result = ocr.get_text(save_path)
    bboxes = BboxProcessing.get_matching_bboxes(result, text)
    box = BboxProcessing.get_bbox(bboxes, num)
    match = lackey.Match(0.9, lackey.Location(10, 10), [box[0], [(box[1][0] - box[0][0]), (box[2][1] - box[0][1])]])
    match.highlight(3, "green")
    match.click()

def highlight_variants(text):
    snapshot = ImageGrab.grab()
    save_path = "./DataProcessingModules/screen.png"
    snapshot.save(save_path)
    ocr = Ocr.Ocr()
    result = ocr.get_text(save_path)
    print("showing variants...")
    bboxes = BboxProcessing.highlight_matching_bboxes(result, text)
    return bboxes

def variant_num(bboxes,num):
    box = BboxProcessing.get_bbox_by_num(bboxes, num)
    match = lackey.Match(0.9, lackey.Location(10, 10), [box[0], [(box[1][0] - box[0][0]), (box[2][1] - box[0][1])]])
    match.highlight(3, "green")
    match.click()
