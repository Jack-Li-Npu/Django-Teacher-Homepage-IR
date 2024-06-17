from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

import nltk
import re
import jieba
# 下载punkt数据包，用于英文分词
# nltk.download('punkt')

class Scraper:
    def __init__(self, driver_path):
        """
        初始化新闻爬取类
        :param driver_path: ChromeDriver路径
        :param url: 目标页面URL
        """
        # options = webdriver.ChromeOptions()
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        # self.driver = webdriver.Chrome(executable_path=driver_path, options=options)
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.url1 = 'https://www.siat.ac.cn/college/jsjkz/szdw/'
        self.url2 = "https://sds.cuhk.edu.cn/"
        self.url3 = "https://bdi.sztu.edu.cn/"
        self.url4 = "https://www.sigs.tsinghua.edu.cn/1378/list.htm"
        self.url5 = "http://cs.hitsz.edu.cn/"
        self.url6 = "https://cse.sustech.edu.cn/"
        self.url7 = "https://ise.sysu.edu.cn/"
        self.url8 = "https://csse.szu.edu.cn/"
        self.data = []
        self.department1 = "中科院先进院计算机科学与控制工程学院"
        self.department2 = "香港中文大学（深圳）数据科学学院"
        self.department3 = "深圳技术大学互联网与大数据学院"
        self.department4 = "清华大学深圳国际研究生院"
        self.department5 = "哈尔滨工业大学深圳计算机科学与技术学院"
        self.department6 = "南方科技大学计算机科学与工程系"
        # 均访问不了
        self.department7 = "中山大学（深圳）智能工程学院"
        self.department8 = "深圳大学计算机与软件学院"
        # self.doc_id = 488  # 全局递增的文档ID



    def fetch_all(self):
        # self.fetch_ZKY()
        # self.fetch_CUHK()
        self.fetch_SZTU()
        # self.fetch_TsingHua()
        # self.fetch_HITSZ()
        # self.fetch_SUS() 
        # self.fetch_SYSU()
        # self.fetch_SZU()

    def save_content(self, content, index, department):
        """
        保存原始文档
        """
        directory = f"data/{department}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        # 保存原始内容
        with open(f"{directory}/{index}.txt", 'w', encoding='utf-8') as f:
            f.write(content)

    def save_tokenized_content(self, tokenized_content, index, department, url):
        """
        保存分词后内容和对应的跳转链接
        """
        tokenized_directory = f"tokenized_data/{department}"
        if not os.path.exists(tokenized_directory):
            os.makedirs(tokenized_directory)
        # 保存分词后的内容
        with open(f"{tokenized_directory}/{index}.txt", 'w', encoding='utf-8') as f:
            f.write('\n'.join(tokenized_content))
        with open(f"{tokenized_directory}/url_{index}.txt", 'w', encoding='utf-8') as f:
            f.write(url)
    
    def tokenize_content(self, content):
        """
        分别进行中英文分词
        """
        stemmer = PorterStemmer()
        chinese_content = ''.join(re.findall(r'[\u4e00-\u9fff]+', content))
        english_content = ' '.join(re.findall(r'[a-zA-Z]+', content))
        tokenized_content = []
        if chinese_content:
            tokenized_content.append(' '.join(jieba.lcut(chinese_content, cut_all=False)))
        if english_content:
            english_tokens = word_tokenize(english_content)
            tokenized_content.append(' '.join([stemmer.stem(word) for word in english_tokens]))
        return tokenized_content

    def fetch_ZKY(self):
        """
        获取中科院链接并抓取内容
        """
        self.driver.get(self.url1)
        for index in range(1, 11):  
            try:
                xpath = f'/html/body/div[2]/table/tbody/tr/td[2]/div/div[3]/div[2]/ul/li[{index}]/div[2]/h2/a'
                link = self.driver.find_element(By.XPATH, xpath)
                url1 = link.get_attribute('href')
                self.driver.get(url1)
                time.sleep(0.15)
                content_element = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div')  # 获取页面所有文本内容
                content = content_element.text
                # 保存原始内容
                self.save_content(content, self.doc_id, self.department1)
                # 分词并保存
                tokenized_content = self.tokenize_content(content)
                self.save_tokenized_content(tokenized_content, self.doc_id, self.department1,url1)
                self.driver.back()  # 回退到上一个页面
                time.sleep(0.15)  # 等待页面加载
                self.doc_id += 1
            except Exception as e:
                break

    def fetch_CUHK(self):
        """
        获取港中深链接并抓取内容
        """
        self.driver.get(self.url2)
        link = self.driver.find_element(By.XPATH, "/html/body/div/div[1]/div[1]/div/div/div/div/div/div/ul/li[3]/a")
        url2 = link.get_attribute('href')
        self.driver.get(url2)
        xpaths = [
            "/html/body/div/div[1]/div[2]/div[4]/div/div[2]/div/div/div/div[11]/div/ul/li[1]/a",
            "/html/body/div/div[1]/div[2]/div[4]/div/div[2]/div/div/div/div[11]/div/ul/li[2]/a",
            "/html/body/div/div[1]/div[2]/div[4]/div/div[2]/div/div/div/div[11]/div/ul/li[5]/a",
            "/html/body/div/div[1]/div[2]/div[4]/div/div[2]/div/div/div/div[11]/div/ul/li[6]/a",
            "/html/body/div/div[1]/div[2]/div[4]/div/div[2]/div/div/div/div[11]/div/ul/li[7]/a",
            "/html/body/div/div[1]/div[2]/div[4]/div/div[2]/div/div/div/div[11]/div/ul/li[7]/a",
            "/html/body/div/div[1]/div[2]/div[4]/div/div[2]/div/div/div/div[11]/div/ul/li[7]/a",
            "/html/body/div/div[1]/div[2]/div[4]/div/div[2]/div/div/div/div[11]/div/ul/li[8]/a"
        ]
        for xpath in xpaths:
            link = self.driver.find_element(By.XPATH, xpath)
            url = link.get_attribute('href')
            self.driver.get(url)
            time.sleep(0.2)
            for index in range(1, 11):  
                try:
                    xpath = f'/html/body/div/div[1]/div[2]/div[4]/div/div[2]/div/div/div/div[{index}]/div[2]/div[1]/a'
                    link = self.driver.find_element(By.XPATH, xpath)
                    url2 = link.get_attribute('href')
                    self.driver.get(url2)
                    time.sleep(0.2)
                    content_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div/article/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div')  # 获取页面所有文本内容
                    content = content_element.text
                    # 保存原始内容
                    self.save_content(content, self.doc_id, self.department2)
                    # 分词并保存
                    tokenized_content = self.tokenize_content(content)
                    self.save_tokenized_content(tokenized_content, self.doc_id, self.department2, url2)
                    self.driver.back()  # 回退到上一个页面
                    time.sleep(0.2)  # 等待页面加载
                    self.doc_id += 1
                except Exception as e:
                    print(e)
                    break
    
    def fetch_SZTU(self):
        # self.driver.get("https://bdi.sztu.edu.cn/szdw/jytd/js.htm")
        # for index in range(1, 18):
        #     try:
        #         xpath = f"/html/body/div[4]/div[4]/div[3]/div/div/div[1]/div/div[{index}]/a"
        #         link = self.driver.find_element(By.XPATH, xpath)
        #         url = link.get_attribute('href')
        #         self.driver.get(url)
        #         content_element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[4]/div[3]/div/div/div[2]")
        #         time.sleep(2)
        #         content = content_element.text
        #         self.save_content(content, self.doc_id, self.department3)
        #         # 分词并保存
        #         tokenized_content = self.tokenize_content(content)
        #         self.save_tokenized_content(tokenized_content, self.doc_id, self.department3, url)
        #         self.driver.back()  # 回退到上一个页面
        #         time.sleep(0.15)  # 等待页面加载
        #         self.doc_id += 1
        #     except Exception as e:
        #         print(e)
        #         self.driver.back()
        #         continue
        # self.driver.get("https://bdi.sztu.edu.cn/szdw/jytd/fjs.htm")
        # for index in range(1, 19):
        #     try:
        #         xpath = f"/html/body/div[4]/div[4]/div[3]/div/div/div[1]/div/div[{index}]/a"
        #         link = self.driver.find_element(By.XPATH, xpath)
        #         url = link.get_attribute('href')
        #         self.driver.get(url)
        #         content_element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[4]/div[3]/div/div/div[2]")
        #         time.sleep(2)
        #         content = content_element.text
        #         self.save_content(content, self.doc_id, self.department3)
        #         # 分词并保存
        #         tokenized_content = self.tokenize_content(content)
        #         self.save_tokenized_content(tokenized_content, self.doc_id, self.department3, url)
        #         self.driver.back()  # 回退到上一个页面
        #         time.sleep(0.15)  # 等待页面加载
        #         self.doc_id += 1
        #     except Exception as e:
        #         print(e)
        #         self.driver.back()
        #         continue
        # time.sleep(2)
        # xpath = "/html/body/div[4]/div[4]/div[3]/div/div/div[2]/span/span[5]/a"
        # link = self.driver.find_element(By.XPATH, xpath)
        # url = link.get_attribute('href')
        # self.driver.get(url)
        # for index in range(1, 9):
        #     try:
        #         xpath = f"/html/body/div[4]/div[4]/div[3]/div/div/div[1]/div/div[{index}]/a"
        #         link = self.driver.find_element(By.XPATH, xpath)
        #         url = link.get_attribute('href')
        #         self.driver.get(url)
        #         content_element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[4]/div[3]/div/div/div[2]")
        #         time.sleep(2)
        #         content = content_element.text
        #         self.save_content(content, self.doc_id, self.department3)
        #         # 分词并保存
        #         tokenized_content = self.tokenize_content(content)
        #         self.save_tokenized_content(tokenized_content, self.doc_id, self.department3, url)
        #         self.driver.back()  # 回退到上一个页面
        #         time.sleep(0.15)  # 等待页面加载
        #         self.doc_id += 1
        #     except Exception as e:
        #         print(e)
        #         self.driver.back()
        #         continue
        self.driver.get("https://bdi.sztu.edu.cn/szdw/jytd/zljs.htm")
        for i in range(3):
            if i != 2:
                for index in range(1, 19):
                    try:
                        xpath = f"/html/body/div[4]/div[4]/div[3]/div/div/div[1]/div/div[{index}]/a"
                        link = self.driver.find_element(By.XPATH, xpath)
                        url = link.get_attribute('href')
                        self.driver.get(url)
                        content_element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[4]/div[3]/div/div/div[2]")
                        time.sleep(2)
                        content = content_element.text
                        self.save_content(content, self.doc_id, self.department3)
                        # 分词并保存
                        tokenized_content = self.tokenize_content(content)
                        self.save_tokenized_content(tokenized_content, self.doc_id, self.department3, url)
                        self.driver.back()  # 回退到上一个页面
                        time.sleep(0.15)  # 等待页面加载
                        self.doc_id += 1
                    except Exception as e:
                        print(e)
                        self.driver.back()
                        continue
                time.sleep(2)
                xpath = "/html/body/div[4]/div[4]/div[3]/div/div/div[2]/span/span[6]/a"
                link = self.driver.find_element(By.XPATH, xpath)
                url = link.get_attribute('href')
                self.driver.get(url)
            else:
                for index in range(1, 7):
                    try:
                        xpath = f"/html/body/div[4]/div[4]/div[3]/div/div/div[1]/div/div[{index}]/a"
                        link = self.driver.find_element(By.XPATH, xpath)
                        url = link.get_attribute('href')
                        self.driver.get(url)
                        content_element = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[4]/div[3]/div/div/div[2]")
                        time.sleep(2)
                        content = content_element.text
                        self.save_content(content, self.doc_id, self.department3)
                        # 分词并保存
                        tokenized_content = self.tokenize_content(content)
                        self.save_tokenized_content(tokenized_content, self.doc_id, self.department3, url)
                        self.driver.back()  # 回退到上一个页面
                        time.sleep(0.15)  # 等待页面加载
                        self.doc_id += 1
                    except Exception as e:
                        print(e)
                        self.driver.back()
                        continue
    
    def fetch_TsingHua(self):
        self.driver.get(self.url4)
        link = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]/div[2]/a")
        url = link.get_attribute('href')
        self.driver.get(url)
        for div_index in range(1, 27):
            if div_index not in [2, 9, 21]:
                index = 1
                while True:
                    xpath = f'/html/body/div[5]/div/div/ul/div[{div_index}]/ul/li[{index}]/a'
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                        )
                        link = self.driver.find_element(By.XPATH, xpath)
                        url = link.get_attribute('href')
                        self.driver.get(url)
                        time.sleep(0.5)
                        try:
                            content_element1 = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div[2]')
                            content = content_element1.text
                            content_element2 = self.driver.find_element(By.XPATH, '/html/body/div[4]')
                            content += content_element2.text
                            self.save_content(content, self.doc_id, self.department4)
                            # 分词并保存
                            tokenized_content = self.tokenize_content(content)
                            self.save_tokenized_content(tokenized_content, self.doc_id, self.department4, url)
                            time.sleep(0.15)  # 等待页面加载
                        except Exception as e:
                            print(f"Error fetching content: {e}")
                            continue
                        self.doc_id += 1
                        index += 1
                        self.driver.back()  # 回退到上一个页面
                        time.sleep(0.15)  # 等待页面加载
                    except Exception as e:
                        print(f"Error finding link at index {index}: {e}")
                        break

    def fetch_HITSZ(self):
        self.driver.get(self.url5)
        link = self.driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul/li[4]/a")
        url = link.get_attribute('href')
        self.driver.get(url)
        for index in range(1, 97):
            try:
                xpath = f'/html/body/div[3]/div/main/div[2]/div[{index}]/div/a'
                link = self.driver.find_element(By.XPATH, xpath)
                url = link.get_attribute('href')
                self.driver.get(url)
                content_element = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[5]/div/div[1]/div[2]/div[1]')  # 获取页面所有文本内容
                content = content_element.text
                # 保存原始内容
                self.save_content(content, self.doc_id, self.department5)
                # 分词并保存
                tokenized_content = self.tokenize_content(content)
                self.save_tokenized_content(tokenized_content, self.doc_id, self.department5, url)
                self.driver.back()  # 回退到上一个页面
                time.sleep(0.15)  # 等待页面加载
                self.doc_id += 1
            except Exception as e:
                # 有些个人主页不太一样
                print(e)
                self.driver.back()  # 回退到上一个页面
                time.sleep(0.15)  # 等待页面加载
                continue
    
    # 南科大
    def fetch_SUS(self):
        # 因为太分散，所以直接截取body的文字内容
        self.driver.get(self.url6)
        link = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/ul/li[3]/a")
        url = link.get_attribute('href')
        self.driver.get(url)
        xpath = f"/html/body/div[4]/div/div/div/div[1]/ul/li[1]/a"
        link = self.driver.find_element(By.XPATH, xpath)
        url = link.get_attribute('href')
        self.driver.get(url)
        # for index in range(4, 13):
        #     try:
        #         xpath = f"/html/body/div[4]/div/div/div/div[2]/div[{index}]/div[2]/b[4]/a"
        #         link = self.driver.find_element(By.XPATH, xpath)
        #         url = link.get_attribute('href')
        #         self.driver.get(url)
        #         content_element = self.driver.find_element(By.XPATH, "/html/body")
        #         content = content_element.text
        #         self.save_content(content, self.doc_id, self.department6)
        #         # 分词并保存
        #         tokenized_content = self.tokenize_content(content)
        #         self.save_tokenized_content(tokenized_content, self.doc_id, self.department6, url)
        #         self.driver.back()  # 回退到上一个页面
        #         time.sleep(0.15)  # 等待页面加载
        #         self.doc_id += 1
        #     except Exception as e:
        #         print(e)
        #         self.driver.back()
        #         continue
        self.driver.get("https://cse.sustech.edu.cn/cn/people/tenure/type/associate_professor")
        for index in range(12, 17):
            try:
                xpath = f"/html/body/div[4]/div/div/div/div[2]/div[{index}]/div[2]/b[4]/a"
                link = self.driver.find_element(By.XPATH, xpath)
                url = link.get_attribute('href')
                self.driver.get(url)
                content_element = self.driver.find_element(By.XPATH, "/html/body")
                content = content_element.text
                self.save_content(content, self.doc_id, self.department6)
                # 分词并保存
                tokenized_content = self.tokenize_content(content)
                self.save_tokenized_content(tokenized_content, self.doc_id, self.department6, url)
                self.driver.back()  # 回退到上一个页面
                time.sleep(0.15)  # 等待页面加载
                self.doc_id += 1
            except Exception as e:
                print(e)
                self.driver.back()
                continue
        self.driver.get("https://cse.sustech.edu.cn/cn/people/tenure/type/assistant_professor")
        for index in range(2, 9):
            try:
                xpath = f"/html/body/div[4]/div/div/div/div[2]/div[{index}]/div[2]/b[4]/a"
                link = self.driver.find_element(By.XPATH, xpath)
                url = link.get_attribute('href')
                self.driver.get(url)
                content_element = self.driver.find_element(By.XPATH, "/html/body")
                content = content_element.text
                self.save_content(content, self.doc_id, self.department6)
                # 分词并保存
                tokenized_content = self.tokenize_content(content)
                self.save_tokenized_content(tokenized_content, self.doc_id, self.department6, url)
                self.driver.back()  # 回退到上一个页面
                time.sleep(0.15)  # 等待页面加载
                self.doc_id += 1
            except Exception as e:
                print(e)
                self.driver.back()
                continue
            

    def fetch_SYSU(self):
        self.driver.get("https://ise.sysu.edu.cn/teacher/teacher01/1414803.htm")
        xpath = "/html/body/div[2]/div/div/ul/li[3]/a"
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        link = self.driver.find_element(By.XPATH, xpath)
        url1 = link.get_attribute('href')
        self.driver.get(url1)
        for index1 in range(11, 7):
            # xpath = f"/html/body/div[3]/div[1]/div/ul/li[{index1}]/a"
            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, xpath))
            # )
            # link = self.driver.find_element(By.XPATH, xpath)
            # url2 = link.get_attribute('href')
            # self.driver.get(url2)
            index = 1
            while True:
                xpath = f'/html/body/div[3]/div[2]/div[2]/ul/li[{index}]/a'
                try:
                    link = self.driver.find_element(By.XPATH, xpath)
                    url = link.get_attribute('href')
                    self.driver.get(url)
                    time.sleep(0.5)
                    try:
                        content_element1 = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]')
                        content = content_element1.text
                        self.save_content(content, self.doc_id, self.department7)
                        # 分词并保存
                        tokenized_content = self.tokenize_content(content)
                        self.save_tokenized_content(tokenized_content, self.doc_id, self.department7, url)
                        time.sleep(0.15)  # 等待页面加载
                        self.doc_id += 1
                    except Exception as e:
                        print(f"Error fetching content: {e}")
                        continue
                    index += 1
                    self.driver.back()  # 回退到上一个页面
                    time.sleep(0.15)  # 等待页面加载
                except Exception as e:
                    print(f"Error finding link at index {index}: {e}")
                    break
        time.sleep(5)

    def fetch_SZU(self):
        self.driver.get(self.url8)
        xpath = "/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div[4]/a"
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        link = self.driver.find_element(By.XPATH, xpath)
        url1 = link.get_attribute('href')
        self.driver.get(url1)
        for index1 in range(2, 7):
            # xpath = f"/html/body/div[3]/div[1]/div/ul/li[{index1}]/a"
            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, xpath))
            # )
            # link = self.driver.find_element(By.XPATH, xpath)
            # url2 = link.get_attribute('href')
            # self.driver.get(url2)
            index = 1
            while True:
                xpath = f'/html/body/div[3]/div[2]/div[2]/ul/li[{index}]/a'
                try:
                    link = self.driver.find_element(By.XPATH, xpath)
                    url = link.get_attribute('href')
                    self.driver.get(url)
                    time.sleep(0.5)
                    try:
                        content_element1 = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]')
                        content = content_element1.text
                        self.save_content(content, self.doc_id, self.department7)
                        # 分词并保存
                        tokenized_content = self.tokenize_content(content)
                        self.save_tokenized_content(tokenized_content, self.doc_id, self.department7, url)
                        time.sleep(0.15)  # 等待页面加载
                        self.doc_id += 1
                    except Exception as e:
                        print(f"Error fetching content: {e}")
                        continue
                    index += 1
                    self.driver.back()  # 回退到上一个页面
                    time.sleep(0.15)  # 等待页面加载
                except Exception as e:
                    print(f"Error finding link at index {index}: {e}")
                    break

    def close(self):
        """
        关闭浏览器
        """
        self.driver.quit()



driver_path = './chromedriver-win64/chromedriver.exe'  # chromedriver路径

# 初始化并运行爬虫
scraper = Scraper(driver_path)
scraper.fetch_all()
scraper.close()

