import json
import os
codes = ["CIV","BPC","CCP","COM","CONS","CORP","EDC","ELEC","EVID","FAC","FAM","FGC","FIN","GOV","HNC","HSC","INS","LAB","MVC","PCC","PEN","PRC","PROB","PUC","RTC","SHC","UIC","VEH","WAT","WIC"]


def main():

    with open("CIV.txt", "r") as text_file:
        rawText = text_file.read()
        dct = json.loads(rawText)

    text_file.close()
    counter = 0
    for k,v in dct.items():
        if counter == 10:
            break
        print("ID:{},  [{},Division {},Title {}, Part {}, Chapter {},Article {}, Section {}, isCodeDescription: {}, {}, {}, {}]".format(k, v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9], v[11]))
        counter += 1


def removeTokenCount(code):
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path)
    with open("{}/codeTexts/{}.txt".format(dir, code), "r") as text_file:
        rawText = text_file.read()
        dct = json.loads(rawText)
    new_dct = {}

    for k,v in dct.items():
        commaIndex = v.index(",")
        newValue = v[commaIndex+1:]
        new_dct[k] = newValue

    text_file.close()
    print("Finished reading {}.".format(code))
    with open('{}/codeTexts/{}.txt'.format(dir, code), 'w') as write_file:
        write_file.write(json.dumps(new_dct))
    write_file.close()
    print("Finished writing {}.".format(code))

def escape_characters(code):
    bad_chars = ["'"]
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path)
    with open("{}/codeTexts/{}.txt".format(dir, code), "r") as text_file:
        rawText = text_file.read()
        dct = json.loads(rawText)
    new_dct = {}
    for k, v in dct.items():
        print("old value: ", v)
        new_value = v
        for ch in bad_chars:
            new_value = new_value.replace(ch, "\{}".format(ch))
        print("new value:", new_value)
        break
def strip_text(code):
    print("Running strip_text for {}".format(code))
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path)
    with open("{}/codeTexts/{}.txt".format(dir, code), "r") as text_file:
        rawText = text_file.read()
        dct = json.loads(rawText)
    new_dct = {}

    for k, v in dct.items():

        newValue = v.strip()
        new_dct[k] = newValue

    text_file.close()

    with open('{}/codeTexts/{}.txt'.format(dir, code), 'w') as write_file:
        write_file.write(json.dumps(new_dct))
    write_file.close()

if __name__ == "__main__":
    main()