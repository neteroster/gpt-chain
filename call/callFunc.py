import json
import sys
import config

Client=config.client
def callFunc(tool_calls,thread_id,run_id):
    tool_outputs=[]
    for tool_call in tool_calls:
        func_id=tool_call['id']
        arguments=tool_call['function']['arguments']
        arguments=json.loads(arguments)
        funcName=tool_call['function']['name']
        func=getattr(sys.modules["__main__"], funcName)
        funcRes=func(**arguments)
        tool_outputs.append({
            "tool_call_id":func_id,
            "output":funcRes
        })
    Client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_outputs
    )
