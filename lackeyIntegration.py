import lackey
from PIL import ImageGrab

from Ocr import Ocr
from OcrTools import *

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
app_path = "C:\\Users\\aseslavinskaya\\AppData\\Local\\Programs\\todoist\\Todoist.exe"
def find_bbox(records):
    words = []
    for row in records.iterrows():
        word = row[1].values[0]
        word = word.strip()
        if word != "":
            words.append(word.upper())
    return " ".join(words)


def get_matching_bboxes(resultSet, text):
    result = resultSet.loc[resultSet['text'].str.contains(text)]
    bboxes = []
    for row in result.iterrows():
        bbox = row[1].values[0]
        bboxes.append(bbox)
    return bboxes


def get_bbox(bboxes, num=0):
    if len(bboxes) > 0:
        return bboxes[num]
    else:
        return []


def click_by_text(text, num=0):
    snapshot = ImageGrab.grab()
    save_path = "screen.png"
    snapshot.save(save_path)
    ocr=Ocr()
    result=ocr.get_text(save_path)
    bboxes = get_matching_bboxes(result, text)
    box = get_bbox(bboxes, num)
    match = lackey.Match(0.9, lackey.Location(10, 10), [box[0], [(box[1][0] - box[0][0]), (box[2][1] - box[0][1])]])
    match.highlight(1, "red")
    match.click()


if __name__ == '__main__':
    app = lackey.App(app_path)
    app.open()
    time.sleep(1)
    # lackey.click("pictures\\maximize.png")
    click_by_text('Добавить', 0)
    lackey.type("test task")
    click_by_text('Добавить', 1)
