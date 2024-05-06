from .meta_scraper import MetaScraper
from threading import Lock
import js2py

pyjs_lock = Lock()
class MetaScraperImpl(MetaScraper):
    def __init__(self, html):
        self.tree_data = MetaScraperImpl._retrive_tree_data(html)

    def dcm_no(self):
        return self.tree_data[0].dcmNo

    def elem_id(self, index_name):
        i = 1
        finance_node = self.tree_data[0]
        while not "재무에 관한 사항" in finance_node.text:
            finance_node = self.tree_data[i]
            i += 1
        indexs = finance_node.children

        i = 0
        index_title = indexs[i].text.split(".")[1].strip()
        while index_name != index_title:
            i += 1
            index_title = indexs[i].text.split(".")[1].strip()
        return indexs[i].eleId

    def elem_index_id(self, index_name):
        i = 1
        finance_node = self.tree_data[0]
        while not index_name in finance_node.text:
            finance_node = self.tree_data[i]
            i += 1
        return finance_node.eleId
    
    def finance_elem_id(self):
        i = 1
        finance_node = self.tree_data[0]
        while not "재무제표" in ''.join([c.strip() for c in finance_node.text]):
            finance_node = self.tree_data[i]
            i += 1
        return finance_node.eleId

    def _retrive_tree_data(html):
        script = html.head.findAll(lambda tag: tag.name =='script')
        target_script = script[-1]
        script_text = target_script.text
        target_function_name = 'function initPage() ' if script_text.find('function makeToc() ') == -1  else 'function makeToc() '
        if target_function_name == 'function initPage() ':
            script_text = script_text[script_text.find(target_function_name):]
            script_text = script_text[len(target_function_name)+1:]

            stack_len = 1
            i = 0
            while stack_len != 0 and i < len(script_text):
                if script_text[i] == '{':
                    stack_len += 1
                if script_text[i] == '}':
                    stack_len -= 1
                i += 1

            target_function_content = script_text[:i-1]
            target_function_content = target_function_content.split("initLayerNew('winCorpInfo');")[1]
            target_function_content = target_function_content.split("//js tree")[0]
            target_function_total = "function f(){" + target_function_content + "\n\t\t\treturn treeData; \n}" 
            with pyjs_lock:
                target_function = js2py.eval_js(target_function_total)
            return target_function()
        else:
            script_text = script_text[script_text.find(target_function_name):]
            script_text = script_text[len(target_function_name)+1:]

            stack_len = 1
            i = 0
            while stack_len != 0 and i < len(script_text):
                if script_text[i] == '{':
                    stack_len += 1
                if script_text[i] == '}':
                    stack_len -= 1
                i += 1

            target_function_content = script_text[:i-1]
            target_function_content = target_function_content.split("//js tree")[0]
            target_function_total = "function f(){" + target_function_content + "\n\t\t\treturn treeData; \n}" 
            with pyjs_lock:
                target_function = js2py.eval_js(target_function_total)
            return target_function()
