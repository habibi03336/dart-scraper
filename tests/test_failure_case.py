from dart_scraper import DataScraper
from dart_scraper import MetaScraper
from util.html_fetcher_for_test import fetch_cover
from util.html_fetcher_for_test import fetch_content

class TestFailureCase:

    def test_20230811(self):
        # Meta scraping 시 tree 데이터를 가져오는 js함수가 조금 다른 경우였음
        # 원래 initPage 함수에 tree data가 있는데 , makeToc 함수로 tree data를 만들도록 분리해논 경우가 있었음
        rcp_no = "20230811002478"
        html = fetch_cover(rcp_no)

        # execute
        index = "연결재무제표"
        scraper = MetaScraper(html)
        dcm_no = scraper.dcm_no()
        elem_id = scraper.elem_id(index)

        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == "2023-2"
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == 78_242_824_718
        assert data_scraper.retreive_operating_profit() == -7_216_844_917
        assert data_scraper.retreive_net_profit() == -5_042_125_884
        assert data_scraper.retreive_equity() == 202_188_015_654
        assert data_scraper.retreive_debt() == 101_818_327_243
        assert data_scraper.retreive_cash() == 24_106_277_269