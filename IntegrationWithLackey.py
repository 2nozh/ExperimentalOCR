import lackey
import configparser
import Click
import time

def tesseract_example():
    print("waiting for app to open")
    lackey.wait("pictures\\ToDoList_Landing.png")
    print("opened successfully")
    #lackey.click("pictures\\maximize.png")
    #time.sleep(2)
    print("ready for commands")
    Click.by_text('Добавить', 0)
    time.sleep(2)
    lackey.type("test task")
    #click_by_text('Добавить', 1)
    lackey.click("pictures\ToDoList_Button.png")   

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("settings.ini")
    app_path = config.get("Paths","toDoList_path")
    app = lackey.App(app_path)
    app.open()
    tesseract_example()

