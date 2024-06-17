import os
import json
from collections import defaultdict
import shutil

def unify_files(source_directory, target_directory):
    """
    将多个文件夹中的所有TXT文件统一到一个文件夹中并编号，并生成URL的JSON文件
    :param source_directory: 源文件夹路径
    :param target_directory: 目标文件夹路径
    :param url_filename: URL对应关系文件名
    """
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    for root, _, files in os.walk(source_directory):
        for file in files:
            src_file_path = os.path.join(root, file)
            dst_file_path = os.path.join(target_directory, file)  # 保持原文件名
            shutil.copy(src_file_path, dst_file_path)
            

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(lambda: {'freq': 0, 'url': ''}))

    def add_document(self, doc_id, text, url):
        for word in text.split():
            self.index[word][doc_id]['freq'] += 1
            self.index[word][doc_id]['url'] = url

    def save_index(self, index_filename, url_filename, url_dict):
        sorted_index = {
            word: {
                'docfreq': len(doc_ids),
                'docs': {doc_id: {'freq': info['freq']} for doc_id, info in doc_ids.items()}
            }
            for word, doc_ids in self.index.items()
        }
        with open(index_filename, 'w', encoding='utf-8') as f:
            json.dump(sorted_index, f, ensure_ascii=False, indent=4)

        # 按顺序保存URL的JSON文件
        sorted_url_dict = dict(sorted(url_dict.items(), key=lambda item: int(item[0])))
        with open(url_filename, 'w', encoding='utf-8') as f:
            json.dump(sorted_url_dict, f, ensure_ascii=False, indent=4)

    def load_index(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.index = defaultdict(lambda: defaultdict(lambda: {'freq': 0}), data)

# 构建倒排索引
def build_inverted_index(tokenized_data_directory, index_filename, url_filename):
    inverted_index = InvertedIndex()
    url_dict = {}

    for root, _, files in os.walk(tokenized_data_directory):
        for file in files:
            if file.endswith(".txt") and not file.startswith("url"):
                doc_id = int(os.path.splitext(file)[0])
                file_path = os.path.join(root, file)
                file_url_path = os.path.join(root, f"url_{doc_id}.txt")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                with open(file_url_path, 'r', encoding='utf-8') as f:
                    url = f.read().strip()

                # 确保每个doc_id对应的url是唯一的
                if doc_id not in url_dict:
                    url_dict[doc_id] = url
                inverted_index.add_document(doc_id, text, url)
    
    inverted_index.save_index(index_filename, url_filename, url_dict)



source_directory1 = "data"
target_directory1 = "unified_data"
source_directory2 = "tokenized_data"
target_directory2 = "unified_tokenized_data"

# 统一文件
unify_files(source_directory1,target_directory1)
unify_files(source_directory2,target_directory2)

tokenized_data_directory = "unified_tokenized_data"
index_filename = "inverted_index.json"
url_filename = "doc_urls.json"

# 构建倒排索引
build_inverted_index(tokenized_data_directory, index_filename, url_filename)

