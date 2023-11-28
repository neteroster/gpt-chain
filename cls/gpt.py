import json
import time

from openai import OpenAI
import config
from cls.gptRes import judgeStatus
Client=config.client
class gpt:
    def __init__(self,name,instructions,model):
        self.name=name
        self.instructions=instructions
        self.tools=[]
        self.model=model
        self.file_ids=[]
        self.assistant=None
        self.response=None
        self.personDict={}

    def addThread(self,name):
        self.personDict[name]=Client.beta.threads.create()
    def create(self):
        self.assistant = Client.beta.assistants.create(
            name=self.name,
            instructions=self.instructions,
            tools=self.tools,
            model=self.model,
            file_ids=self.file_ids
        )
    def chat(self,chat,name,time,instructions):
        message = Client.beta.threads.messages.create(
            thread_id=self.personDict[name].id,
            role="user",
            content=chat
        )
        run=Client.beta.threads.runs.create(
            thread_id=self.personDict[name].id,
            assistant_id=self.assistant.id,
            instructions=instructions
        )
        return self.__getRes(time,name,run)
    def __getRes(self,time_,name,run_):
        while True:
            time.sleep(time_)
            run=Client.beta.threads.runs.retrieve(
                thread_id=self.personDict[name].id,
                run_id=run_.id
            )
            gptRes=judgeStatus(run,self.personDict[name].id)
            if gptRes!=None:
                return gptRes.res


def uploadFile(filePath):
    return Client.files.create(
        file=open(filePath, "rb"),
        purpose='assistants'
    )




