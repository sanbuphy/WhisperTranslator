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
    def __init__(self, model_path: str, system_prompt: str, device:str):
        """
        实现模型的初始化以及初始参数设定
        """
        self.model_path = model_path
        self.system_prompt = system_prompt
        self.device = device
        self.model = self._load_model()

    def _load_model(self):
        openai_key = os.getenv("OPENAI_TOKEN")

    def infer(self, src_text: str) -> str:
        """
        根据初始 system prompt 设定执行推理，返回推理结果
        """
        raise NotImplementedError("子类必须实现infer方法")
    
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
class InternLM2(LocalLLM):
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
    