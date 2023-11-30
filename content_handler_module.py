import json
from typing import Dict
from langchain.llms.sagemaker_endpoint import LLMContentHandler

class ContentHandler(LLMContentHandler):  
    content_type = "application/json"  
    accepts = "application/json"  

    def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:  
        input_str = json.dumps({prompt: prompt, **model_kwargs})  
        return input_str.encode("utf-8")  

    def transform_output(self, output: bytes) -> str:  
        response_json = json.loads(output.read().decode("utf-8"))  
        return response_json[0]["generated_text"]
