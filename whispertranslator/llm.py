from dotenv import load_dotenv
import os
load_dotenv()

# LLM Base class
class BaseLLM:
    def __init__(self, model_path: str, system_prompt: str):
        """
        实现模型的初始化以及初始参数设定
        """
        self.model_path = model_path
        self.system_prompt = system_prompt
        self.model = self._load_model()

    def _load_model(self) -> None:
        raise NotImplementedError("子类必须实现模型的加载")

    def infer(self, input: str) -> str:
        """
        根据初始 system prompt 设定执行推理，返回推理结果
        """
        raise NotImplementedError("子类必须实现infer方法")

class OnlineLLM(BaseLLM):
    def __init__(self, system_prompt: str):
        """
        实现模型的初始化以及初始参数设定
        """
        self.system_prompt = system_prompt
        self.model = self._load_model()

    def _load_model(self) -> None:
        key = None
        raise NotImplementedError("子类必须实现模型的加载")

    def infer(self, input: str) -> str:
        """
        根据初始 system prompt 设定执行推理，返回推理结果
        """
        raise NotImplementedError("子类必须实现infer方法")
    
class LocalLLM(BaseLLM):
    def __init__(self, model_path: str, system_prompt: str, device:str):
        """
        实现模型的初始化以及初始参数设定
        """
        self.model_path = model_path
        self.system_prompt = system_prompt
        self.device = device
        self.model = self._load_model()

    def _load_model(self) -> None:
        raise NotImplementedError("子类必须实现模型的加载")

    def infer(self, input: str) -> str:
        """
        根据初始 system prompt 设定执行推理，返回推理结果
        """
        raise NotImplementedError("子类必须实现infer方法")

# OnlineLLM
class ChatGPTLLM(OnlineLLM):
    def __init__(self, system_prompt: str, dst_language:str):
        """
        实现模型的初始化以及初始参数设定
        """
        self.system_prompt = system_prompt
        self.dst_language = dst_language
        self.model = self._load_model()

    def _load_model(self):
        openai_key = os.getenv("OPENAI_TOKEN")
        # return client

    def infer(self, input: str) -> str:
        completion = self.model.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    # english prompt here to save tokens
                    "content": f'{self.prompt}'
                },
                {
                    "role":"user",
                    "content": f"Original text:`{input}`. Target language: {self.language}"
                }
            ],
            temperature=self.temperature
        )
        result_text = (
            completion.choices[0].message.content.encode("utf8").decode()
        )
        return result_text
    
class ZhiPuLLM(OnlineLLM):
    def __init__(self,model_path,system_prompt,device):
        """
        实现模型的初始化以及初始参数设定
        """
        self.model_path = model_path
        self.system_prompt = system_prompt
        self.device = device
        self._load_model()

    def _load_model(self):
        raise NotImplementedError("子类必须实现_load_model方法")

    def infer(self, src_text: str) -> str:
        """
        根据初始 system prompt 设定执行推理，返回推理结果
        """
        raise NotImplementedError("子类必须实现infer方法")
        
class DeepSeekLLM(OnlineLLM):
    def __init__(self):
        """
        实现模型的初始化以及初始参数设定
        """
        self.model_path = None
        self.device = None
        self.system_prompt = None
        self._load_model()

    def _load_model(self):
        raise NotImplementedError("子类必须实现_load_model方法")

    def infer(self, src_text: str) -> str:
        """
        根据初始 system prompt 设定执行推理，返回推理结果
        """
        raise NotImplementedError("子类必须实现infer方法")
    
# LocalLLM
os.environ['HF_HOME'] = '../temp/hf-cache'
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from lmdeploy import pipeline, TurbomindEngineConfig,GenerationConfig
class InternLM2(LocalLLM):
    def __init__(self,model_path="",max_batch_size=1,session_len=4096):
        """
        实现模型的初始化以及初始参数设定
        """
        self.model_path = model_path
        self.model = self._load_model(max_batch_size,session_len)

    def _load_model(self,max_batch_size,session_len):
        engine_config = TurbomindEngineConfig(model_format='awq',max_batch_size=max_batch_size,session_len=session_len)
        if self.model_path is not "":
            pipe = pipeline(self.model_path, backend_config=engine_config)
        else:
            pipe = pipeline("internlm/internlm2-chat-7b-4bits", backend_config=engine_config)
        return pipe

    def infer(self,system_prompt, src_text: str,gen_config:GenerationConfig) -> str:
        prompts = [
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': src_text
        }]
        response = self.model(prompts,gen_config)
        return response
    

if __name__ == "__main__":
    pass
    # internLM2
    internLM2 = InternLM2(session_len=2048)
    result = internLM2.infer(system_prompt="你现在是一个翻译专家，请帮我把下列文字翻译成中文，直接给出翻译后结果：",src_text="hello this is my first time to visit here")
    print(result[0].text)
    
