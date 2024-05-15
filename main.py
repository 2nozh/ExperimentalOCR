import timeit
from functools import wraps

import lackey
import easyocr
import time
from PIL import ImageGrab


def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = f(*args, **kwargs)
        elapsed_time = timeit.default_timer() - start_time
        print("time elapsed for",f.__name__ ,":",elapsed_time)
        return result
    return wrapper
def lackeyTest_notepad():
    notepad = lackey.App("C:\\Windows\\System32\\notepad.exe")
    notepad.open()
    lackey.wait("pictures\\notepadHeader.png")
    #notepad.focus()
    lackey.type("hello from lackey")
    lackey.hover("pictures\\fileButton.png")
    lackey.click("pictures\\spravkaButton.png")
    lackey.click("pictures\\notepadApp.png")
    lackey.type(lackey.Key.ENTER)
    #lackey.type("this is bold")
    #lackey.type(lackey.Key.ENTER)
    #lackey.type("this is cursive")
    hello = lackey.find("pictures\\helloFromlackey.png")
    hello.highlight(2,"green")
    #hello.findText("hello")
    notepad.close()
def getTextBox(resultSet,text):
    for [bbox,value,prob] in resultSet:
        if text in value:
            print("found",text,"in",value,"coord:",bbox)
            return bbox

def ocrTest():
    reader = easyocr.Reader(['en'])
    result = reader.readtext("pictures\\img_1.png")
    for (bbox,text,prob) in result:
        print(bbox,text,prob)
    box = getTextBox(result,"view")
@timing
def getAllText():
    reader = easyocr.Reader(['en'])
    result = reader.readtext("C:\\Users\\aseslavinskaya\\PycharmProjects\\TextRecog\\screen.png")
    return result
def ocrTest_notepad():
    print("starting",time.time())
    notepad = lackey.App("C:\\Windows\\System32\\notepad.exe")
    notepad.open()
    print("start open", time.time())
    lackey.wait("pictures\\notepadHeader.png")
    print("end open", time.time())
    lackey.click("pictures\\maximize.png")
    lackey.type("hello from lackey and easyOcr")

    snapshot = ImageGrab.grab()
    save_path = "C:\\Users\\aseslavinskaya\\PycharmProjects\\TextRecog\\screen.png"
    snapshot.save(save_path)
    print("start read", time.time())
    result = getAllText()
    print("end read", time.time())
    print("start search and draw", time.time())
    for (bbox, text, prob) in result:
        print(bbox, text, prob)
    box= getTextBox(result,"ello")
    print(box)

    match = lackey.Match(0.9,lackey.Location(10,10),[box[0],[(box[1][0]-box[0][0]),(box[2][1]-box[0][1])]])
    match.highlight(5,"red")
    print("end search and draw", time.time())


    #hello.findText("hello")
    notepad.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #lackeyTest_notepad()
    #time.sleep(2)
    ocrTest_notepad()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
