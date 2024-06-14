def getTextBox(data,text):
    for [bbox,value,prob] in data:
        if text in value:
            print("found",text,"in",value,"coord:",bbox)
            return bbox
