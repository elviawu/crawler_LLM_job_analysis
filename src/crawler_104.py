import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def setup_driver():
    """設置並返回WebDriver"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-notifications')
    return webdriver.Chrome(options=options)

def get_job_links(keyword, area, page=1):
    """
    獲取職缺連結列表
    
    Args:
        keyword (str): 搜尋關鍵字
        area (str): 地區代碼
        page (int): 頁碼
        
    Returns:
        list: 職缺連結列表
    """
    keyword = '+'.join(keyword.split())
    url = f'https://www.104.com.tw/jobs/search/?keyword={keyword}&mode=s&order=15&page={page}&jobsource=joblist_search&area={area}'
    
    driver = setup_driver()
    job_links = []
    
    try:
        driver.get(url)
        time.sleep(2)
        
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")
        
        for link in soup.find_all('a', class_="info-job__text"):
            href = link.get('href')
            if href:
                job_links.append(href)
                
        return job_links
        
    finally:
        driver.quit()

def get_job_description(soup):
    """獲取工作描述"""
    try:
        description = soup.find('div', class_='job-description')
        return description.text.strip() if description else None
    except Exception as e:
        print(f"獲取工作描述時發生錯誤：{e}")
        return None

def get_job_requirements(soup, job_data):
    """
    獲取職缺要求
    
    Args:
        soup: BeautifulSoup對象
        job_data: 要搜尋的資料類型
        
    Returns:
        list: 要求列表
    """
    try:
        # 找到條件要求的區塊
        req_section = soup.find('h3', class_='h3', string=job_data)
        if not req_section:
            return []
            
        # 找到工具列表
        req_container = req_section.parent.find_next_sibling('div', class_='col p-0 list-row__data')
        if not req_container:
            return []
            
        # 找到第一個工具連結中的u標籤，獲取其data-v屬性
        first_req = req_container.find('u')
        if not first_req:
            return []
            
        # 獲取data-v屬性名稱
        data_v_attr = None
        for attr in first_req.attrs:
            if attr.startswith('data-v-'):
                data_v_attr = attr
                break
                
        if not data_v_attr:
            # 如果沒有找到data-v屬性，使用備選方案
            reqs = req_container.find_all('u')
        else:
            # 使用找到的data-v屬性
            reqs = req_container.find_all('u', attrs={data_v_attr: ""})
        
        # 提取工具名稱
        req_names = [req.text.strip() for req in reqs if req.text.strip()]
        
        return req_names
        
    except Exception as e:
        print(f"提取{job_data}時發生錯誤：{e}")
        return []

def get_job_other_conditions(soup):
    """獲取其他條件"""
    try:
        # 找到條件要求的區塊
        con_section = soup.find('div', class_='job-requirement-table__data')
        if not con_section:
            print(f"未找到其他條件區塊")
            return []
            
        # 找到內容容器
        con_container = con_section.find('p', class_='m-0 r3 w-100')
        if not con_container:
            print(f"未找到其他條件容器")
            return []
        
        conditions = con_container.text.replace('\n', '').replace('-', '').strip()
        if not conditions:
            print(f"未找到其他條件")
            return []
        
        else:
            return conditions
        
    except Exception as e:
        print(f"提取其他條件時發生錯誤：{e}")
        return []

def get_job_details(link, driver=None):
    """
    獲取單個職缺詳細信息
    
    Args:
        link: 職缺連結
        driver: WebDriver實例（可選）
        
    Returns:
        dict: 職缺詳細信息
    """
    job_info = {
        'title': None,
        'description': None,
        'tools': None,
        'skills': None,
        'certificates': None,
        #'other_conditions': None
    }
    
    should_quit_driver = False
    try:
        if driver is None:
            driver = setup_driver()
            should_quit_driver = True
            
        driver.get(link)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "job-description"))
        )
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # 獲取各項信息
        title_element = soup.find('h1', class_='d-inline')
        if title_element:
            job_info['title'] = title_element.get('title', '').strip()
            
        job_info['description'] = get_job_description(soup)
        job_info['tools'] = get_job_requirements(soup, '擅長工具')
        job_info['skills'] = get_job_requirements(soup, '工作技能')
        job_info['certificates'] = get_job_requirements(soup, '具備證照')
        job_info['other_conditions'] = get_job_other_conditions(soup)
        
        return job_info
        
    except Exception as e:
        print(f"獲取職缺詳細信息時發生錯誤：{e}")
        return job_info
    finally:
        if should_quit_driver and driver:
            driver.quit()

def get_top_jobs_info(job_links):
    """
    獲取所有職缺信息
    
    Args:
        job_links: 職缺連結列表
        
    Returns:
        list: 職缺信息列表
    """
    driver = setup_driver()
    all_jobs_info = []
    
    try:
        for i, link in enumerate(job_links[:10], 1):
            print(f"\n處理第 {i}/10 個職缺...")
            job_info = get_job_details(link, driver)
            if job_info['title']:
                all_jobs_info.append(job_info)
                print(f"成功獲取職缺信息：{job_info['title']}")
            else:
                print(f"跳過無效職缺：{link}")
            time.sleep(1)  # 避免請求過於頻繁
            
        return all_jobs_info
        
    finally:
        driver.quit()

def combine_jobs_info(all_jobs_info):
    """
    整合所有職缺信息
    
    Args:
        all_jobs_info: 職缺信息列表
        
    Returns:
        dict: 整合後的職缺信息
    """
    jobs_info_sum = {
        'title': [],
        'description': [],
        'tools': [],
        'skills': [],
        'certificates': [],
        'other_conditions': []
    }
    
    for job_info in all_jobs_info:
        for key in jobs_info_sum.keys():
            value = job_info.get(key)
            if value and (isinstance(value, list) and value or not isinstance(value, list)):
                jobs_info_sum[key].append(value)
    
    return jobs_info_sum

def print_jobs_info(jobs_info_sum):
    """打印職缺信息統計"""
    print("\n職缺信息統計：")
    print("-" * 50)
    for key, values in jobs_info_sum.items():
        print(f"\n{key}:")
        print(f"總數：{len(values)}")
        if isinstance(values[0], list):
            # 統計列表類型的數據
            all_items = [item for sublist in values for item in sublist]
            unique_items = set(all_items)
            print(f"唯一值：{len(unique_items)}")
            for item in sorted(unique_items):
                count = all_items.count(item)
                print(f"  - {item}: {count}次")
        else:
            # 統計字串類型的數據
            unique_values = set(values)
            print(f"唯一值：{len(unique_values)}")
    print("-" * 50)

if __name__ == "__main__":
    try:
        # 搜尋參數
        keyword_insert = 'Data Engineer'
        
        # 獲取職缺連結
        print(f"搜尋關鍵字：{keyword_insert}")
        job_links = get_job_links(keyword_insert)
        print(f"找到 {len(job_links)} 個職缺連結")
        
        # 獲取所有職缺信息
        all_jobs_info = get_top_jobs_info(job_links)
        print(f"成功獲取 {len(all_jobs_info)} 個職缺信息")
        
        # 整合職缺信息
        jobs_info_sum = combine_jobs_info(all_jobs_info)
        
        # 打印統計信息
        print_jobs_info(jobs_info_sum)
        
    except Exception as e:
        print(f"程式執行時發生錯誤：{e}")