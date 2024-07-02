![Alt text](https://i.imgur.com/RhRQLLN.jpg)

# 👀 Convert Photos to PDF file

> You can find video tutorial to build this application [on YouTube](https://youtu.be/nn25oTz8zxE).

> You can find running Demo [here](https://langchain-rag.streamlit.app/)

This application allows users to upload images and convert them to a PDF file.
Images can be added, removed and rearranged.
After clicking 'Create PDF', the file will be created and downloaded automatically.

[![Support](https://img.shields.io/badge/linktree-white?style=for-the-badge&logo=linktree&logoColor=43E55E)](https://linktr.ee/sagib?lt_utm_source=lt_share_link#373198503)
[![Support](https://img.shields.io/badge/Buy_Me_A_Coffee-white?style=for-the-badge&logo=buymeacoffee&logoColor=FFDD00)](https://buymeacoffee.com/sagibar)
[![Support](https://img.shields.io/badge/linkedin-white?style=for-the-badge&logo=linkedin&logoColor=0A66C2)](https://www.linkedin.com/in/sagi-bar-on)
[![Support](https://img.shields.io/badge/whatsapp-white?style=for-the-badge&logo=whatsapp&logoColor=25D366)](https://api.whatsapp.com/send?phone=972549995050)
[![Support](https://img.shields.io/badge/facebook-white?style=for-the-badge&logo=facebook&logoColor=0866FF)](https://www.facebook.com/sagi.baron)
[![Support](https://img.shields.io/badge/email_me-white?style=for-the-badge&logo=gmail&logoColor=EA4335)](mailto:sagi.baron76@gmail.com)

Join my [WhatsApp AI TIPS & TRICKS Channel](https://whatsapp.com/channel/0029Vaj33VkEawds11JP9o1c)

## How it works

The application reads the PDF file and processes the data. It utilizes OpenAI LLMs alongside Langchain to answer your questions. From the results, I used an appropriate response with the help of a LLM.

The application Streamlit creates the graphical user interface (GUI) and utilizes Langchain to interact with the LLM.

## Install dependencies

1. Do the following before installing the dependencies found in `requirements.txt` file because of current challenges installing `onnxruntime` through `pip install onnxruntime`.

   - For MacOS users, a workaround is to first install `onnxruntime` dependency for `chromadb` using:

   ```python
    conda install onnxruntime -c conda-forge
   ```

   See this [thread](https://github.com/microsoft/onnxruntime/issues/11037) for additional help if needed.

   - For Windows users, follow the guide [here](https://github.com/bycloudai/InstallVSBuildToolsWindows?tab=readme-ov-file) to install the Microsoft C++ Build Tools. Be sure to follow through to the last step to set the environment variable path.

2. Install Tesseract [here](https://github.com/UB-Mannheim/tesseract/wiki) is an open source OCR or optical character recognition engine and command line program.

3. Now run this command to install dependencies in the `requirements.txt` file.

```python
pip install -r requirements.txt
```

## Usage

Make sure you have [Streamlit installed](https://docs.streamlit.io/) CLI before running the application. Run the following command in your terminal:

```
streamlit run main.py
```
