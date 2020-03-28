from lm_corpus_processor_base import * 

import jieba 
import re

class PassageCleaner(BasePassageCleaner):
    def __init__(self, num_worker):
        super(PassageCleaner, self).__init__(num_worker)
    
    @staticmethod
    def remove_html(sentance: str) -> str:
        re_tag = re.compile('</?\w+[^>]*>')  # HTML标签
        new_text = re.sub(re_tag, '', sentance)
        new_text = re.sub(",+", ",", new_text)   # 合并逗号
        new_text = re.sub(" +", " ", new_text)   # 合并空格
        new_text = re.sub("[...|…|。。。]+", "...", new_text)  # 合并句号
        new_text = re.sub("-+", "--", new_text)  # 合并-
        new_text = re.sub("———+", "———", new_text)  # 合并-
        return new_text

    def _clean_func(self, passage):
        self.remove_html(passage)
        return passage
    

class PassageSplitter(BasePassageSplitter):
    def __init__(self, num_worker):
        super(PassageSplitter, self).__init__(num_worker)
        
    def _split_func(self, passage):
        passage = re.sub('([；，。！？\?])([^”’])', r"\1\n\2", passage)  # 单字符断句符
        passage = re.sub('(\.{6})([^”’])', r"\1\n\2", passage)  # 英文省略号
        passage = re.sub('(\…{2})([^”’])', r"\1\n\2", passage)  # 中文省略号
        passage = re.sub('([；，。！？\?][”’])([^，。！？\?])', r'\1\n\2', passage)
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        passage = passage.rstrip()  # 段尾如果有多余的\n就去掉它
        return passage.split("\n")


class SentanceCleaner(BaseSentanceCleaner):
    def __init__(self, num_worker, user_dict_file=None):
        super(SentanceCleaner, self).__init__(num_worker)

    @staticmethod
    def remove_other(sentance):
        def is_chinese(uchar):
            """判断一个unicode是否是汉字"""
            if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
                return True
            else:
                return False

        def is_number(uchar):
            """判断一个unicode是否是数字"""
            if uchar >= u'\u0030' and uchar <= u'\u0039':
                return True
            else:
                return False

        def is_alphabet(uchar):
            """判断一个unicode是否是英文字母"""
            if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
                return True
            else:
                return False
        content_str = ''
        for i in sentance:
            if is_chinese(i) | is_number(i) | is_alphabet(i):
                content_str = content_str+i

        return content_str
            
    def _clean_func(self, sentance):
        #sentance = sentance
        sentance = self.remove_other(sentance)
        return sentance


if __name__ == '__main__':
    handler = Handler(3)
    passage_list = 100*['我爱北京天安门，天安门上太阳升。伟大领袖毛主席，指引我们向前进。','我爱北京天安门，天安门上太阳升。伟大领袖毛主席，指引我们向前进。','我爱北京天安门，天安门上太阳升。伟大领袖毛主席，指引我们向前进。']
    pc = PassageCleaner(3)
    ps = PassageSplitter(3)
    sc = SentanceCleaner(3)
    handler.init(pc,ps,sc)
    c = handler.handle(passage_list)
    print(c[:10])






