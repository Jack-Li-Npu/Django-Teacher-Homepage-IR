import json
from collections import defaultdict
import math
import time

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


def main():
    index_filename = "inverted_index.json"

    inverted_index = InvertedIndex()
    inverted_index.load_index(index_filename)
    
    # 加载文档长度信息
    with open(index_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    doc_lengths = defaultdict(int)
    for term, info in data.items():
        if isinstance(info, dict) and 'docs' in info:
            for doc_id, doc_info in info['docs'].items():
                doc_lengths[int(doc_id)] += doc_info['freq']

    tfidf = compute_tfidf(inverted_index.index, doc_lengths)

    query = """潘毅"""
    start_time = time.time()
    scores = cosine_similarity(query, tfidf, doc_lengths)
    results = custom_sort(scores)
    end_time = time.time()

    print(f"Query time: {end_time - start_time:.2f} seconds")
    for doc_id, score in results[:10]:
        print(f"Document: {doc_id}, Score: {score}")

if __name__ == "__main__":
    main()
