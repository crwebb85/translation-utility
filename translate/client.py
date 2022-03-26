from pathlib import Path
import re
import time
import pyautogui
import pyperclip
from pywinauto.application import Application
from tqdm import tqdm

def get_paragraphs(fileobj, separator='\n'):
    if separator[-1:] != '\n': separator += '\n'
    paragraph = []
    for line in fileobj:
        if line == separator:
            if paragraph:
                yield ''.join(paragraph)
                paragraph = []
        else:
            paragraph.append(line)
    if paragraph: yield ''.join(paragraph)

def isJapanesse(text):
    pattern = r'(.*)([\u4e00-\u9fff\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF\u3200-\u32FF]+?)(.*)'
    return bool(re.match(pattern, text))

def copy_clipboard():
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.01)  # ctrl-c is usually very fast but your program may execute faster
    return pyperclip.paste()

def copy_translation():
    translation = ''
    for attempt in range(20):
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        translation = copy_clipboard()
        if not isJapanesse(translation):
            return translation
    return translation 

def translate_paragraph(paragraph):
    pyperclip.copy(paragraph)
    pyautogui.moveTo(100, 200)
    pyautogui.click()
    time.sleep(.01)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(.01)
    pyautogui.hotkey('del')
    time.sleep(.01)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(.01)
    (width, height) = pyautogui.size() 
    pyautogui.moveTo(width-100, 200)
    translation = copy_translation()
    return translation

def translate(input_path: Path, output_path: Path, deepl_executable_path: Path):
    app = Application().start(str(deepl_executable_path.absolute()))
    time.sleep(1)
    with open(input_path, 'r', encoding = 'utf-8') as input_file, open(output_path,'w', encoding = 'utf-8') as output_file :
        paragraphs = [paragraph for paragraph in get_paragraphs(input_file)]
        for paragraph in tqdm(paragraphs):
            translation = translate_paragraph(paragraph)
            for line in translation.splitlines():
                output_file.write(line)
                output_file.write('\n')
            output_file.write('\n')