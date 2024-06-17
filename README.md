### 项目概述

深圳大学信息检索大作业：搭建了一个基于Django框架的面向教师个人主页的信息检索系统，主要用于检索教师个人主页信息。系统实现了倒排索引、查询纠正、TF-IDF加权和余弦相似度计算等信息检索技术，并支持中文和英文的查询。项目包含网页抓取、分词处理、倒排索引构建、查询搜索、结果排序及展示等功能模块。

### 功能模块

1. **网页抓取**：通过Scraper.py脚本，从以下院校的教师主页抓取相关信息，并存储在本地文件中：
   - 中科院先进院计算机科学与控制工程学院
   - 香港中文大学（深圳）数据科学学院
   - 深圳技术大学互联网与大数据学院
   - 清华大学深圳国际研究生院
   - 哈尔滨工业大学深圳计算机科学与技术学院
   - 南方科技大学计算机科学与工程系

2. **分词处理**：使用结巴分词对抓取到的中文内容进行分词处理，并存储分词结果。

3. **倒排索引**：通过InvertedIndex.py脚本，构建倒排索引，并将索引存储为JSON文件，便于快速检索。

4. **查询搜索**：Query_search.py脚本实现了基于余弦相似度的查询搜索，能够根据用户输入的查询词快速返回相关文档。

5. **查询纠正**：QueryCorrection模块提供查询纠正功能，通过拼音模型纠正用户的拼写错误。

6. **权重计算**：使用TF-IDF作为权重计算查询和文档的相关性，具体公式和计算方法详见项目文档。

7. **结果排序**：根据余弦相似度对匹配到的文档进行排序，并返回前10个相关结果。排序结果包含文档ID、相关性分值和文档内容片段。

8. **用户交互**：提供简洁美观的网页界面，支持用户输入查询词并查看搜索结果。搜索结果页面包括原文片段和高亮显示的查询词，同时支持分页展示搜索结果。

9. **外部API集成**：集成百度文心一言等大模型API，将模型的返回结果展示在搜索结果页面，提供更多维度的信息辅助用户决策。

### 项目特点

- **支持多语言查询**：支持中文和英文的查询，能够处理不同语言的分词和检索。
- **高效的索引和检索**：基于倒排索引和余弦相似度的检索算法，能够快速返回相关文档。
- **用户友好的界面**：提供直观的搜索框和结果展示区域，方便用户进行查询操作。
- **文档高亮**：在搜索结果中高亮显示查询词，便于用户快速定位相关信息。

### 项目依赖

项目依赖以下主要Python包：

- `Django`：用于构建Web应用的框架。
- `requests`：用于HTTP请求。
- `nltk`：用于英文分词和词干提取。
- `jieba`：用于中文分词。
- `selenium`：用于网页抓取。
- `pypinyin`：用于拼音处理。

详细依赖项请参考项目根目录下的`requirements.txt`文件。

### 安装和运行

1. 克隆项目代码：

   ```sh
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
   ```

2. 安装依赖：

   ```sh
   pip install -r requirements.txt
   ```

#### 倒排索引检索功能实现

1. **进入项目根目录**：

2. **运行Scraper.py**：
   ```
   python Scraper.py
   ```
   该脚本会抓取教师主页信息，并在根目录下构建 `data` 和 `tokenized_data` 文件夹。

3. **运行InvertedIndex.py**：
   ```
   python InvertedIndex.py
   ```
   该脚本会生成 `unified_data` 和 `unified_tokenized_data` 文件夹，并构建 `inverted_index.json` 倒排索引表和 `doc_urls.json` 的 docid 和 URL 对应表。

4. **运行Qurry_search.py进行query测试**：
   ```
   python Qurry_search.py
   ```

#### query纠错前期准备

1. **进入QueryCorrection文件夹**：
   ```
   cd QueryCorrection
   ```

2. **运行Create_dict.py** 将 `inverted_index.json` 转换为 `dict.txt`：
   ```
   python Create_dict.py
   ```

3. **运行Create_pinyinmodel.py** 将拼音对应term结果写入 `pinyin2word.model` 文件：
   ```
   python Create_pinyinmodel.py
   ```

#### 启动Django程序

1. **进入search_engine文件夹**：
   ```
   cd search_engine
   ```
2. **将settings.py中的内容进行替换**：
   替换为自己的access_key和secret_key
   ```
   os.environ["QIANFAN_ACCESS_KEY"] = "your_AK"
   os.environ["QIANFAN_SECRET_KEY"] = "your_SK"
   ```

3. **运行Django项目**：
   ```
   python manage.py runserver
   ```

   以上步骤完成后，您可以在浏览器中访问 `http://127.0.0.1:8000/` 进行查询测试。

![image](https://gitee.com/LCZsecretspace/images/raw/master/202406170932681.png)

![image](https://gitee.com/LCZsecretspace/images/raw/master/202406170932113.png)

![image](https://gitee.com/LCZsecretspace/images/raw/master/202406170932165.png)






### 文件结构


|  data                         // 按院校进行分类的原始内容  
|  tokenized_data               // 按院校进行分类的分词内容  
|  unified_data                 // 统一索引的原始内容  
|  unified_tokenized_data       // 统一索引的分词内容和对应url
│  doc_urls.json                // 存储文档ID和对应URL的JSON文件
│  InvertedIndex.py             // 倒排索引的实现代码
│  inverted_index.json          // 倒排索引的JSON文件
│  Query_search.py              // 查询搜索的实现代码
│  README.md                    // 项目说明文档
│  Scraper.py                   // 网页抓取脚本
│
├─chromedriver-win64            // ChromeDriver的文件夹
│      chromedriver.exe         // ChromeDriver可执行文件
│      LICENSE.chromedriver     // ChromeDriver的许可证文件
│
├─QueryCorrection               // 查询纠正模块
│      char.txt                 // 字符文件
│      Create_dict.py           // 创建词典的脚本
│      Create_pinyinmodel.py    // 创建拼音模型的脚本
│      dict.txt                 // 词典文件
│      inverted_index.json      // 查询纠正模块的倒排索引
│      pinyin2word.model        // 拼音到词的模型文件
│
└─search_engine                 // Django项目的根目录
    │  db.sqlite3               // SQLite数据库文件
    │  manage.py                // Django管理脚本
    │  unified_data.zip         // 压缩的统一数据文件
    │
    ├─data                      // 查询纠正数据
    │      char.txt             // 字符文件
    │      dict.txt             // 词典文件
    │      doc_urls.json        // 文档ID和URL的对应文件
    │      inverted_index.json  // 倒排索引文件
    │      pinyin2word.model    // 拼音到词的模型文件
    │
    ├─search                    // Django应用文件夹
    │  │  admin.py              // 管理界面配置文件
    │  │  apps.py               // 应用配置文件
    │  │  models.py             // 数据模型定义文件
    │  │  tests.py              // 测试文件
    │  │  urls.py               // 路由配置文件
    │  │  views.py              // 视图文件
    │  │  __init__.py           // 应用初始化文件
    │
    ├─search_engine             // 项目的核心配置文件夹
    │  │  asgi.py               // ASGI配置文件
    │  │  settings.py           // 项目配置文件
    │  │  urls.py               // 项目路由文件
    │  │  wsgi.py               // WSGI配置文件
    │  │  __init__.py           // 项目初始化文件
    │
    ├─static                    // 静态文件目录
    │      style.css            // 样式文件
    │
    ├─stopwords-master          // 停用词文件夹
    │      baidu_stopwords.txt  // 百度停用词表
    │      cn_stopwords.txt     // 中文停用词表
    │      hit_stopwords.txt    // 哈工大停用词表
    │      README.md            // 停用词说明文档
    │      scu_stopwords.txt    // 四川大学停用词表
    │
    └─templates                 // 模板文件夹
            index.html          // 搜索主页模板
            results.html        // 搜索结果页面模板

