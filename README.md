# WhisperTranslator

Language: [English](./README.md) | [简体中文](./README_CN.md)

WhisperTranslator is an application based on [N46Whisper](https://github.com/Ayanaminn/N46Whisper), aimed at improving the efficiency of transcription, translation, and summarization for various foreign language videos.

This application utilizes the optimized deployment of the AI speech recognition model [Whisper](https://github.com/openai/whisper), known as [faster-whisper](https://github.com/guillaumekln/faster-whisper).

The output files are in ass or srt format, preformatted for a specific subtitle group, and can be directly imported into [Aegisub](https://github.com/Aegisub/Aegisub) for further translation and timing adjustments. You have the option to enable full text extraction and summarization.

## Feature

⭐ Converting videos and audio into corresponding language text.

⭐ Translating transcribed text into any language (using local large models).

⭐ Outputting full text and timeline captions after transcription.

⭐ Summarizing the full content of videos (using local large models).

## Recent Updates:

- 2024.2.24:
  - 🤗Added support for local large models; now using [InternLM2 7B](https://github.com/InternLM/InternLM) to automatically translate ass and srt, entire texts, and summarize them. All operations can be run with just a 12GB GPU by executing `WhisperTranslator_local.py`.

- 2024.2.20:
  * Initial release, providing transcription and segmented article output.

## Environment Setup

- If running locally, execute `pip install -r requirements.txt` to install dependencies. To **run local large models for translation and summarization**, you need to install additional dependencies with `pip install -r requirements_localllm.txt`.

## How to Use

### Local Usage (Recommended):

- Transcription alone requires only 6GB of VRAM; for full functionality, which includes translation and summarization, you'll need a 12GB VRAM GPU (ampere architecture, e.g., similar to a 3060 series). Modify the configuration file [local_whisper_config.toml](local_whisper_config.toml), then simply run [WhisperTranslator_local.py](WhisperTranslator_local.py) using Python.

- After completion, you'll get: 1. Subtitles and full text, 2. Translated subtitles and full text, and 3. A full-text summary, which is currently embedded within the translated full-text file by default.

- You can choose to enable or disable translation and summarization features according to your needs; refer to the configuration for details.

### Google Colab Usage:

- [Click here](https://colab.research.google.com/github/sanbuphy/WhisperTranslator/blob/main/WhisperTranslator_colab.ipynb) to open the application in Google Colab.
- Upload the file to transcribe and run the application.
- The ass file will automatically download after successful transcription.

### AI Features (Optional):

- If you choose to use AI tools (AI translation, AI summarization) that rely on online APIs, you need to write API tokens into the `.env` file in the current folder using the following variable names:
    ```
    OPENAI_API_KEY=
    OPENAI_API_BASE=
    ZHIPUAI_API_KEY=
    BAIDU_API_KEY=
    ```

- If you're using local AI tools, simply wait for the models to download and then run the application.

### Translating with Only the Local Large Model:

- This project provides standalone translation and summarization capabilities without requiring transcription. Simply modify the input and output file addresses in `summay_everything.py` and run it.

## AI Translation

The application can now perform line-by-line translation of transcribed texts using AI translation tools.

Users can also upload individual srt or ass files to use the translation module.

Currently supports translation with InternLM2.

Translated texts are merged with the original on the same line separated by `/N`, creating bilingual subtitles.

Example images: 

[![](https://user-images.githubusercontent.com/49441654/224525469-18a43cbc-33b9-4b2f-b7ca-7ae0c1865b17.png)](https://user-images.githubusercontent.com/49441654/224525469-18a43cbc-33b9-4b2f-b783-7ae0c1865b17.png)

[![](https://user-images.githubusercontent.com/49441654/224525526-51e2123c-6e1c-427c-8d67-9ccd4a7e6630.png)](https://user-images.githubusercontent.com/49441654/224525526-51e2123c-6e1c-427c-8d67-9ccd4a7e6630.png)

Users require their OpenAI API Key to use the translation feature. To generate a free Key, visit your account settings at https://platform.openai.com/account/api-keys.

## Automatic Line Breaking for Subtitles

When there are multiple sentences in one line, users can choose to split them into separate lines by spaces. The temporary timestamps for these new lines are the same as the original line, marked with 'adjust_required' to indicate the need for adjusting timestamps to avoid overlapping.

Regular splitting occurs only when single-word or single-sentence characters exceed 5 in length:
Before Splitting:

[![](https://user-images.githubusercontent.com/49441654/225230578-2977511d-324f-463f-b783-fa9251df8e9f.PNG)](https://user-images.githubusercontent.com/49441654/225230578-2977511d-324f-463f-b783-fa9251df8e9f.PNG)

After Splitting:

[![](https://user-images.githubusercontent.com/49441654/225230645-efe8b26a-3392-4234-ad3f-f9b8d4e95d10.PNG)](https://user-images.githubusercontent.com/49441654/225230645-efe8b26a-3392-4234-ad3f-f9b8d4e95d10.PNG)

As seen, particularly in line 7, short phrases and interjections are preserved while long sentences are split. The character length limit of 5 is default, generally filtering out most short phrases and interjections in Japanese.

Comprehensive splitting creates a new line for every space, resulting in:

[![](https://user-images.githubusercontent.com/49441654/225231063-3e60561b-a821-4c61-8c8e-4ce53e6c1a12.PNG)](https://user-images.githubusercontent.com/49441654/225231063-3e60561b-a821-4c61-8c8e-4ce53e6c1a12.PNG)

In both cases, English single words are not split.
