from .html_fetcher import HtmlFetcher
from bs4 import BeautifulSoup
from .utils import get_random_user_agent, get_random
import requests

class HtmlFetcherImpl(HtmlFetcher):
    try_limit = 3
    def __init__(self, proxies, try_limit):
        self.proxies = proxies
        self.try_limit = try_limit if try_limit else self.try_limit

    def fetch_cover(self, rcp_no):
        res = self._do_sneaky_request(f'https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcp_no}')
        if not res or res.status_code != 200:
            raise Exception(f'재무제표 {rcp_no} 호출에 실패하였습니다.')
        return BeautifulSoup(res.text, 'html.parser')
    
    def fetch_content(self, rcp_no, elem_id, dcm_no):
        res = self._do_sneaky_request(f'https://dart.fss.or.kr/report/viewer.do?rcpNo={rcp_no}&dcmNo={dcm_no}&eleId={elem_id}&offset=1&length=1&dtd=dart3.xsd')
        if res.status_code != 200:
             raise Exception(f'재무제표 {rcp_no}의 {elem_id} 목차 호출에 실패하였습니다.')
        return BeautifulSoup(res.text, 'html.parser')

    def _do_sneaky_request(self, url):
        if not self.proxies:
            return requests.get(url)
            
        for i in range(HtmlFetcherImpl.try_limit):
            try:
                proxy_ip = get_random(self.proxies)
                proxies = {'http': proxy_ip, 'https': proxy_ip}
                user_agent = get_random_user_agent()
                headers = {"User-Agent" : user_agent }
                res = requests.get(url, headers=headers, proxies=proxies) 
                return res
            except BaseException as e:
                if i == HtmlFetcherImpl.try_limit-1:
                   raise e
    