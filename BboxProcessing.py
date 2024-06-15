import lackey
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
highlight_for = config.get("Time","highlight")
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
        for box in bboxes:
            match = lackey.Match(0.9, lackey.Location(10, 10), [box[0], [(box[1][0] - box[0][0]), (box[2][1] - box[0][1])]])
            match.highlight(highlight_for, "red")
        return bboxes[num]
    else:
        return []