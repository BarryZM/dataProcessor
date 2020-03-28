from concurrent.futures import ProcessPoolExecutor
import time
from itertools import chain
import jieba


class Base:
    """
    base class
    """
    def __init__(self, num_worker):
        self.num_worker = num_worker
    
    def _multi_process(self, process_func, iter_list: list) -> list:
        with ProcessPoolExecutor(max_workers = self.num_worker) as executor:
            result = executor.map(process_func, iter_list)
        return list(result)
    
    @staticmethod
    def timer(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            ret = func(*args, **kwargs)
            end = time.time()
            print(f'func \'{func.__name__}\' done in {round(end - start, 3)}s')
            return ret
        return wrapper

    
class BasePassageCleaner(Base):
    """
    to be override _clean_func
    """
    
    def __init__(self, num_worker):
        super(BasePassageCleaner, self).__init__(num_worker)
    
    @Base.timer
    def run(self, passage_list: list):
        cleaned_passages = self._multi_process(self._clean_func, passage_list)
        return cleaned_passages
    
    def _clean_func(self, passage: str) -> str:
        cleaned_passage = passage
        return cleaned_passage

    
class BasePassageSplitter(Base):
    """
    to be override _split_func
    """
    
    def __init__(self, num_worker):
        super(BasePassageSplitter, self).__init__(num_worker)
    
    @Base.timer
    def run(self, passage_list: list):
        splitted_passages = self._multi_process(self._split_func, passage_list)
        splitted_passages = self.reshape(splitted_passages)
        return splitted_passages
    
    def reshape(self, splitted_passages: list) -> list:
        return list(chain(*splitted_passages))
    
    def _split_func(self, passage: str) -> str:
        splitted_passages = passage.split('。')
        return splitted_passages

    
class BaseSentanceCleaner(Base):
    """
    to be override _clean_func
    """
    def __init__(self, num_worker):
        super(BaseSentanceCleaner, self).__init__(num_worker)
    
    @Base.timer
    def run(self, sentance_list: list) -> list:
        passages = self._multi_process(self._clean_func, sentance_list)
        return passages
        
    def _clean_func(self, sentance: str) -> str:
        cleaned_sentance = sentance
        return cleaned_sentance


class Handler(Base):
    """
    the main pipeline
    """
    def __init__(self, num_worker, user_dict=None):
        super(Handler, self).__init__(num_worker)
        self.passage_cleaner = None
        self.passage_splitter = None
        self.sentance_cleaner = None
        if user_dict is not None:
            jieba.load_userdict(user_dict)
    
    @Base.timer
    def init(self, passage_cleaner, passage_splitter, sentance_cleaner):
        self.passage_cleaner = passage_cleaner
        self.passage_splitter = passage_splitter
        self.sentance_cleaner = sentance_cleaner
        print(f'handler initialized')
        
    @Base.timer
    def segment(self, cleaned_sentances: list, use_hmm: bool=False) -> list:
        jieba.enable_parallel(self.num_worker)
        cleaned_sentances = [' '.join(jieba.lcut(i, HMM=use_hmm)) for i in cleaned_sentances]
        jieba.disable_parallel()
        return cleaned_sentances
    
    @Base.timer
    def handle(self, passage_list):
        assert self.passage_cleaner is not None
        assert self.passage_splitter is not None
        assert self.sentance_cleaner is not None 
        cleaned_passages = self.passage_cleaner.run(passage_list)
        splitted_passages = self.passage_splitter.run(cleaned_passages)
        cleaned_sentances = self.sentance_cleaner.run(splitted_passages)
        cleaned_sentances = self.segment(cleaned_sentances)
        return cleaned_sentances
    
class Segmentor:
    def __init__(self, num_worker):
        self.num_worker = num_worker
        
    def segment(self, sentance_list: list) -> list:
        return segment


if __name__ == '__main__':
    passage_list = ['a。b。c。d。f。e','a。b。c。d。f。e','a。b。c。d。f。e']
    passage_cleaner = BasePassageCleaner(3)
    passage_splitter = BasePassageSplitter(3)
    sentance_cleaner = BaseSentanceCleaner(3)
    handler = Handler(3)
    handler.init(passage_cleaner,passage_splitter,sentance_cleaner)
    handler.handle(passage_list)
    print(handler.cleaned_sentance)