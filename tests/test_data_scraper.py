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

class TestDataScraper:

    def test_제조기업_2020년대_1분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20220516002457&dcmNo=8666473&eleId=19&offset=191721&length=71754&dtd=dart3.xsd')
        # 에코프로비엠 2022-1 분기보고서
        # 당기순이익이 "분기순이익"으로 표기되어 있음
        # 기말현금및현금성 자산이 "분기말현금및현금성자산"으로 표기되어있음 
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-1'
        assert data_scraper.retreive_period_length() == 3
        assert data_scraper.retreive_sales() == 662_461_915_161
        assert data_scraper.retreive_operating_profit() == 41_062_294_987
        assert data_scraper.retreive_net_profit() == 30_411_457_961
        assert data_scraper.retreive_equity() == 621_579_904_073
        assert data_scraper.retreive_debt() == 1_186_176_330_280
        assert data_scraper.retreive_cash() == 63_021_302_691

    def test_제조기업_2020년대_반기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20220816001069&dcmNo=8770227&eleId=19&offset=315096&length=86484&dtd=dart3.xsd')
        # LG전자 2022-2 분기 보고서
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)
        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-2'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == 40_433_045_000_000
        assert data_scraper.retreive_operating_profit() == 2_735_144_000_000
        assert data_scraper.retreive_net_profit() == 1_739_033_000_000
        assert data_scraper.retreive_equity() == 23_253_025_000_000
        assert data_scraper.retreive_debt() == 32_115_772_000_000
        assert data_scraper.retreive_cash() == 6_482_932_000_000

    def test_제조기업_2020년대_사업보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20230307000542&dcmNo=9040011&eleId=19&offset=305544&length=101364&dtd=dart3.xsd')
        # 삼성전자 2022 사업보고서
        # 매출액이 "수익(매출액)"으로 표시됨
        # 당기순이익이 "당기순이익(손실)"로 표시됨
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-4'
        assert data_scraper.retreive_period_length() == 12
        assert data_scraper.retreive_sales() == 302_231_360_000_000
        assert data_scraper.retreive_operating_profit() == 43_376_630_000_000
        assert data_scraper.retreive_net_profit() == 55_654_077_000_000
        assert data_scraper.retreive_equity() == 354_749_604_000_000
        assert data_scraper.retreive_debt() == 93_674_903_000_000
        assert data_scraper.retreive_cash() == 49_680_710_000_000
        
        
    def test_금융기업_2020년대_1분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20230515002373&dcmNo=9277024&eleId=17&offset=1135471&length=162617&dtd=dart3.xsd')
        # 신한지주 2023-1 분기
        # 문제: 손익계산서에 계정과목 이름 바로 다음 칸이 숫자가 적혀있는 곳이 아님
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2023-1'
        assert data_scraper.retreive_period_length() == 3
        assert data_scraper.retreive_sales() == None
        assert data_scraper.retreive_operating_profit() == 1_756_186_000_000
        assert data_scraper.retreive_net_profit() == 1_414_343_000_000
        assert data_scraper.retreive_equity() == 55_795_494_000_000
        assert data_scraper.retreive_debt() == 620_380_094_000_000
        assert data_scraper.retreive_cash() == 29_421_069_000_000
 
    def test_금융기업_2020년대_반기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20220816001769&dcmNo=8772635&eleId=17&offset=2052983&length=139955&dtd=dart3.xsd')
        # KB금융지주 2022-2 분기
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-2'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == None
        assert data_scraper.retreive_operating_profit() == 3_502_003_000_000
        assert data_scraper.retreive_net_profit() == 2_772_105_000_000
        assert data_scraper.retreive_equity() == 48_383_936_000_000
        assert data_scraper.retreive_debt() == 646_140_160_000_000
        assert data_scraper.retreive_cash() == 9_031_349_000_000
    
    def test_금융기업_2020년대_3분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20221114002298&dcmNo=8872153&eleId=17&offset=1085301&length=204203&dtd=dart3.xsd')
        # 우리금융지주 2022-3 분기
        # 문제: 바로 다음 칸이 계정과목의 숫자가 아닌 경우가 있음 (총계는 한 칸 오른쪽에 적음)
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == None
        assert data_scraper.retreive_operating_profit() == 3_702_665_000_000
        assert data_scraper.retreive_net_profit() == 2_792_689_000_000
        assert data_scraper.retreive_equity() == 31_128_414_000_000
        assert data_scraper.retreive_debt() == 470_940_520_000_000
        assert data_scraper.retreive_cash() == 9_276_913_000_000

    def test_금융기업_2020년대_사업보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20230324001073&dcmNo=9103464&eleId=19&offset=2059571&length=134809&dtd=dart3.xsd')
        # KB금융지주 2022 사업보고서
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-4'
        assert data_scraper.retreive_period_length() == 12
        assert data_scraper.retreive_sales() == None
        assert data_scraper.retreive_operating_profit() == 5_638_855_000_000
        assert data_scraper.retreive_net_profit() == 4_173_239_000_000
        assert data_scraper.retreive_equity() == 49_642_914_000_000
        assert data_scraper.retreive_debt() == 651_527_934_000_000
        assert data_scraper.retreive_cash() == 26_162_524_000_000

    def test_제조기업_2010년대_1분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20150514005248&dcmNo=4666869&eleId=13&offset=368684&length=113979&dtd=dart3.xsd')
        # GS리테일 2015 1분기 보고서
        # 계정과목앞에 로마숫자와 점이 있음 "Ⅶ.영업이익"
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2015-1'
        assert data_scraper.retreive_period_length() == 3
        assert data_scraper.retreive_sales() == 1_324_824_332_099
        assert data_scraper.retreive_operating_profit() == 39_735_267_844
        assert data_scraper.retreive_net_profit() == 31_024_469_789
        assert data_scraper.retreive_equity() == 1_666_598_297_930
        assert data_scraper.retreive_debt() == 1_289_834_296_095
        assert data_scraper.retreive_cash() == 130_552_589_245

    def test_제조기업_2010년대_2분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20150813001312&dcmNo=4766417&eleId=13&offset=420171&length=136274&dtd=dart3.xsd')
        # 신세계 2015 2분기 보고서
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)


        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2015-2'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == 1_231_758_066_951
        assert data_scraper.retreive_operating_profit() == 120_822_145_582
        assert data_scraper.retreive_net_profit() == 331_539_777_549
        assert data_scraper.retreive_equity() == 3_928_535_616_143
        assert data_scraper.retreive_debt() == 4_098_779_793_081
        assert data_scraper.retreive_cash() == 532_936_031_545

    def test_제조기업_2010년대_3분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20181114002234&dcmNo=6383657&eleId=13&offset=414024&length=108143&dtd=dart3.xsd')
        # 현대자동차 2018년 3분기 보고서
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2018-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 71_582_098_000_000
        assert data_scraper.retreive_operating_profit() == 1_921_038_000_000
        assert data_scraper.retreive_net_profit() == 1_848_314_000_000
        assert data_scraper.retreive_equity() == 74_924_021_000_000
        assert data_scraper.retreive_debt() == 104_848_396_000_000
        assert data_scraper.retreive_cash() == 9_336_428_000_000

    def test_제조기업_2010년대_4분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20180402004388&dcmNo=6057630&eleId=13&offset=341662&length=97296&dtd=dart3.xsd')
        # 대우건설 2017 4분기 보고서
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2017-4'
        assert data_scraper.retreive_period_length() == 12
        assert data_scraper.retreive_sales() == 11_766_840_487_669
        assert data_scraper.retreive_operating_profit() == 429_026_367_019
        assert data_scraper.retreive_net_profit() == 257_893_627_412
        assert data_scraper.retreive_equity() == 2_278_069_286_129
        assert data_scraper.retreive_debt() == 6_498_263_149_456
        assert data_scraper.retreive_cash() == 517_092_528_197
        

    def test_서비스금융기업_2020년대_1분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20220516001307&dcmNo=8663608&eleId=19&offset=188728&length=66363&dtd=dart3.xsd')
        # 카카오페이 2022년 1분기, 영업손실
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-1'
        assert data_scraper.retreive_period_length() == 3
        assert data_scraper.retreive_sales() == 123_345_338_644
        assert data_scraper.retreive_operating_profit() == -1_078_608_013
        assert data_scraper.retreive_net_profit() == 3_791_117_524
        assert data_scraper.retreive_equity() == 1_802_150_808_677
        assert data_scraper.retreive_debt() == 1_388_200_828_990
        assert data_scraper.retreive_cash() == 1_166_589_189_408

    def test_서비스금융기업_2020년대_2분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20220816001814&dcmNo=8772792&eleId=19&offset=227553&length=71140&dtd=dart3.xsd')
        # 카카오뱅크 2022년 2분기
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-2'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == 709_235_000_000
        assert data_scraper.retreive_operating_profit() == 162_769_000_000
        assert data_scraper.retreive_net_profit() == 123_812_000_000
        assert data_scraper.retreive_equity() == 5_556_301_000_000
        assert data_scraper.retreive_debt() == 34_026_262_000_000
        assert data_scraper.retreive_cash() == 8_411_000_000

    def test_서비스금융기업_2020년대_3분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20221114001768&dcmNo=8870851&eleId=24&offset=229725&length=75021&dtd=dart3.xsd')
        # 카카오페이 2022년 3분기
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 398_815_207_234
        assert data_scraper.retreive_operating_profit() == -23_268_781_879
        assert data_scraper.retreive_net_profit() == -6_578_580_326
        assert data_scraper.retreive_equity() == 1_793_540_532_350
        assert data_scraper.retreive_debt() == 1_453_037_999_481
        assert data_scraper.retreive_cash() == 1_452_852_366_666
    
    def test_서비스금융기엽_2020년대_4분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20230321001298&dcmNo=9084380&eleId=19&offset=227131&length=64048&dtd=dart3.xsd')
        # 카카오 뱅크 2022년 4분기
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-4'
        assert data_scraper.retreive_period_length() == 12
        assert data_scraper.retreive_sales() == 1_605_801_000_000
        assert data_scraper.retreive_operating_profit() == 353_186_000_000
        assert data_scraper.retreive_net_profit() == 263_091_000_000
        assert data_scraper.retreive_equity() == 5_715_110_000_000
        assert data_scraper.retreive_debt() == 33_800_969_000_000
        assert data_scraper.retreive_cash() == 1_381_539_000_000

    def test_IT서비스기엽_2020년대_1분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20230512001100&dcmNo=9270863&eleId=19&offset=215826&length=72411&dtd=dart3.xsd')
        # 네이버 2023년 1분기
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2023-1'
        assert data_scraper.retreive_period_length() == 3
        assert data_scraper.retreive_sales() == 2_280_442_537_690
        assert data_scraper.retreive_operating_profit() == 330_492_062_205
        assert data_scraper.retreive_net_profit() == 43_655_223_104
        assert data_scraper.retreive_equity() == 24_123_911_619_350
        assert data_scraper.retreive_debt() == 11_649_421_682_473
        assert data_scraper.retreive_cash() == 2_955_043_611_306

    def test_IT서비스기엽_2020년대_2분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20220816002580&dcmNo=8775459&eleId=24&offset=463760&length=90676&dtd=dart3.xsd')
        # 카카오 2022년 2분기
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-2'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == 3_474_017_956_597
        assert data_scraper.retreive_operating_profit() == 329_677_382_255
        assert data_scraper.retreive_net_profit() == 1_423_336_392_973
        assert data_scraper.retreive_equity() == 14_821_152_791_339
        assert data_scraper.retreive_debt() == 9_955_798_559_392
        assert data_scraper.retreive_cash() == 4_307_258_808_444
    
    def test_IT서비스기업_2020년대_3분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20221114001371&dcmNo=8869823&eleId=19&offset=483373&length=66532&dtd=dart3.xsd')
        # 솔트룩스 2022년 3분기
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 16_470_265_484
        assert data_scraper.retreive_operating_profit() == -5_172_190_920
        assert data_scraper.retreive_net_profit() == -3_602_965_699
        assert data_scraper.retreive_equity() == 51_254_686_350
        assert data_scraper.retreive_debt() == 29_875_393_388
        assert data_scraper.retreive_cash() == 12_344_944_746

    def test_IT서비스기업_2020년대_4분기보고서(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20230313000551&dcmNo=9050721&eleId=19&offset=187195&length=102681&dtd=dart3.xsd')
        # 에프앤가이드 2022년 4분기
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-4'
        assert data_scraper.retreive_period_length() == 12
        assert data_scraper.retreive_sales() == 28_422_917_679
        assert data_scraper.retreive_operating_profit() == 6_072_307_916
        assert data_scraper.retreive_net_profit() == 7_944_169_868
        assert data_scraper.retreive_equity() == 56_107_226_484
        assert data_scraper.retreive_debt() == 42_427_474_057
        assert data_scraper.retreive_cash() == 9_111_329_388

    
    def test_중국통화_표시기업(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20221128000610&dcmNo=8887256&eleId=19&offset=252514&length=109166&dtd=dart3.xsd')
        # 로스웰 2022-3 분기보고서
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "CNY"
        assert data_scraper.retreive_period_standard() == '2022-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 142_534_145
        assert data_scraper.retreive_operating_profit() == -36_227_393
        assert data_scraper.retreive_net_profit() == -65_528_543
        assert data_scraper.retreive_equity() == 1_093_978_471
        assert data_scraper.retreive_debt() == 384_647_859
        assert data_scraper.retreive_cash() == 818_515_192

    def test_일본통화_표시기업(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20221031000294&dcmNo=8853500&eleId=19&offset=175956&length=122877&dtd=dart3.xsd')
        # JTC 2022-3 분기보고서
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "JPY"
        assert data_scraper.retreive_period_standard() == '2022-3'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == 618_439_931
        assert data_scraper.retreive_operating_profit() == -1_184_449_268
        assert data_scraper.retreive_net_profit() == -1_128_811_242
        assert data_scraper.retreive_equity() == 1_966_633_947
        assert data_scraper.retreive_debt() == 22_246_578_361
        assert data_scraper.retreive_cash() == 1_055_919_028

    def test_미국통화_표시기업(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20221111000684&dcmNo=8865817&eleId=19&offset=195232&length=89804&dtd=dart3.xsd')
        # 잉글우드랩 2022-3 분기보고서
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "USD"
        assert data_scraper.retreive_period_standard() == '2022-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 86_861_752
        assert data_scraper.retreive_operating_profit() == 5_548_205
        assert data_scraper.retreive_net_profit() == 6_117_690
        assert data_scraper.retreive_equity() == 72_274_126
        assert data_scraper.retreive_debt() == 33_960_181
        assert data_scraper.retreive_cash() == 6_425_454

    def test_테이블_특이케이스_계정이름다음주석(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20220516001802&dcmNo=8664798&eleId=19&offset=117554&length=44700&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-1'
        assert data_scraper.retreive_period_length() == 3
        assert data_scraper.retreive_sales() == 72_073_732_829
        assert data_scraper.retreive_operating_profit() == 1_717_787_019
        assert data_scraper.retreive_net_profit() == 1_602_888_491
        assert data_scraper.retreive_equity() == 62_373_582_074
        assert data_scraper.retreive_debt() == 47_238_424_424
        assert data_scraper.retreive_cash() == 20_027_394_281

    def test_테이블_특이케이스_당기순이익계정이큰목차로테이블에존재(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20221114002393&dcmNo=8872417&eleId=19&offset=268185&length=65753&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 310_352_067_647
        assert data_scraper.retreive_operating_profit() == 19_946_858_488
        assert data_scraper.retreive_net_profit() == -1_497_336_756
        assert data_scraper.retreive_equity() == 59_729_823_892
        assert data_scraper.retreive_debt() == 447_175_507_043
        assert data_scraper.retreive_cash() == 51_890_954_369

    def test_형식_특이케이스_추가적인_테이블이_맨위에존재(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20220812000480&dcmNo=8763953&eleId=19&offset=142265&length=69436&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-2'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == 282_516_749_000
        assert data_scraper.retreive_operating_profit() == 13_446_700_000
        assert data_scraper.retreive_net_profit() == 9_114_339_000
        assert data_scraper.retreive_equity() == 229_392_012_000
        assert data_scraper.retreive_debt() == 231_674_506_000
        assert data_scraper.retreive_cash() == 229_453_905_000

    def test_형식_특이케이스_테이블메타정보에nb클래스없음(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20220816002672&dcmNo=8775714&eleId=21&offset=78673&length=32245&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-2'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == 877_197_505
        assert data_scraper.retreive_operating_profit() == -631_861_423
        assert data_scraper.retreive_net_profit() == -481_175_288
        assert data_scraper.retreive_equity() == -4_106_107_910
        assert data_scraper.retreive_debt() == 5_394_688_472
        assert data_scraper.retreive_cash() == 148_958_681

    
    def test_정정보고서인경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20220816002669&dcmNo=8775775&eleId=4&offset=11510&length=352289&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-2'
        assert data_scraper.retreive_period_length() == 3
        assert data_scraper.retreive_sales() == 135_706_282_069
        assert data_scraper.retreive_operating_profit() == 9_920_439_142
        assert data_scraper.retreive_net_profit() == -957_322_915
        assert data_scraper.retreive_equity() == 196_955_682_670
        assert data_scraper.retreive_debt() == 172_161_896_116
        assert data_scraper.retreive_cash() == 14_402_693_454

    def test_금융사정정보고서인경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20160401000506&dcmNo=5038484&eleId=4&offset=11487&length=1274743&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2015-4'
        assert data_scraper.retreive_period_length() == 12
        assert data_scraper.retreive_sales() == None
        assert data_scraper.retreive_operating_profit() == 1_821_134_000_000
        assert data_scraper.retreive_net_profit() == 1_727_306_000_000
        assert data_scraper.retreive_equity() == 28_902_722_000_000
        assert data_scraper.retreive_debt() == 300_162_745_000_000
        assert data_scraper.retreive_cash() == 7_457_919_000_000
    
    def test_당기순이익이계층형으로분리되어제시되는경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20221114002401&dcmNo=8872441&eleId=19&offset=168504&length=62616&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 47_727_208_168
        assert data_scraper.retreive_operating_profit() == 9_310_808_543
        # 당기순이익 직접적인 값이 없다면 None 처리
        assert data_scraper.retreive_net_profit() == None
        assert data_scraper.retreive_equity() == 172_101_907_240
        assert data_scraper.retreive_debt() == 33_875_498_573
        assert data_scraper.retreive_cash() == 10_313_262_583

    def test_당기순이익계정과목이름이특이한경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20150817001489&dcmNo=4772203&eleId=13&offset=1454333&length=96419&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2015-2'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == None
        assert data_scraper.retreive_operating_profit() == 933_786_000_000
        assert data_scraper.retreive_net_profit() == 959_576_000_000
        assert data_scraper.retreive_equity() == 28_196_495_000_000
        assert data_scraper.retreive_debt() == 289_135_372_000_000
        assert data_scraper.retreive_cash() == 8_165_753_000_000

    def test_테이블사이에의미없는p태그가있는경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20180814002280&dcmNo=6287532&eleId=13&offset=1479597&length=153372&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2018-2'
        assert data_scraper.retreive_period_length() == 6
        assert data_scraper.retreive_sales() == None
        assert data_scraper.retreive_operating_profit() == 2_509_874_000_000
        assert data_scraper.retreive_net_profit() == 1_817_092_000_000
        assert data_scraper.retreive_equity() == 34_298_893_000_000
        assert data_scraper.retreive_debt() == 418_983_090_000_000
        assert data_scraper.retreive_cash() == 7_578_624_000_000

    def test_자본변동표에테이블과p태그가많은경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20150522000376&dcmNo=4680279&eleId=15&offset=1149287&length=99587&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2014-4'
        assert data_scraper.retreive_period_length() == 12
        assert data_scraper.retreive_sales() == None
        assert data_scraper.retreive_operating_profit() == 1_243_447_000_000
        assert data_scraper.retreive_net_profit() == 979_789_000_000
        assert data_scraper.retreive_equity() == 21_893_642_000_000
        assert data_scraper.retreive_debt() == 293_654_604_000_000
        assert data_scraper.retreive_cash() == 9_671_645_000_000

    def test_숫자에특수문자표기로음수를나타내는케이스(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20160513001280&dcmNo=5135112&eleId=15&offset=100387&length=72695&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2016-1'
        assert data_scraper.retreive_period_length() == 3
        assert data_scraper.retreive_sales() == 155_255_400
        assert data_scraper.retreive_operating_profit() == -341_783_167
        assert data_scraper.retreive_net_profit() == -742_986_464
        assert data_scraper.retreive_equity() == 34_344_061_067
        assert data_scraper.retreive_debt() == 3_157_411_961
        assert data_scraper.retreive_cash() == 784_233_798

    def test_빈칸에의미없는기호넣은케이스(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20171113000012&dcmNo=5840043&eleId=15&offset=99720&length=70988&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2017-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 738_675_711
        assert data_scraper.retreive_operating_profit() == -1_011_576_933 
        assert data_scraper.retreive_net_profit() == -869_671_828
        assert data_scraper.retreive_equity() == 31_215_812_782
        assert data_scraper.retreive_debt() == 3_633_208_566
        assert data_scraper.retreive_cash() == 2_213_690_235

    
    def test_현금흐름표계정에재무상태표가언급되는경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20230316000958&dcmNo=9065081&eleId=19&offset=566668&length=110394&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2022-4'
        assert data_scraper.retreive_period_length() == 12
        assert data_scraper.retreive_sales() == 1_841_963_668_280
        assert data_scraper.retreive_operating_profit() == 106_957_340_322 
        assert data_scraper.retreive_net_profit() == 93_785_712_822
        assert data_scraper.retreive_equity() == 986_415_922_987
        assert data_scraper.retreive_debt() == 8_517_287_853_460
        assert data_scraper.retreive_cash() == 571_134_516_524

    def test_p태그로제목이표시된경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20180615000380&dcmNo=6218053&eleId=15&offset=602790&length=44183&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2017-4'
        assert data_scraper.retreive_period_length() == 12
        assert data_scraper.retreive_sales() == 19_155_572_359
        assert data_scraper.retreive_operating_profit() == 3_563_613_602 
        assert data_scraper.retreive_net_profit() == 3_603_176_883
        assert data_scraper.retreive_equity() == 6_372_517_171
        assert data_scraper.retreive_debt() == 3_901_790_253
        assert data_scraper.retreive_cash() == 3_415_642_275

    def test_단위가표시되어있지않는경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20171114000325&dcmNo=5842457&eleId=13&offset=100230&length=115510&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2017-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 12_369_273_164
        assert data_scraper.retreive_operating_profit() == 1_715_385_569
        assert data_scraper.retreive_net_profit() == 1_719_397_396
        assert data_scraper.retreive_equity() == 85_854_647_322
        assert data_scraper.retreive_debt() == 8_066_491_692
        assert data_scraper.retreive_cash() == 1_232_652
    
    def test_재무상태표열이름이간결한경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20151130001214&dcmNo=4870018&eleId=13&offset=220118&length=78519&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2015-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 259_617_199
        assert data_scraper.retreive_operating_profit() == -17_122_834_935
        assert data_scraper.retreive_net_profit() == -38_187_079_089
        assert data_scraper.retreive_equity() == 40_758_758_179
        assert data_scraper.retreive_debt() == 87_403_287_033
        assert data_scraper.retreive_cash() == 32_847_456_250

    def test_한달짜리재무제표(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20180330002495&dcmNo=6036512&eleId=13&offset=136948&length=32730&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2017-4'
        assert data_scraper.retreive_period_length() == 1
        assert data_scraper.retreive_sales() == 30_302_120_514
        assert data_scraper.retreive_operating_profit() == 5_007_673_808 
        assert data_scraper.retreive_net_profit() == 2_426_389_384
        assert data_scraper.retreive_equity() == 359_175_875_647
        assert data_scraper.retreive_debt() == 70_321_944_470
        assert data_scraper.retreive_cash() == 14_636_315_340

    def test_당기순이익이없는경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20210514001603&dcmNo=8070602&eleId=14&offset=311726&length=52891&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2021-1'
        assert data_scraper.retreive_period_length() == 3
        assert data_scraper.retreive_sales() == 4_254_116_000_000
        assert data_scraper.retreive_operating_profit() == 341_219_000_000
        assert data_scraper.retreive_net_profit() == None
        assert data_scraper.retreive_equity() == 8_218_007_000_000
        assert data_scraper.retreive_debt() == 12_582_074_000_000
        assert data_scraper.retreive_cash() == 2_400_981_000_000

    def test_연월일외에연속적인숫자가있는경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20181114002435&dcmNo=6384144&eleId=13&offset=230064&length=66224&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2018-3'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == 50_296_565_698
        assert data_scraper.retreive_operating_profit() == -2_369_709_145
        assert data_scraper.retreive_net_profit() == -3_071_324_588
        assert data_scraper.retreive_equity() == 12_828_067_903
        assert data_scraper.retreive_debt() == 118_576_694_715
        assert data_scraper.retreive_cash() == 8_090_904_984

    def test_데이터컬럼이딱한개만있는경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20150528000182&dcmNo=4684532&eleId=15&offset=153628&length=23971&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2014-4'
        assert data_scraper.retreive_period_length() == 9
        assert data_scraper.retreive_sales() == None
        assert data_scraper.retreive_operating_profit() == -685_471_281
        assert data_scraper.retreive_net_profit() == -619_497_672
        assert data_scraper.retreive_equity() == 12_733_886_838
        assert data_scraper.retreive_debt() == 1_812_699_538
        assert data_scraper.retreive_cash() == 1_470_538_205

    def test_메타데이터가테이블로주어지는경우(self):
        rcp_no, dcm_no, elem_id = \
            retrieve_meta('https://dart.fss.or.kr/report/viewer.do?rcpNo=20171114000784&dcmNo=5843318&eleId=15&offset=134263&length=88160&dtd=dart3.xsd')
        html = fetch_content(rcp_no, elem_id, dcm_no)
        data_scraper = DataScraper(html)

        assert data_scraper.retreive_currency() == "KRW"
        assert data_scraper.retreive_period_standard() == '2017-3'
        assert data_scraper.retreive_period_length() == 3
        assert data_scraper.retreive_sales() == 121_844_791_780
        assert data_scraper.retreive_operating_profit() == 2_389_719_466
        assert data_scraper.retreive_net_profit() == 2_136_918_310
        assert data_scraper.retreive_equity() == 15_396_512_931
        assert data_scraper.retreive_debt() == 47_179_500_949
        assert data_scraper.retreive_cash() == 168_931_182