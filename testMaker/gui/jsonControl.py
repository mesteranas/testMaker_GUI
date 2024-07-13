# this file for opening and saving questions.json file
import json,os
import settings
path=os.path.join(os.getenv('appdata'),settings.app.appName,"questions.json")
def get():
    """
    get the json file and return it as dictionary (dict) 
    if file not fownd return a impty dict
    """
    try:
        with open(path,"r",encoding="utf-8") as file:
            data=json.load(file)
    except:
        data={}
    return data
def save(data:dict):
    """
    this define convert the (dect) into (json) then save it
    ?args
    :data:dict the dict to save  it
    """
    with open(path,"w",encoding="utf-8") as file:
        json.dump(data,file,ensure_ascii=True,indent=4)
