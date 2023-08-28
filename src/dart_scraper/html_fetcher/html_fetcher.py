import abc

class HtmlFetcher(abc.ABC):
    @abc.abstractclassmethod
    def fetch_cover(rcp_no):
        pass

    @abc.abstractclassmethod
    def fetch_content(rcp_no, elem_id, dcm_no):
        pass
