# WhisperTranslator

Language : [English](./README.md)  | 简体中文

WhisperTranslator 是基于 [N46Whisper](https://github.com/Ayanaminn/N46Whisper) 的应用。开发初衷旨在提高各类外文视频的转录、翻译、总结效率。

此应用基于AI语音识别模型 [Whisper](https://github.com/openai/whisper)的优化部署 [faster-whisper](https://github.com/guillaumekln/faster-whisper).

应用输出文件为ass或srt格式，内置指定字幕组的字幕格式，可直接导入 [Aegisub](https://github.com/Aegisub/Aegisub) 进行后续翻译及时间轴校正。你可以根据选项决定是否启动全文摘录和总结。


## 最近更新:

2024.2.24:
- 支持本地大模型，使用[InternLM2 7B](https://github.com/InternLM/InternLM)自动翻译时间轴、翻译全文、总结全文。你只需要在一个 12G 显存的显卡上就可以运行`WhisperTranslator_local.py`的所有操作。

2024.2.20:
* release初版，提供转录和输出为分割文章。


## 环境安装

- 如果你在本地运行，则需要运行 `pip install -r requirements.txt` 安装依赖,如果你想运行本地大模型进行翻译、总结工作，你需要额外安装大模型依赖 `pip install -r requirements_localllm.txt`

## 如何使用

- 基于本地的使用（推荐）：

    - 仅转录不翻译总结只需要6G的显存，若体验完整功能需要12G显存的显卡（ampere架构，也就是3060类的显卡），然后修改请修改配置文件 `local_whisper_config.toml`，接着直接挂机运行`WhisperTranslator_local.py`即可

    - 运行结束后你可以得到：1、字幕文件和全文 2、翻译后的字幕文件和全文 3、全文摘要，当前默认放在翻译后的全文文件中

    - 你可以根据需要选择是否开启翻译总结功能，具体请查看配置

- 基于Google Colab的使用：

    - [点击这里](https://colab.research.google.com/github/sanbuphy/WhisperTranslator/blob/main/WhisperTranslator_colab.ipynb) 在Google Colab中打开应用.
    - 上传要识别的文件并运行应用
    - 识别完成后ass文件会自动下载到本地.

- 有关AI功能的使用（可选）：

    - 如果你选择了AI相关工具（AI翻译、AI总结），且使用的是online的api，则你需要按照不同的token命名写入到当前文件夹的`.env`文件夹下，其中各环境变量命名方式参考下列方式（约定为下列命名）：
    ```
    OPENAI_API_KEY=
    OPENAI_API_BASE=
    ZHIPUAI_API_KEY=
    BAIDU_API_KEY=
    ```

    - 如果你使用的是local的AI工具，只需要等待模型下载完成后运行即可。

- 我只想使用本地大模型翻译和总结一个外国文章：

    - 本项目提供了单独运行翻译和总结功能，不需要转录，你只需要修改 `summay_everything.py` 的原始文件和输出文件地址，并运行即可。

## AI翻译

应用现在可以使用AI翻译工具对转录的文本进行逐行翻译。

用户也可以单独上传srt或ass文件来使用翻译模块。

目前支持 InternLM2 的翻译

翻译后的文本将于原文合并在一行，以 `/N`分割，生成双语对照字幕。

例如: 

![QQ截图20230312155700](https://user-images.githubusercontent.com/49441654/224525469-18a43cbc-33b9-4b2f-b7ca-7ae0c1865b17.png)

双语字幕效果为:

![QQ截图20230312160015](https://user-images.githubusercontent.com/49441654/224525526-51e2123c-6e1c-427c-8d67-9ccd4a7e6630.png)

用户需要自己的OpenAI API Key来使用翻译功能. 要生成免费的Key，进入自己账户设定 https://platform.openai.com/account/api-keys

## 对字幕的自动分行
当一行中有若干句话时，用户可选择按空格分割成多行。分割后的若干行均临时采用原行相同的时间戳，且添加了adjust_required标记提示调整时间戳避免叠轴。

普通分割只有在单（词）句字符长度大于5时才进行分割：
分割前：

![No](https://user-images.githubusercontent.com/49441654/225230578-2977511d-324f-463f-b783-fa9251df8e9f.PNG)

分割后：

![Modest](https://user-images.githubusercontent.com/49441654/225230645-efe8b26a-3392-4234-ad3f-f9b8d4e95d10.PNG)

可以看到，尤其以第7行为例，短句和语气词被保留，只有长句被分割。字符长度5为默认值，一般来说日语大部分短句和语气词都可以过滤掉。

全面分割则是对任何空格都另起一行，分割后：

![Aggre](https://user-images.githubusercontent.com/49441654/225231063-3e60561b-a821-4c61-8c8e-4ce53e6c1a12.PNG)


此外可以看到，在两种情况下英文单字都不会被分割。
