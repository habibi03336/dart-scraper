import abc

class MetaScraper(abc.ABC):
    @abc.abstractclassmethod
    def __init__(self, html):
        pass

    @abc.abstractclassmethod
    def dcm_no(self):
        pass

    @abc.abstractclassmethod
    def elem_id(self, index_name):
        pass

    @abc.abstractclassmethod
    def elem_index_id(self, index_name):
        pass

    @abc.abstractclassmethod
    def finance_elem_id(self):
        pass