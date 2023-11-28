import json
import time

from call.callFunc import callFunc
import config
Client=config.client
class gptRes:
    def __init__(self,status,run,thread_id):
        self.thread_id=thread_id
        self.run=run
        self.status = status
        self.chat=""
        self.func=""
        self.func_id=None
        self.arguments=None
        self.res=None
        if self.status=="completed":
            self.__completed()
        elif self.status=="queued":
            self.__queued()
        elif self.status=="requires_action":
            self.__requires_action()


    def __completed(self):
        messages=Client.beta.threads.messages.list(
            thread_id=self.thread_id
        )
        self.res=json.dumps({
            "status":self.status,
            "chat":json.loads(messages.model_dump_json())['data'][0]['content'][0]['text']['value']
        })

    def __queued(self):
        messages=Client.beta.threads.messages.list(
            thread_id=self.thread_id
        )
        self.res=json.dumps({
            "status":self.status,
            "chat":json.loads(messages.model_dump_json())['data'][0]['content'][0]['text']['value']
        })

    def __requires_action(self):
        callFunc(self.run['required_action']['submit_tool_outputs']['tool_calls'],self.thread_id,self.run['id'])
        while True:
            time.sleep(5)
            run=Client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=self.run['id']
            )
            gptRes=judgeStatus(run,self.thread_id)
            if gptRes!=None:
                self.res=json.dumps({
                    "status":self.status,
                    "chat":json.loads(gptRes.res)['chat']
                })
                break


def judgeStatus(run,thread_id):
    run=json.loads(run.model_dump_json())
    status=run['status']
    print("status: "+status)
    if status=="in_progress":
        print("gpt is in_progress")
        return None
    else:
        return gptRes(status,run,thread_id)







