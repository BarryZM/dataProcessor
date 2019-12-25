# -*- coding: utf-8 -*-
# -*- author: JeremySun -*-
# -*- dating: 19/12/23 -*-

# 模块导入
import re
import os
import time
from functools import wraps
from tqdm import tqdm
from pyltp import SentenceSplitter

# ltp模型目录路径
LTP_DATA_DIR = "D:/PyLTP/ltp_data"

# 数据读取
# test = open('../testClean.txt', 'r', encoding='utf-8').readlines()

# 数据导入
def batch_file(path, file_list):
    for file in os.listdir(path):
        fs = os.path.join(path, file)
        if os.path.isfile(fs):
            file_list.append(fs)
        elif os.path.isdir(fs):
            batch_file(fs, file_list)
    return file_list

# 匹配网页标签
def loss_html(text):
    pattern_tag = re.compile('</?\w+[^>]*>')  # HTML标签
    text_html = re.sub(pattern=pattern_tag, repl='', string=str(text))
    return text_html


# 匹配标签
def loss_label(text):
    pattern_img = re.compile(r"<(img|IMG)(.*?)(/>|></img>|>)")
    text_img = re.sub(pattern=pattern_img, repl='', string=str(text))
    pattern_video = re.compile(r'<(video)(.*?)(/>|></video>|>)')
    text_video = re.sub(pattern=pattern_video, repl='', string=str(text_img))
    pattern_src = re.compile(r"(src|SRC)=(\"|\')(.*?)(\"|\')")
    text_src = re.sub(pattern=pattern_src, repl='', string=str(text_video))
    pattern_div = re.compile(r'/<div(([\s\S])*?)<\/div>/g')
    text_div = re.sub(pattern=pattern_div, repl='', string=str(text_src))
    pattern_span = re.compile(r"<(span)(.*?)(/>|></span>|>)")
    text_span = re.sub(pattern=pattern_span, repl='', string=str(text_div))
    pattern_again = re.compile(r'</span>')
    text_span_again = re.sub(pattern=pattern_again, repl='', string=str(text_span))
    pattern_p1 = re.compile(r'<(p)(.*?)(/>|></p>|>)')
    text_p1 = re.sub(pattern=pattern_p1, repl='', string=str(text_span_again))
    pattern_p2 = re.compile(r'(</p>)')
    text_p2 = re.sub(pattern=pattern_p2, repl='', string=str(text_p1))
    pattern_p3 = re.compile(r'(<p)')
    text_p3 = re.sub(pattern=pattern_p3, repl='', string=str(text_p2))
    return text_p3


# 匹配邮箱
def loss_mail(text):
    pattern_mail = re.compile('[\w]+(\.[\w]+)*@[\w]+(\.[\w])+')
    text_mail = re.sub(pattern=pattern_mail, repl='', string=str(text))
    return text_mail


# 匹配特殊标点
def loss_other(text):
    pattern_other = re.compile(r'[\u4e00-\u9fa5]|[\u0030-\u0039]|[\u0041-\u005a]|[\u0061-\u007a]|[,，。 \.;\'：/\\:\/!！？?]|[\s]]')
    text_other = re.findall(pattern=pattern_other, string=str(text))
    text_other = ''.join(text_other)
    return text_other


# 匹配网址
def loss_url(text):
    pattern_url1 = re.compile(r'(https?|ftp|file|img3):\/\/[a-z0-9_.:]+\/[-a-z0-9_:@&?=+,.!/~*%$]*(\.(html|htm|shtml))?')
    pattern_url2 = re.compile(r'^https?:\/\/([^/:]+)(:(\d)+)?(/.*)?$')
    pattern_url3 = re.compile(r'^([a-z0-9]\.|[a-z0-9][-a-z0-9]{0,61}[a-z0-9]\.)(com|edu|gov|int|mil|net|org|biz|info|name|museum|coop|aero|[a-z][a-z])$')
    pattern_url4 = re.compile(r'(登录|网|网站|网站是|网址|网址是|平台|点击|店|地址|微信公众号|微信号|微信|微信号是|公众号|公众号是)[A-Z.a-z.0-9]{1,100}')
    pattern_url5 = re.compile(r'(https?|ftp|file|img3)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
    pattern_url6 = re.compile(r'(www.)[a-zA-Z0-9\-\.]+')
    pattern_url7 = re.compile(r'(登录：|网：|网站：|网站是：|网址：|网址是：|点击：|店：|微信公众号：|微信号：|微信：|微信号是：|公众号：|公众号是)[A-Z.a-z.0-9]{1,100}')
    pattern_url8 = re.compile(r'(登录:|网:|网站:|网站是:|网址:|网址是:|点击:|店:|微信公众号:|微信号:|微信:|微信号是:|公众号:|公众号是)[A-Z.a-z.0-9]{1,100}')
    text_url1 = re.sub(pattern=pattern_url1, repl='', string=str(text))
    text_url2 = re.sub(pattern=pattern_url2, repl='', string=str(text_url1))
    text_url3 = re.sub(pattern=pattern_url3, repl='', string=str(text_url2))
    text_url4 = re.sub(pattern=pattern_url4, repl='', string=str(text_url3))
    text_url5 = re.sub(pattern=pattern_url5, repl='', string=str(text_url4))
    text_url6 = re.sub(pattern=pattern_url6, repl='', string=str(text_url5))
    text_url7 = re.sub(pattern=pattern_url7, repl='', string=str(text_url6))
    text_url = re.sub(pattern=pattern_url8, repl='', string=str(text_url7))
    return text_url


# 匹配网址
def clean_url(text):
    pattern_in = re.compile(r'（网.*?）')
    corpus_in = re.sub(pattern=pattern_in, repl='', string=str(text))
    pattern_out = re.compile(r'网（.*?）')
    corpus_out = re.sub(pattern=pattern_out, repl='', string=str(corpus_in))
    pattern_none = re.compile(r'网站\s.*?）')
    corpus_none = re.sub(pattern=pattern_none, repl='', string=str(corpus_out))
    pattern_sim = re.compile(r'网址\s.*?）')
    corpus_sim = re.sub(pattern=pattern_sim, repl='', string=str(corpus_none))
    return corpus_sim


# 匹配连续英文
def loss_continue(text):
    pattern_continue = re.compile(r'[A-Za-z ]{13,100}')
    text_continue = re.sub(pattern=pattern_continue, repl=' ', string=str(text))
    return text_continue



# 匹配特定单词
def loss_word(text):
    pattern_word = re.compile(r'htm|chinatimesnetcn|start|http|w w w|h t t p|-|\xa0|\u3000|\r|\t|\n|html|nbsp|video|videobr|epdm|br|alt|img|ref|picType1|imageUrl|divclass|high34|normal34|0datavid|div')
    text_word = re.sub(pattern=pattern_word, repl='', string=str(text))
    return text_word


# 匹配逗号
def loss_comma(text):
    pattern_comma = re.compile(r"[，,：:]")  # 加：:
    text_comma = re.sub(pattern=pattern_comma, repl='。', string=str(text))
    return text_comma


# 去掉空行
def delBlankline(infile, outfile):
    infopen = open(infile, 'r', encoding="utf-8")
    outfopen = open(outfile, 'w', encoding="utf-8")
    lines = infopen.readlines()
    for line in lines:
        if line.split():
            outfopen.writelines(line)
        else:
            outfopen.writelines("")
    infopen.close()
    outfopen.close()


# 定义timer
def func_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        print('[Function: {name} start...]'.format(name=function.__name__))
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print('[Function: {name} finished, spent time: {time:.2f}s]'.format(name=function.__name__, time=t1 - t0))
        return result
    return function_timer


# 定义main()函数
@func_timer
def main():
    file_list = []
    path = r'C:\Users\JeremySun\Desktop\Internship\Project02_corpusProcessor\english_folder'
    file_path = batch_file(path=path, file_list=file_list)
    for path in file_path:
        english_text_connect = open(path, encoding='utf-8').readlines()
        assetPath_loss_html = loss_html(text=english_text_connect)
        assetPath_loss_label = loss_label(text=assetPath_loss_html)
        assetPath_loss_mail = loss_mail(text=assetPath_loss_label)
        assetPath_loss_other = loss_other(text=assetPath_loss_mail)
        assetPath_loss_url = loss_url(text=assetPath_loss_other)
        assetPath_clean_url = clean_url(text=assetPath_loss_url)
        assetPath_loss_continue = loss_continue(text=assetPath_clean_url)
        assetPath_loss_word = loss_word(text=assetPath_loss_continue)
        assetPath_loss_comma = loss_comma(text=assetPath_loss_word)

        # 分句
        english_text_sentence = SentenceSplitter.split(assetPath_loss_comma)

        # 去掉其余符号并写入文件
        pattern_all = re.compile(r"[。.；;？?!！:：]")  # 加：:
        pattern_last = re.compile(r'[a-zA-Z0-9]{13,}')
        f = open("english_text_sent_pre.txt", 'a', encoding='utf-8')
        for i in tqdm(english_text_sentence):
            if len(i) <= 100:
                i = re.sub(pattern=pattern_all, repl=' ', string=i)
                i = re.sub(pattern=pattern_last, repl='', string=i)
                f.write(i.strip() + '\n')
        f.close()

        # delBlankline("english_text_filtered_pre.txt", "english_cleaned.txt")



if __name__ == '__main__':
    """
    代码执行结果包含\n等标签
    """
    main()