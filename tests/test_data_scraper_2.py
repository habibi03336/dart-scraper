from dart_scraper import DataScraper
from util.html_fetcher_for_test import fetch_content

def retrieve_meta(url):
    params = url.split("?")[1]
    params = params.split('&')
    answer = dict()
    for param in params:
        k, v = param.split("=")
        answer[k] = v
    return answer['rcpNo'], answer['dcmNo'], answer['eleId']

class TestDataScraper2:

    def test_실패케이스(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20230811002311&dcmNo=9385300&eleId=21&offset=569032&length=51747&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2023-2'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == 100_804_535_723
        assert data_scraper.retreive_operating_profit() == 13_905_376_051
        assert data_scraper.retreive_net_profit() == 9_631_149_133
        assert data_scraper.retreive_equity() == 171_456_398_651
        assert data_scraper.retreive_debt() == 97_111_961_827
        assert data_scraper.retreive_cash() == 33_230_181_489

    def test_실패케이스_20240506(self):
        # 재무제표 부제목인 '재무상태표'가 누락되어있는 경우. 종종 이런 케이스가 있음
        # 재무제표 가장 첫 섹션은 재무상태표라고 가정하도록 수정 
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20230814002977&dcmNo=9394635&eleId=21&offset=1099519&length=122660&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2023-2'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == 813_079_000_000
        assert data_scraper.retreive_operating_profit() == 54_454_000_000
        assert data_scraper.retreive_net_profit() == 45_153_000_000
        assert data_scraper.retreive_equity() == 1_259_941_000_000
        assert data_scraper.retreive_debt() == 10_280_972_000_000
        assert data_scraper.retreive_cash() == 912_235_000_000

    def test_실패케이스_20240506_2(self):
        # 계정 값들이 들어있는 메인 테이블이 다른 테이블로 한 번 래핑 되어있는 경우 (추가 정보 테이블로 인지해서 제대로 파싱이 안됨)
        # 만약 추가 정보 테이블인데 안에 테이블이 하나 더 있으면 내부 테이블을 기준으로 파싱하도록 변경
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20231114003042&dcmNo=9500646&eleId=19&offset=105778&length=123278&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2023-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 19_094_002_603
        assert data_scraper.retreive_operating_profit() == 456_527_954
        assert data_scraper.retreive_net_profit() == 4_665_525_211
        assert data_scraper.retreive_equity() == 66_816_677_834
        assert data_scraper.retreive_debt() == 4_229_214_028
        assert data_scraper.retreive_cash() == 5_587_514_803

    def test_실패케이스_20240506_3(self):
        # 현금흐름표가 아예 없는 케이스.. 상장 폐지된 기업인듯
        # 표 자체가 없는 경우 None 반환
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20240329000617&dcmNo=9780572&eleId=21&offset=180407&length=20614&dtd=dart4.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2023-4'
        assert data_scraper.retreive_period_length() == 12
        assert data_scraper.retreive_sales() == 44_238_998_675
        assert data_scraper.retreive_operating_profit() == -4_188_312_757
        assert data_scraper.retreive_net_profit() == -4_315_526_273
        assert data_scraper.retreive_equity() == 3_015_121_556
        assert data_scraper.retreive_debt() == 12_418_186_557
        assert data_scraper.retreive_cash() == None

    def test_실패케이스_20240506_4(self):
        # 추가 정보 테이블 판별기준이 row개수 5개 이하였는데, 이 테이블은 추가정보 테이블에 row가 6개 있음 
        # 기준을 8개로 상향
        # 또한, 계정과목에 [자본총계] 이런 식으로 중괄호가 있는데, 중괄호 무시하고 계정과목 검색하도록 변경
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20230814003057&dcmNo=9394891&eleId=17&offset=243367&length=115070&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2023-2'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == 88_293_000_000
        assert data_scraper.retreive_operating_profit() == 16_164_000_000
        assert data_scraper.retreive_net_profit() == -15_708_000_000
        assert data_scraper.retreive_equity() == 978_998_000_000
        assert data_scraper.retreive_debt() == 779_321_000_000
        assert data_scraper.retreive_cash() == 134_318_000_000

    def test_실패케이스_20240506_5(self):
        # 추가적인 설명으로, 재무상태표와 손익계산서라는 단어가 기존 부제 표시 외에 등장하여, 표의 종류를 제대로 분별하지 못함.
        # 만약 하나의 요소에서 재무제표의 여러 종류가 언급되면 그 요소는 넘어가도록 변경
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20240320001781&dcmNo=9742929&eleId=19&offset=604606&length=206704&dtd=dart4.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2023-4'
        assert data_scraper.retreive_period_length() == 12
        assert data_scraper.retreive_sales() == 3_371_117_789_921
        assert data_scraper.retreive_operating_profit() == -45_110_972_558
        assert data_scraper.retreive_net_profit() == -1_579_398_502_150
        assert data_scraper.retreive_equity() == -561_743_856_036
        assert data_scraper.retreive_debt() == 5_842_979_816_295
        assert data_scraper.retreive_cash() == 230_661_360_830

    def test_실패케이스_20240506_6(self):
        # 손익계산서 제목이 '손익계산'까지만 적혀있음
        # '손익계산'까지로 손익계산서 판단
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20231114001869&dcmNo=9497530&eleId=25&offset=515814&length=92005&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2023-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 18_631_426_063
        assert data_scraper.retreive_operating_profit() == -5_874_573_275
        assert data_scraper.retreive_net_profit() == -5_114_560_781
        assert data_scraper.retreive_equity() == 47_109_893_683
        assert data_scraper.retreive_debt() == 23_373_363_314
        assert data_scraper.retreive_cash() == 2_203_143_077




