#@gptFunc(gpt=gptClass,funcName="",funcDescription=,paramDescription={},required=[])
def gptFunc(**kwds):
    tool = {
        "type": "function",
        "function": {
            "name": kwds['funcName'],
            "description": kwds['funcDescription'],
            "parameters": {
                "type": "object",
                "properties": {x: {
                    "type": "string",
                    "description": kwds['paramDescription'][x]
                } for x in kwds['paramDescription']}
                , "required": kwds['required']
            }
        }

    }
    kwds['gpt'].tools.append(tool)
    def decorate(fn):
        return fn
    return decorate


