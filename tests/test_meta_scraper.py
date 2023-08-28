from dart_scraper import MetaScraper
from util.html_fetcher_for_test import fetch_cover

class TestMetaScraper:

    def test_find_dcm_no(self):
        # given
        rcp_no = "20230515002541" #KB금융 2023-1 분기보고서
        html = fetch_cover(rcp_no)

        # execute
        scraper = MetaScraper(html)
        dcm_no = scraper.dcm_no()

        # compare
        assert dcm_no == '9277507'

    def test_find_elem_id(self):
        # given
        rcp_no = "20230315001030" #현대자동차 2022 사업보고서
        index = "연결재무제표"
        html = fetch_cover(rcp_no)

        # execute
        scraper = MetaScraper(html)
        elem_id = scraper.elem_id(index)

        # compare
        assert elem_id == '24'

    def test_find_index_elem_id(self):
        # given
        rcp_no = "20190225000609" #대한화섬 2014 정정신고
        html = fetch_cover(rcp_no)

        # execute
        scraper = MetaScraper(html)
        elem_id = scraper.elem_index_id("재무제표 등")

        # compare
        assert elem_id == '27'

    def test_find_index_elem_id_정정보고서(self):
        # given
        rcp_no = "20160401000506" #KB금융 2015 사업보고서
        html = fetch_cover(rcp_no)

        # execute
        scraper = MetaScraper(html)
        elem_id = scraper.finance_elem_id()

        # compare
        assert elem_id == '4'

