# 대한민국 재무제표 스크래퍼

대한민국 기업의 공시 정보를 https://dart.fss.or.kr/ 홈페이지를 통해 확인할 수 있다. 공시정보 중에서도 정기공시의 재무제표에는 기업의 매출, 영업이익, 순이익, 자산, 부채 등의 기업 주요 지표가 들어있다. 이 어플리케이션을 통해 다트에서 제공하는 재무제표 html을 스크래핑하여 주요 지표를 얻어 낼 수 있다.

## 스크래핑을 통해 얻을 수 있는 데이터

1. 재무제표의 표시통화 ('KRW', 'USD', 'JPY', 'CNY' 4가지 중 하나)
2. 재무제표 기준 연도, 분기 (보고서 말 일 기준으로, 몇 년도 몇 분기에 해당하는지를 나타냄. 기업의 회계연도가 아님)
3. 재무제표 측정 월 길이 (매출 등 손인계산서 계정이 몇 개월 치인지를 나타냄)
4. 매출
5. 영업이익
6. 순이익
7. 자본 총계
8. 부채 총계
9. 기말 현금 및 현금성 자산

## 사용 방법

1. 프록시 할 IP 주소를 마련한다. (동일한 IP에서 빠르게 요청을 하면 IP밴을 먹는다.)

- 멀티 쓰레딩을 활용하면 작업 속도가 훨씬 빠르다. 프록시 IP 10개 정도에 50개의 쓰레드로 dart 서버에 요청을 했을 때, IP밴을 먹지 않았다.

2. 프록시 IP 배열을 인자로 넘기면서 html fetcher 객체를 생성한다.

   ```python
   proxies =['https://proxy1.com', 'https://proxy2.com', 'https://proxy2.com']
   fetcher = HtmlFetcher(proxies)
   ```

3. Dart에서 제공하는 별도의 Open API를 활용하여 스크래핑 할 공시의 보고서 번호를 알아낸다. fetcher 객체에 해당 보고서 번호를 넣어 보고서의 메타 데이터를 가지고 있는 html을 받아온다.

   ```python
   report_code = 123456789 # Dart Open API 활용하여, 특정 기업의 일정 기간 동안의 보고서 목록을 받아올 수 있다.
   cover_html = fetcher.fetch_cover(report_code)
   ```

4. 메타 스크래퍼를 통해 보고서 중에서도 재무제표 html을 불러오는데 필요한 메타 데이터를 뽑아낸다. 재무제표 html을 불러오기 위해서는 elem_id, dcm_no 두 가지의 추가적인 데이터가 필요하다.

   elem_id는 보고서가 가진 여러 목차와 매핑되는 id를 의미한다. dcm_no는 보고서 마다 하나의 값을 가지는데, 무분별한 데이터 호출을 막기위해서 넣은 데이터로 보인다.

   ```python
   meta_scraper = MetaScraper(cover_html)
   elem_id = meta_scraper.elem_id('연결재무제표') # 찾고자하는 목차의 이름을 넣으면 된다. 주로 '연결재무제표' or '재무제표'
   dcm_no = meta_scraper.dcm_no()
   ```

5. 재무제표를 테이블 형식으로 제공하는 html을 불러온다.

   ```python
   finance_html = fetcher.fetch_content(report_code, elem_id, dcm_no)
   ```

6. 재무제표 html을 스크래핑 한다. 메소드를 통해서 원하는 데이터를 호출할 수 있다.

   ```python
   finance_scraper = DataScraper(finance_html)
   currency = finance_scraper.retreive_currency()
   year, quarter = finance_scraper.retreive_period_standard().split("-")
   period_length = finance_scraper.retreive_period_length()
   sales = finance_scraper.retreive_sales()
   operating_profit = finance_scraper.retreive_operating_profit()
   net_profit = finance_scraper.retreive_net_profit()
   equity = finance_scraper.retreive_equity()
   debt = finance_scraper.retreive_debt()
   cash_equivalents = finance_scraper.retreive_cash()
   ```

- 대량으로 스크래핑할 때는 재무제표 html을 불러오는 것과, 스크래핑하는 것을 분리하는 것이 좋다. 재무제표 html을 미리 로컬에 저장해두고, 저장된 html을 읽어와 스크래핑 하는 방식을 추천한다. 이렇게 하면 html 호출로 인한 오류와 스크래핑 시 오류를 분리할 수 있다. html을 요청하는 것이 큰 병목이기 때문에 저장해 두고 쓰는 것이 큰 이득이 된다.
