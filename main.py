
from annotation.gptFunc import gptFunc
from cls.gpt import gpt
from flask import Flask, request


app = Flask(__name__)
chatgpt=gpt("招待机器人","""你是一个招待机器人，你一共有三个状态，第一个状态：当别人想购物的时候，你就调用购物函数，第二个状态：当别人想离开的时候，调用离开函数，
                                           第三个状态：当别人说的话都不在前两个状态时，调用无视函数
    ""","gpt-3.5-turbo-1106")
@gptFunc(gpt=chatgpt,funcName="shopFunc",funcDescription="这个函数是购物函数",paramDescription={"name":"这个参数是对话者的名字"},required=["name"])
def shopFunc(name):
    print(name+"想购物")
    return name+"想购物"

@gptFunc(gpt=chatgpt,funcName="leaveFunc",funcDescription="这个函数是离开函数",paramDescription={"name":"这个参数是对话者的名字"},required=["name"])
def leaveFunc(name):
    print(name+"想离开")
    return name+"想离开"

@gptFunc(gpt=chatgpt,funcName="nothingFunc",funcDescription="这个函数是无视函数",paramDescription={"name":"这个参数是对话者的名字"},required=["name"])
def nothingFunc(name):
    print(name+"在随便说话")
    return name+"在随便说话"

@app.route("/user",methods=["POST"])
def user():
    form = request.form
    name=form.get("name")
    chatgpt.addThread(name)
    return "success"

@app.route("/start",methods=["POST"])
def start():
    chatgpt.create()
    return "success"

@app.route("/chat",methods=["POST"])
def chat():
    form=request.form
    name=form.get("name")
    chat=form.get("chat")
    instructions="""客户的名字是{name}""".format(name=name)
    res=chatgpt.chat(chat,name,5,instructions)
    print(res)
    return res
if __name__=="__main__":
    app.run(host="0.0.0.0", port=8082)




