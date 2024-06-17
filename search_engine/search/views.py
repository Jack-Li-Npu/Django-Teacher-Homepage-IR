from django.shortcuts import render
from django.http import HttpResponse
import json
from collections import defaultdict
import math
import time
import nltk
import re
import jieba
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import os
import requests
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from pypinyin import lazy_pinyin


# nltk.download('punkt')

class InvertedIndex:
    def __init__(self):
        # 使用嵌套的 defaultdict 来存储词条、文档ID及其出现次数
        self.index = defaultdict(lambda: defaultdict(int))

    def load_index(self, filename):
        """
        从文件加载倒排索引
        :param filename: 文件名
        """
        with open(filename, 'r', encoding='utf-8') as f:
            self.index = json.load(f)

def load_urls(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def compute_tfidf(inverted_index, doc_lengths):
    """
    计算倒排索引中每个词条的TF-IDF值
    :param inverted_index: 倒排索引，包含每个词条及其相关文档的信息
    :param doc_lengths: 文档长度字典，包含每个文档的长度
    :return: 包含每个词条和文档ID的TF-IDF值字典
    """
    tfidf = defaultdict(lambda: defaultdict(float))
    N = len(doc_lengths)  # 文档总数

    for term, data in inverted_index.items():
        df = data['docfreq']  # 包含词条 t 的文档数
        idf = math.log(N / (df + 1))  # 计算 IDF，分母加1防止分母为零

        for doc_id, info in data['docs'].items():
            freq = info['freq']  # 访问嵌套的频率
            tf = freq / doc_lengths[int(doc_id)]
            tfidf[term][doc_id] = tf * idf
    return tfidf

def cosine_similarity(query, tfidf, doc_lengths):
    """
    计算查询向量和文档向量之间的余弦相似度
    :param query: 查询字符串
    :param tfidf: TF-IDF 字典
    :param doc_lengths: 文档长度字典
    :return: 排序后的 (文档ID, 相似度) 元组列表
    """
    query_terms = query.split()
    scores = defaultdict(float)
    query_tfidf = defaultdict(float)
    N = len(doc_lengths)

    # 计算查询向量的TF-IDF值
    term_freq = defaultdict(int)  # 词频统计
    for term in query_terms:
        term_freq[term] += 1  # 统计查询中的词频
    for term, freq in term_freq.items():
        if term in tfidf:
            df = len(tfidf[term])  # 获取包含该词条的文档数
            idf = math.log(N / (df + 1))  # 计算IDF值，分母加1以防止分母为零
            query_tfidf[term] = (freq / len(query_terms)) * idf  # 计算查询词条的TF-IDF值

    # 计算每个文档的相似度得分
    for term, q_tfidf in query_tfidf.items():
        for doc_id, d_tfidf in tfidf[term].items():
            scores[doc_id] += q_tfidf * d_tfidf  # 计算分子部分

    # 计算查询向量的模
    query_norm = math.sqrt(sum(q_tfidf ** 2 for q_tfidf in query_tfidf.values()))

    # 计算每个文档的模
    doc_norms = {}
    for doc_id in scores.keys():
        doc_norms[doc_id] = math.sqrt(sum(tfidf[term][doc_id] ** 2 for term in tfidf if doc_id in tfidf[term]))

    # 计算最终的余弦相似度
    for doc_id in scores:
        if query_norm * doc_norms[doc_id] != 0:
            scores[doc_id] /= (query_norm * doc_norms[doc_id])  # 计算余弦相似度
        else:
            scores[doc_id] = 0.0  # 防止除以零

    # 返回排序后的相似度得分
    return scores

def quick_sort(arr, low, high):
    """
    使用快速排序对数组进行排序
    :param arr: 待排序的 (文档ID, 自定义分值) 元组列表
    :param low: 列表的起始索引
    :param high: 列表的结束索引
    """
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    """
    快速排序的分区函数
    :param arr: 待排序的 (文档ID, 自定义分值) 元组列表
    :param low: 列表的起始索引
    :param high: 列表的结束索引
    :return: 分区点的索引
    """
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j][1] >= pivot[1]:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def custom_sort(scores):
    """
    自定义排序算法，根据余弦相似度进行排序
    :param scores: 余弦相似度得分字典
    :return: 排序后的 (文档ID, 自定义分值) 元组列表
    """
    combined_scores = [(doc_id, score) for doc_id, score in scores.items()]
    # 使用快速排序对 combined_scores 进行排序
    quick_sort(combined_scores, 0, len(combined_scores) - 1)
    return combined_scores


index_filename = "data/inverted_index.json"
url_filename = "data/doc_urls.json"

inverted_index = InvertedIndex()
inverted_index.load_index(index_filename)
doc_urls = load_urls(url_filename)

# 加载文档长度信息
with open(index_filename, 'r', encoding='utf-8') as f:
    data = json.load(f)
doc_lengths = defaultdict(int)
for term, info in data.items():
    if isinstance(info, dict) and 'docs' in info:
        for doc_id, doc_info in info['docs'].items():
            doc_lengths[int(doc_id)] += doc_info['freq']
tfidf = compute_tfidf(inverted_index.index, doc_lengths)

def index(request):
    return render(request, 'index.html')

def tokenize_content(content):
    """
    分别进行中英文分词
    """
    stemmer = PorterStemmer()
    chinese_content = ''.join(re.findall(r'[\u4e00-\u9fff]+', content))
    english_content = ' '.join(re.findall(r'[a-zA-Z]+', content))
    tokenized_content = []
    if chinese_content:
        # 采用搜索引擎模式，提高召回率
        cn_list_exact = jieba.lcut_for_search(chinese_content)
        with open('./stopwords-master/cn_stopwords.txt', encoding='utf-8') as f:  # 可根据需要打开停用词库，然后加上不想显示的词语
            con = f.readlines()
            stop_words = set()
            for i in con:
                i = i.replace("\n", "")  # 去掉读取每一行数据的\n
                stop_words.add(i)
        # 去除停用词并且去除单字
        for word in cn_list_exact:
            if word not in stop_words and len(word) > 1:
                tokenized_content.append(word)
    if english_content:
        english_tokens = word_tokenize(english_content)
        tokenized_content.append(' '.join([stemmer.stem(word) for word in english_tokens]))
    return tokenized_content

def get_snippet(doc_id, query_terms):
    """
    获取文档的部分内容，并高亮查询关键词
    :param doc_id: 文档ID
    :param query_terms: 查询关键词列表
    :return: 部分原文内容，并高亮查询关键词
    """
    file_path = os.path.join('unified_data', f'{doc_id}.txt')  # 假设文档内容保存在 data 文件夹中
    if not os.path.exists(file_path):
        return ''
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    snippet_length = 150  # 定义片段长度
    snippets = []
    # 查找每个查询词条的位置并截取上下文片段
    snippet_count = 0

    # 查找每个查询词条的位置并截取上下文片段
    for term in query_terms:
        if snippet_count >= 3:
            break
        for match in re.finditer(re.escape(term), content, flags=re.IGNORECASE):
            start = max(match.start() - snippet_length // 2, 0)
            end = min(match.end() + snippet_length // 2, len(content))
            snippet = content[start:end] + '......'

            # 高亮关键词
            snippet = re.sub(f'({re.escape(term)})', r'<mark class="highlight">\1</mark>', snippet, flags=re.IGNORECASE)
            snippets.append(snippet)
            snippet_count += 1

            # 只截取第一个匹配的片段，避免重复
            if snippet_count >= 3:
                break
    # 如果没有找到关键词，返回文档的开头部分
    if not snippets:
        print(1)
        snippet = content[:150] + '......'
        snippets.append(snippet)

    return '...'.join(snippets)


def get_access_token():
    """
    使用 API Key,Secret Key 获取access_token
    """
    api_key = os.environ.get("QIANFAN_ACCESS_KEY")
    secret_key = os.environ.get("QIANFAN_SECRET_KEY")
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def stream_wenxin_response(query):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
         "stream": True
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload, stream=True)
    
    def event_stream():
        for line in response.iter_lines():
            if line:
                line = line.decode("UTF-8")
                if line.startswith("data:"):
                    json_data = json.loads(line[5:])
                    if "result" in json_data:
                        yield f"data: {json_data['result']}\n\n"
    
    return event_stream

class WordCorrect:
    def __init__(self):
        self.char_path = './data/char.txt'
        self.model_path = './data/pinyin2word.model'
        # 存储着term列表
        self.dict_path = './data/dict.txt'
        self.charlist = [word.strip() for word in open(self.char_path, encoding='utf-8') if word.strip()]
        self.pinyin_dict = self.load_model(self.model_path)
        self.known_words = self.load_known_words()
        self.cache = {}

    def load_model(self, model_path):
        with open(model_path, 'r', encoding='utf-8') as f:
            a = f.read()
            word_dict = eval(a)
        return word_dict

    def load_known_words(self):
        known_words = set()
        with open(self.dict_path, encoding='utf-8') as f:
            for line in f:
                word = line.strip().split(' ')[0]
                known_words.add(word)
        return known_words

    def is_proper_noun(self, word):
        return word in self.known_words

    def edit1(self, word):
        if word in self.cache:
            return self.cache[word]

        n = len(word)
        edits = set()
        for i in range(n):
            edits.add(word[0:i] + word[i+1:])  # 删除
            if i < n-1:
                edits.add(word[0:i] + word[i+1] + word[i] + word[i+2:])  # 调换
            for c in self.charlist:
                edits.add(word[0:i] + c + word[i+1:])  # 替换
                edits.add(word[0:i] + c + word[i:])  # 插入
        self.cache[word] = edits
        return edits


corrector = WordCorrect()

def correct_query(query):
    # 将query转换为拼音
    query_pinyin = ','.join(lazy_pinyin(query))
    print(f"Query: {query}, Pinyin: {query_pinyin}")  # 调试输出拼音
    # 检查是否是term列表中的词
    if corrector.is_proper_noun(query):
        return query, True
    candiwords = corrector.edit1(query)
    # 优先考虑拼音完全匹配的候选词汇
    # 如果拼音存在
    if query_pinyin in corrector.pinyin_dict:
        candidate_words = corrector.pinyin_dict[query_pinyin]
        best_candidate = max(candidate_words, key=candidate_words.get)
        return best_candidate, False
    # 如果没有拼音完全匹配的候选词汇，再考虑编辑距离的候选词汇
    best_candidate = query
    best_score = float('-inf')
    for candidate in candiwords:
        # 将编辑距离为1的候选词汇转换为拼音
        candidate_pinyin = ','.join(lazy_pinyin(candidate))
        candidate_words = corrector.pinyin_dict.get(candidate_pinyin, {})
        for word, count in candidate_words.items():
            score = count  # 仅使用词频作为评分
            if score > best_score:
                best_score = score
                best_candidate = word

    return best_candidate, False


def results(request):
    query = request.GET.get('query', '')
    query_terms = tokenize_content(query)
    print(query_terms)
    corrected_queries = []
    correction_needed = False
    for query_term in query_terms:
        corrected_query_term, is_proper_noun = correct_query(query_term)
        corrected_queries.append(corrected_query_term)
        if not is_proper_noun and corrected_query_term != query_term:
            correction_needed = True

    tokenize_corrected_query = " ".join(corrected_queries)

    start_time = time.time()
    scores = cosine_similarity(tokenize_corrected_query, tfidf, doc_lengths)
    sorted_scores = custom_sort(scores)
    end_time = time.time()

    results_with_snippet = [(extract_first_term_info(doc_id, corrected_queries), doc_urls[str(doc_id)], get_snippet(doc_id, query_terms)) for doc_id, score in sorted_scores[:10]]
    query_time = end_time - start_time
    result_count = len(results_with_snippet)

    response = render(request, 'results.html', {
        'query': query,
        'corrected_query': tokenize_corrected_query if correction_needed else None,
        'results': results_with_snippet,
        'query_time': query_time,
        'result_count': result_count
    })
    return response



def wenxin_result(request):
    query = request.GET.get('query', '')
    return StreamingHttpResponse(stream_wenxin_response(query)(), content_type='text/event-stream')

def extract_first_term_info(doc_id, query_terms):
    """
    提取文档中第一个term的部分信息
    """
    file_path = os.path.join('unified_data', f'{doc_id}.txt')
    if not os.path.exists(file_path):
        return f"Document {doc_id}"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    for first_term in query_terms:
        match = re.search(re.escape(first_term), content, flags=re.IGNORECASE)
        if match:
            start = max(match.start() - 15, 0)
            end = min(match.end() + 15, len(content))
            snippet = content[start:end].replace('\n', ' ')
            snippet = re.sub(f'({re.escape(first_term)})', r'<mark class="highlight">\1</mark>', snippet, flags=re.IGNORECASE)
            return snippet
    return f"Document {doc_id}"