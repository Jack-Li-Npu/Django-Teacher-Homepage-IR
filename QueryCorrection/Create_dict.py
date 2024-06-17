import json

def convert_inverted_index_to_dict_txt(json_file, output_file):
    # 读取倒排索引 JSON 文件
    with open(json_file, 'r', encoding='utf-8') as f:
        inverted_index = json.load(f)
    
    # 打开输出文件 dict.txt
    with open(output_file, 'w', encoding='utf-8') as f:
        # 遍历每个 term 及其对应的数据
        for term, data in inverted_index.items():
            # 计算每个 term 的总频率
            total_freq = sum(doc['freq'] for doc in data['docs'].values())
            # 写入 dict.txt 文件，格式为 "term total_freq"
            f.write(f"{term} {total_freq}\n")

# 调用函数，将 inverted_index.json 转换为 dict.txt
convert_inverted_index_to_dict_txt('./inverted_index.json', 'dict.txt')





