
def listToJson(liste):
    jsonList = []
    for data in liste :
        jsonList.append(data.to_json())
    return jsonList