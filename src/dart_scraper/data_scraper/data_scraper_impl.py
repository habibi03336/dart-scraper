from collections import defaultdict
import re
from .data_scraper import DataScraper

class DataScraperImpl(DataScraper):
    unit_map = defaultdict(lambda: 1)
    unit_map["천"] = 1_000
    unit_map["만"] = 10_000
    unit_map["백만"] = 1_000_000
    unit_map["천만"] = 10_000_000
    unit_map["억"] = 100_000_000
    units = ["억", "천만", "백만", "만", "천", "백"]
    foreign_currencies = ["CNY", "USD", "JPY"]
    finance_names = ["재무상태표", "손익계산서", "현금흐름표"]
    
    def __init__(self, html):
        self._parse_html(html)

    def retreive_currency(self):
        return self.tables['currency']

    def retreive_period_standard(self):
        return self.tables['period'].year_quarter()

    def retreive_period_length(self):
        return self.tables['period_length']

    def is_3month_data(self):
        return self.tables['is_3month_data']

    def retreive_sales(self):
        return self._get_index_num("손익계산서", ["매출액", "수익", "매출", "영업수익"])

    def retreive_operating_profit(self):
        return self._get_index_num("손익계산서", ["영업이익", "영업손익", "영업손실", "계속영업이익"])
    
    def retreive_net_profit(self):
        return self._get_index_num("손익계산서", ["당기순이익", "분기순이익", "연결분기순이익", "연결당기순이익", "분기순이익", "반기순이익", "반기순손익", "분기순손익", "당기순이익및포괄이익", "반기순손실", "당분기순이익", "당기순손실", "분기순손실", "당반기순이익", "당기순손익", "연결반기순이익", "반(당)기순이익", "분(당)기순이익", "연결당분기순이익", "연결당반기순이익", "당(분)기순이익"])

    def retreive_equity(self):
        return self._get_index_num("재무상태표", ["자본총계"])

    def retreive_debt(self):
        return self._get_index_num("재무상태표", ["부채총계"])
    
    def retreive_cash(self):
        return self._get_index_num("현금흐름표", ["기말의현금및현금성자산", "분기말현금및현금성자산", "기말현금및현금성자산", "분기말의현금및현금성자산", "반기말현금및현금성자산", "반기말의현금및현금성자산", "기말의현금", "당기말현금및현금성자산", "당기말의현금및현금성자산", "당반기말의현금및현금성자산", "기말현금", "분기말재무상태표상현금및현금성자산", "분기(당기)말의현금및현금성자산", "분기말의현금", "반기말의현금", "기말현금및예치금", "현금및현금성자산(기말)", "당기(분기)말현금및현금성자산", "당(분)기말의현금및현금성자산"])

    def _get_index_num(self, table_name, index_names):
        if self.tables[table_name].main_table is None:
            return None
        cell_offset = DataScraperImpl._get_cell_offset(self.tables[table_name].main_table)
        rows = self.tables[table_name].main_table.tbody.find_all(recursive=False)
        for row in rows:
            cells = row.find_all(recursive=False)
            row_name = ''.join([c.strip() for c in cells[0].text])
            if '.' in cells[0].text:
                row_name = row_name.split(".")[1].strip()
            if '(주' in row_name:
                row_name = row_name.split('(주')[0].strip()
            if '(손실)' in row_name:
                row_name = row_name.split("(손실)")[0].strip()
            if '(매출액)' in row_name:
                row_name = row_name.split("(매출액)")[0].strip()
            if re.sub(r'[\[\]]', '', row_name)in index_names:
                if self.is_3month_data() and table_name == '손익계산서':
                    count = 0
                    for i in range(1, len(cells) - cell_offset):
                        cell_content = cells[i + cell_offset].text.strip()
                        if cell_content and cell_content != "-":
                            count += 1
                        if count == 2:
                            return DataScraperImpl._parse_cell_num(cells[i + cell_offset]) * DataScraperImpl.unit_map[self.tables[table_name].unit]
                if 1+cell_offset < len(cells) and cells[1+cell_offset].text.strip() and cells[1+cell_offset].text.strip() != "-":
                    return DataScraperImpl._parse_cell_num(cells[1+cell_offset]) * DataScraperImpl.unit_map[self.tables[table_name].unit]
                elif 2+cell_offset < len(cells) and cells[2+cell_offset].text.strip() and cells[2+cell_offset].text.strip() != "-":
                    return DataScraperImpl._parse_cell_num(cells[2+cell_offset]) * DataScraperImpl.unit_map[self.tables[table_name].unit]
        return None

    def _get_cell_offset(table):
        if table.thead:
            head_cells = table.thead.find_all(recursive=False)[0].find_all(lambda tag: tag.name == 'th')
        else:
            head_cells = table.tbody.find_all(recursive=False)[0].find_all(lambda tag: tag.name == 'td')
        cell_offset = 0
        for i in range(1, len(head_cells)):
            text = "".join([c.strip() for c in head_cells[i].getText()])
            if '제' in text or '년도' in text:
                return cell_offset
            cell_offset += 1
        return 0

    def _parse_cell_num(cell_num):
        c = cell_num.text.replace(",","").replace("=", "").strip()
        if c[:3] == "(-)":
            return -int(c[3:])
        if c[0] == "(" :
            return -int(c[1:-1])
        if c[0] == "△" :
            return -int(c[1:])
        return int(c)

    def _parse_html(self, html):
        sections = DataScraperImpl._split_by_consecutive_table(html)
        self.tables = DataScraperImpl._parse_sections(sections)

    def _split_by_consecutive_table(html):
        children = html.body.find_all(recursive=False)
        sections = []
        section = []
        for child in children:
            if DataScraperImpl._is_has_title(child):
                sections.append(section)
                section = []
            section.append(child)
        if section:
            sections.append(section)
        return sections

    def _is_has_title(elem):
        titles = ["손익계산서", "자본변동표", "현금흐름표"]
        text = "".join([c.strip() for c in elem.getText()])
        for title in titles:
            if title in text:
                return True
        return False

    def _parse_sections(sections):
        summary = {
            "재무상태표": Section(),
            "손익계산서": Section(),
            "현금흐름표": Section(),
            "currency": "KRW",
            "period": "",
            "period_length": 3,
            "is_3month_data": True,
        }
        parsed_table = DataScraperImpl._classify_sections(summary, sections)
        DataScraperImpl._parse_unit(parsed_table)
        position_text = DataScraperImpl._get_all_text_from_elems(parsed_table['재무상태표'].extra_elems)
        DataScraperImpl._parse_currency(parsed_table, position_text) 
        DataScraperImpl._parse_period(parsed_table, position_text)
        DataScraperImpl._parse_period_length(parsed_table)
        DataScraperImpl._is_3month_data(parsed_table)
        return parsed_table
    
    def _classify_sections(summary, sections):
        for i in range(len(sections)):
            section = sections[i]
            flag = '재무상태표' if i == 0 else None 
            for elem in section:
                elem_text = ''.join([c.strip() for c in elem.getText()])
                if sum(['재무상태표' in elem_text, '손익계산서' in elem_text, '현금흐름표' in elem_text]) >= 2:
                    continue
                if not summary['재무상태표'].main_table and '재무상태표' in elem_text:
                    flag = '재무상태표'
                if not summary['손익계산서'].main_table and ('손익계산' in elem_text or '손익포괄계산' in elem_text or '손익상태' in elem_text):
                    flag = '손익계산서'
                if not summary['현금흐름표'].main_table and '현금흐름표' in elem_text:
                    flag = '현금흐름표'
                if not flag:
                    continue
                if DataScraperImpl._is_meta_table(elem) and len(elem.find_all(lambda tag: tag.name == 'table', recursive=True)) > 0:
                    elem = elem.find_all(lambda tag: tag.name == 'table', recursive=True)[0]
                if (elem.name == 'table' and (len(summary[flag].extra_elems) == 0)) \
                    or DataScraperImpl._is_meta_table(elem) \
                    or elem.name != 'table':
                        summary[flag].extra_elems.append(elem)
                elif not summary[flag].main_table and DataScraperImpl._is_main_table(elem):
                    summary[flag].main_table = elem
        return summary

    def _is_meta_table(elem):
        return elem.name == 'table' and ((elem.has_attr('class') and 'nb' in elem['class']) or (len(elem.tbody.find_all(recursive=False)) <= 8))

    def _is_main_table(elem):
        return (elem.name == 'table' and len(elem.tbody.find_all(recursive=False)) > 8) 

    def _parse_unit(summary):
        for key in DataScraperImpl.finance_names:
            buffer = []
            for elem in summary[key].extra_elems:
                buffer.append(elem.getText())
            text = ''.join(buffer).replace("\n", "").replace("\t", "").replace(" ", "")
            start_index = text.find("(단위")
            if start_index != -1:
                end_index = 0
                for i in range(start_index, start_index + 10):
                    if text[i] == ")":
                        end_index = i
                        break
                position_unit = text[start_index+1: end_index].strip().split(":")[1].strip()
                for unit in DataScraperImpl.units:
                    if unit in position_unit:
                        summary[key].unit = unit
                        break

    def _parse_currency(summary, position_text):
        start_index = position_text.find("(단위")
        if start_index == -1:
            return
        end_index = 0
        for i in range(start_index, start_index + 10):
            if position_text[i] == ")":
                end_index = i
                break
        currency_containing_token = position_text[start_index+1: end_index].strip().split(":")[1].strip()
        for currency in DataScraperImpl.foreign_currencies:
            if currency in currency_containing_token:
                summary['currency'] = currency
                return

    def _parse_period(summary, position_text):
        periods = DataScraperImpl._get_all_periods(position_text)
        periods.sort(key=lambda period: -period.month_unit)
        summary['period'] = periods[0]

    def _get_all_periods(text):
        all_periods = []
        for match in re.finditer(r'[\d][\d][\d][\d][\D][\d]?[\d][\D][\d]?[\d]', text):
            parsed_period = Period.from_string(match.group())
            all_periods.append(parsed_period)
        return list(set(all_periods))

    def _parse_period_length(summary):
        text = DataScraperImpl._get_all_text_from_elems(summary['손익계산서'].extra_elems)
        periods = DataScraperImpl._get_all_periods(text)
        periods.sort(key=lambda period: -period.month_unit)
        if len(periods) == 1:
            # if one month data
            summary['period_length'] = 1
        else:
            finish_period = periods[0]
            start_period = periods[1]
            summary['period_length'] = finish_period - start_period + 1
    
    def _is_3month_data(summary):
        text = DataScraperImpl._get_all_text_from_elems([summary['손익계산서'].main_table])
        summary['is_3month_data'] = (text.find('3개월') != -1)

    def _get_all_text_from_elems(elems):
        buffer = []
        for el in elems:
            buffer.append(el.getText())
        text = ''.join(buffer)
        return "".join([c.strip() for c in text])


class Section:
    def __init__(self):
        self.main_table = None;
        self.unit = None;
        self.extra_elems = [];

class Period:
    def from_string(period_str):
        year, month, day = map(int, re.split(r'[\D]', period_str))
        return Period(year, month)

    def year_quarter(self):
        year, month = self._get_year(), self._get_month()
        quarter = 0
        if month >= 2 and month <= 4:
            quarter = 1
        elif month >= 5 and month <= 7:
            quarter = 2
        elif month >= 8 and month <= 10:
            quarter = 3
        elif month in [1, 11, 12]:
            quarter = 4
        return f'{year}-{quarter}'

    def __init__(self, year, month):
        self.month_unit = year * 12 + month

    def __str__(self):
        return f'{self._get_year()}-{self._get_month()}'

    def __sub__(self, other):
        return self.month_unit - other.month_unit

    def __eq__(self, other):
        return self.month_unit == other.month_unit

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.month_unit
        
    def _get_year(self):
        if self.month_unit % 12 == 0:
            return self.month_unit // 12 - 1
        return self.month_unit // 12
    
    def _get_month(self):
        if self.month_unit % 12 == 0:
            return 12
        return self.month_unit % 12