import os
from lmdeploy import pipeline, TurbomindEngineConfig
os.environ['HF_HOME'] = '../temp/hf-cache'
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 提前预分配显存
engine_config = TurbomindEngineConfig(model_format='awq', max_batch_size=1, session_len=4096)
pipe = pipeline("internlm/internlm2-chat-7b-4bits", backend_config=engine_config)

input_text = """
请你自我介绍
"""

response = pipe([input_text])
print(response)