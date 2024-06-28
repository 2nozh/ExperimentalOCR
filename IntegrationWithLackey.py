import configparser
import time

import lackey

from DataProcessingModules import Click


def tesseract_example():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    app_path = config.get("Paths", "toDoList_path")
    app = lackey.App(app_path)
    app.open()
    print("waiting for app to open")
    time.sleep(5)
    lackey.wait("pictures\\ToDoList_Landing.png")
    print("opened successfully")
    # lackey.click("pictures\\maximize.png")
    # time.sleep(2)
    print("ready for commands")
    Click.by_text('Добавить', 0)
    time.sleep(2)
    lackey.type("test task")
    lackey.click("pictures\ToDoList_Button.png")

def real_time_tesseract_example():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    #app_path = config.get("Paths", "toDoList_path")
    app_path = "C:\\Users\\aseslavinskaya\\AppData\\Local\\Programs\\todoist\\Todoist.exe"
    print('default app is "toDoList", to change, type path to exe file:')
    app= input()
    if app=='':
        app = lackey.App(app_path)
    app.open()
    print("waiting for app to open")
    time.sleep(3)
    print('ready for commands, write "quit" to exit')
    text=''
    while text!='quit':
        #try:
        print("write text to search:")
        text = input()
        bboxes=Click.highlight_variants(text)
        if len(bboxes)>0:
            print("write variant number to click (0 to skip):")
            num=int(input())
            if num>0:
                Click.variant_num(bboxes,num-1)
        else:
            print("text was not found,try again")
        #except:
         #   print("something went wrong")


if __name__ == '__main__':
    real_time_tesseract_example()
