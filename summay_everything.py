# 使用 internLM2 总结文件，格式化输出到目标位置
import re
import os
from pathlib import Path
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HOME'] = './temp/hf-cache'
from whispertranslator.llm import InternLM2
from lmdeploy import GenerationConfig

def split_text(text, max_word_count):
    def count_words(text):
        words = re.findall(r'\b\w+\b', text)
        return len(words)

    sentences = re.split(r'(?<=[,.])\s', text)  # 按照逗号和句号分割文本
    new_paragraphs = []
    current_paragraph = ''
    current_word_count = 0

    for sentence in sentences:
        sentence_word_count = count_words(sentence)
        if current_word_count + sentence_word_count <= max_word_count:
            current_paragraph += sentence + ' '
            current_word_count += sentence_word_count
        else:
            if current_word_count > 0:
                new_paragraphs.append(current_paragraph.strip())
            current_paragraph = sentence + ' '
            current_word_count = sentence_word_count

    if current_paragraph != '':
        new_paragraphs.append(current_paragraph.strip())

    return new_paragraphs

internLM2 = InternLM2(session_len=8096)
gen_config = GenerationConfig(top_k=20,top_p=0.3,temperature=0.1)

translator_system_prompt = """
    把下列文字翻译成中文,修改和补充语序让他更符合中文习惯，只返回给我结果：
    """
summary_system_prompt = f"""
    总结下列文字的主题，分点阐述：
    """

if __name__ == "__main__":
    # 只需要修改这些内容
    src_path = ""
    export_dir = ''

    with open(src_path,'r') as file:
        full_text = file.read()

    new_paragraphs = split_text(full_text, max_word_count=200)

    translate_filename = os.path.basename(src_path) + '_translate_new' + '.txt'
    translate_filename = Path(export_dir) / translate_filename

    with open(translate_filename, 'w', encoding='utf-8') as file:
        for chunk in new_paragraphs:
            chunk_translate = internLM2.infer(translator_system_prompt,f"{chunk}" ,gen_config)
            chunk_translate[0].text = chunk_translate[0].text.replace(" ", "") # 去除空格
            if chunk_translate[0].text.count(chunk_translate[0].text[-4:]) > 10:
                print("出现重复！")
                chunk_translate = internLM2.infer(translator_system_prompt,f"{chunk}" ,gen_config)
            print(chunk, '\n' ,chunk_translate[0].text.split('\n')[-1])
            file.write(
                chunk_translate[0].text.split('\n')[-1] +'\n')
            
    with open(translate_filename, 'r') as file:
        content = file.read()
        summary_text = internLM2.infer(summary_system_prompt,str(content).replace(' ','').replace('\n',''),gen_config)[0].text 
        print("总结结果：",summary_text)
        content = summary_text + '\n\n' + content

    with open(translate_filename, "w") as file:
        file.write(content)
