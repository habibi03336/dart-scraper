import requests
from bs4 import BeautifulSoup

def fetch_content(rcp_no, elem_id, dcm_no):
    res = requests.get(f'https://dart.fss.or.kr/report/viewer.do?rcpNo={rcp_no}&dcmNo={dcm_no}&eleId={elem_id}&offset=1&length=1&dtd=dart3.xsd')
    if res.status_code != 200:
        raise Exception(f'재무제표 {rcp_no} 호출에 실패하였습니다.')
    return BeautifulSoup(res.text, 'html.parser')

def fetch_cover(rcp_no):
    res = requests.get(f'https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcp_no}')
    if res.status_code != 200:
        raise Exception(f'재무제표 {rcp_no} 호출에 실패하였습니다.')
    return BeautifulSoup(res.text, 'html.parser')