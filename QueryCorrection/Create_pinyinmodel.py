import json
from pypinyin import lazy_pinyin

def build_pinyin2word_model(dict_file, model_file):
    pinyin2word = {}

    # 读取 dict.txt 文件
    with open(dict_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 解析每一行，获取词汇和频率
            word, freq = line.strip().split()
            freq = int(freq)
            # 将词汇转换为拼音
            pinyin = ','.join(lazy_pinyin(word))
            # 如果拼音不在字典中，则添加
            if pinyin not in pinyin2word:
                pinyin2word[pinyin] = {}
            # 将词汇和频率添加到对应的拼音映射中
            pinyin2word[pinyin][word] = freq

    # 将结果写入 pinyin2word.model 文件
    with open(model_file, 'w', encoding='utf-8') as f:
        json.dump(pinyin2word, f, ensure_ascii=False, indent=4)

def add_alphabets_to_char_file(char_file):
    # 26个英文字母
    alphabets = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # 读取现有的char.txt文件内容
    with open(char_file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    
    # 将英文字母加入到读取的内容中
    updated_lines = set(lines)  # 使用集合避免重复
    updated_lines.update(alphabets)
    
    # 将更新后的内容写回到char.txt文件
    with open(char_file, 'w', encoding='utf-8') as f:
        for line in sorted(updated_lines):  # 按字母顺序写入文件
            f.write(f"{line}\n")

# 调用函数，将英文字母加入到char.txt文件中
add_alphabets_to_char_file('char.txt')

# 调用函数，构建 pinyin2word.model 文件
build_pinyin2word_model('dict.txt', 'pinyin2word.model')
