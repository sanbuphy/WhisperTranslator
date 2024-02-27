import toml
import os
import pprint
import torch
from tqdm import tqdm
import time
import pysubs2
import re
from pathlib import Path

# 加载配置
config = toml.load('local_whisper_config.toml')
work_dir = config['work_dir']
export_dir = config['export_dir']
file_type = config['file_type']
language = config['language']
model_size = config['model_size']
initial_prompt = config['initial_prompt']
export_srt = config['export_srt']
if_translate = config['if_translate']
target_language = config['target_language']
if_summary = config['if_summary']
is_split = config['is_split']
split_method = config['split_method']
sub_style = config['sub_style']
is_vad_filter = config['is_vad_filter']
set_beam_size = config['set_beam_size']

# 处理过程
my_root_name = work_dir.split('/')[-1]
media_names = []
for root, d_names, f_names in os.walk(work_dir):
    folders = root.split('/')
    for folder in folders:
        if folder.startswith('.'):
            continue
    for d_name in d_names:
        if d_name.startswith('.'):
            d_names.remove(d_name)
    for f_name in f_names:
        # if f_name.startswith('.'):
        #     f_names.remove(f_name)
        # only add media files
        if f_name.lower().endswith(
            ('mp3', 'm4a', 'flac', 'aac', 'wav', 'mp4', 'mkv', 'ts', 'flv')):
            media_names.append(f_name)

if not os.path.exists(export_dir):
    os.makedirs(export_dir)

pprint.pprint(media_names)
print("待处理文件数：", len(media_names))
choice = input("请检查待处理文件是否正确，若错误清重新检查配置（y/n）\n Please verify if the files to be processed are correct. If incorrect, please recheck the configuration (y/n).")
if choice.lower() != "y":
    exit()

# 处理环节
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HOME'] = './temp/hf-cache'
from faster_whisper import WhisperModel


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


print('开始转录，请等待...')

file_names = media_names
file_basenames = []
for i in range(len(file_names)):
    file_basenames.append(Path(file_names[i]).stem)
output_dir = Path(export_dir).parent.resolve()

for i in range(len(file_names)):
    torch.cuda.empty_cache()
    whisper_model = WhisperModel(model_size)
    torch.cuda.empty_cache()
    file_name = file_names[i]
    #Transcribe
    file_basename = file_basenames[i]
    if file_type == "video":
        print('提取音频中 Extracting audio from video file...')
        os.system(
            f'ffmpeg -i {file_name} -f mp3 -ab 192000 -vn {file_basename}.mp3')
        print('提取完毕 Done.')

    tic = time.time()
    print('识别中 Transcribe in progress...')

    segments, info = whisper_model.transcribe(
        audio=f'{Path(work_dir) / file_name}',
        beam_size=set_beam_size,
        language=language,
        vad_filter=is_vad_filter,
        initial_prompt=initial_prompt,
        vad_parameters=dict(min_silence_duration_ms=1000))

    # segments is a generator so the transcription only starts when you iterate over it
    # to use pysubs2, the argument must be a segment list-of-dicts
    total_duration = round(info.duration,
                           2)  # Same precision as the Whisper timestamps.
    results = []
    pure_texts = []

    with tqdm(total=total_duration, unit=" seconds") as pbar:
        for s in segments:
            segment_dict = {'start': s.start, 'end': s.end, 'text': s.text}
            results.append(segment_dict)
            if language == 'zh':
                # 用于中文情况断句，否则没有标点符号。
                if not s.text.endswith(tuple([',', '.', '，', '。'])):
                    pure_texts.append(s.text + ',')
                else:
                    pure_texts.append(s.text)
            else:
                pure_texts.append(s.text)
            segment_duration = s.end - s.start
            pbar.update(segment_duration)
    full_text = ''.join(pure_texts)

    #Time comsumed
    toc = time.time()
    print('识别完毕 Done')
    print(f'Time consumpution {toc-tic}s')
    del whisper_model
    torch.cuda.empty_cache()

    if if_translate or if_summary:
        from whispertranslator.llm import InternLM2,GenerationConfig
        internLM2 = InternLM2(session_len=8096)
        gen_config = GenerationConfig(top_k=20,top_p=0.3,temperature=0.1)
        translator_system_prompt = f"""
            把下列文字翻译成{target_language},修改和补充语序让他更符合{target_language}习惯，只返回给我结果：
            """
        summary_system_prompt = f"""
            用{target_language}总结下列文字的主题：
            """
        
    # get translated texts for srt ass file
    if if_translate:
        translate_results = []
        for i in results:
            translate_text = internLM2.infer(translator_system_prompt,i['text'].replace(' ',''),gen_config)
            translate_segment_dict = {
                'start': i['start'],
                'end': i['end'],
                'text': i['text'] + r"\\N" + translate_text.text.split('\n')[-1]
            }
            translate_results.append(translate_segment_dict)

    #Save full text
    new_paragraphs = split_text(full_text, max_word_count=200)
    chunk_filename = file_basename + '.txt'

    chunk_filename = Path(export_dir) / chunk_filename
    with open(chunk_filename, 'w', encoding='utf-8') as file:
        for chunk in new_paragraphs:
            file.write(chunk + '\n')

    if if_translate:
        translate_filename = file_basename + '_translate' + '.txt'
        translate_filename = Path(export_dir) / translate_filename
        with open(translate_filename, 'w', encoding='utf-8') as file:
            for chunk in new_paragraphs:
                chunk = chunk.replace("\n", ".")
                chunk_translate = internLM2.infer(translator_system_prompt,f"{chunk}" ,gen_config)
                chunk_translate.text = chunk_translate.text.replace(" ", "") # 去除空格
                if chunk_translate.text.count(chunk_translate.text[-4:]) > 10:
                    print("出现重复！")
                    chunk_translate = internLM2.infer(translator_system_prompt,f"{chunk}" ,gen_config)
                print(chunk, '\n' ,chunk_translate.text.split('\n')[-1])
                file.write(
                    chunk_translate.text.split('\n')[-1] +'\n')

    #Save srt
    subs = pysubs2.load_from_whisper(results)
    srt_filename = file_basename + '.srt'
    srt_filename = Path(export_dir) / srt_filename
    subs.save(srt_filename)

    if if_translate:
        translate_subs = pysubs2.load_from_whisper(translate_results)
        translate_srt_filename = file_basename + '_translate' + '.srt'
        translate_srt_filename = Path(export_dir) / translate_srt_filename
        translate_subs.save(translate_srt_filename)

    #Save ass
    from srt2ass import srt2ass
    ass_filename = srt2ass(str(srt_filename), sub_style, is_split,
                           split_method)

    if if_translate:
        translate_ass_filename = srt2ass(str(translate_srt_filename),
                                         sub_style, is_split, split_method)

    print('ASS subtitle saved as: ' + ass_filename)
    print('文件字幕生成完毕/ file(s) was completed!')
    if if_summary:
        with open(translate_filename, 'r', encoding='utf-8') as file:
            content = file.read()
            summary_text = internLM2.infer(summary_system_prompt,str(content).replace(' ','').replace('\n',''),gen_config).text 
            print("总结结果：",summary_text)
            content = summary_text + '\n\n' + content
        with open(translate_filename, "w") as file:
            file.write(content)
    import gc
    if if_translate or if_summary:
        del internLM2
    gc.collect()
    torch.cuda.empty_cache()

print('所有字幕生成完毕 All done!')
