import os
import json
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv
from .prompts import SYSTEM_PROMPT, USER_PROMPT, functions
from .component_manager import function_calling, player_manager, npc_manager

load_dotenv()
model_name = "gpt-4o-mini"

class LLMManager:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.sys_prompt = SYSTEM_PROMPT
    
    def load_scenario(self, scenario: str):
        self.sys_prompt = SYSTEM_PROMPT.format(scenario=scenario)
        # print(f"System prompt: {self.sys_prompt}")
        
    def get_response(self, messages: List[Dict[str, str]], player_input: str, module_context: str = "") -> str:
        """Get response from LLM with context."""

        user_prompt = USER_PROMPT.format(player_input=player_input,)
        # player_name=player_manager.players.keys()[0])#TODO: 玩家名字
        # print(f"User prompt: {user_prompt}")

        messages.append({
            "role": "user",
            "content": user_prompt
        })
        system_message = {
            "role": "system",
            "content": self.sys_prompt
        }
        
        full_messages = [system_message] + messages
        response = self.client.chat.completions.create(
            model=model_name,
            messages=full_messages,
            temperature=0.7,
            tools=functions,
        )
        retry_times = 3
        response = None
        while retry_times > 0:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=full_messages,
                temperature=0.7,
                tools=functions,
            )
            toolcalls = response.choices[0].message.tool_calls
            if toolcalls:
                full_messages.append(response.choices[0].message)
                for toolcall in toolcalls:
                    function_name = toolcall.function.name
                    function_args = json.loads(toolcall.function.arguments)
                    try:
                        print(f"Calling function: {function_name}, {function_args}")
                        function_response = function_calling(function_name, function_args)
                    except Exception as e:
                        print(f"Function calling error: {e}")
                        function_response = f"发生了一些错误:Function calling error: {e}"
                    full_messages.append({
                        "role": "tool",
                        "tool_call_id": toolcall.id,
                        "content": str(function_response)
                    })
            else:
                break
        return full_messages[1:], response.choices[0].message.content 
