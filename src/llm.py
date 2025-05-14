import os
import json
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv
from .prompts import SYSTEM_PROMPT, functions
from .functions import function_calling

load_dotenv()
model_name = "gpt-4o-mini"

class LLMManager:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def get_response(self, messages: List[Dict[str, str]], module_texts: List[str] = []) -> str:
        """Get response from LLM with context."""
        sys_prompt = SYSTEM_PROMPT.format(scenario="\n".join(module_texts))
        system_message = {
            "role": "system",
            "content": sys_prompt
        }
        
        full_messages = [system_message] + messages
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
                    function_response = function_calling(function_name, function_args)
                except Exception as e:
                    print(f"Function calling error: {e}")
                    return full_messages, None
                full_messages.append({
                    "role": "tool",
                    "tool_call_id": toolcall.id,
                    "content": str(function_response)
                })
            response = self.client.chat.completions.create(
                model=model_name,
                messages=full_messages,
                temperature=0.7,
                tools=functions,
            )
        return full_messages[1:], response.choices[0].message.content 
