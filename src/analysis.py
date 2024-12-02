from openai_service import OpenAIService

from crawler_104 import get_job_links, get_top_jobs_info, combine_jobs_info


def analyze_requirements(jobs_info_sum, category):
        """
        分析工具和技能的出現頻率及佔比
        
        Args:
            jobs_info_sum: 整合後的職缺信息
            
        Returns:
            dict: 包含工具和技能的分析結果
        """
        def calculate_frequency(items_list):
            # 展平列表並轉換為小寫以進行統一比較
            flat_items = [item.lower() for sublist in items_list for item in sublist]
            # 計算總數
            total_jobs = len(items_list)
            # 計算每個項目出現的次數
            frequency = {}
            for item in set(flat_items):
                count = flat_items.count(item)
                percentage = (count / total_jobs) * 100
                frequency[item] = {
                    'count': count,
                    'percentage': round(percentage, 1)
                }
            # 按照出現次數降序排序
            return dict(sorted(frequency.items(), key=lambda x: x[1]['count'], reverse=True))

        analysis_result = {
            category : calculate_frequency(jobs_info_sum[f'{category}'])
        }
        
        # 打印分析結果
        print(f"\n{category.upper()} 分析結果：")
        for item, stats in analysis_result[category].items():
                print(f"{item}: {stats['count']}次 ({stats['percentage']}%)")
        
        return analysis_result


def analysis(keyword, area):
    
    # 獲取職位數據
    try:
        # 設置搜尋參數
        keyword = keyword #'Data Engineer'
        area = area  # 台北市 '6001001000'
        
        print(f"\n開始搜尋職缺...")
        print(f"關鍵字：{keyword}")
        print(f"地區：台北市")
        
        # 獲取職缺連結
        job_links = get_job_links(keyword, area)
        if not job_links:
            print("未找到符合條件的職缺")
            return
            
        print(f"找到 {len(job_links)} 個職缺連結")
        
        # 獲取所有職缺詳細信息
        print("\n開始獲取職缺詳細信息...")
        all_jobs_info = get_top_jobs_info(job_links)
        
        if not all_jobs_info:
            print("未能成功獲取職缺信息")
            return
            
        print(f"成功獲取 {len(all_jobs_info)} 個職缺信息")
        
        # 整合職缺信息
        print("\n整合職缺信息...")
        jobs_info_sum = combine_jobs_info(all_jobs_info)
        
        # 打印統計信息
        print(jobs_info_sum)
        
    except Exception as e:
        print(f"執行過程中發生錯誤：{e}")
        return None
    
    
    
    # 初始化 OpenAI 服務
    openai_service = OpenAIService()
    
    # 生成摘要
    analysis_job_desc = openai_service.generate_job_summary(jobs_info_sum)


    analysis_job_tools = analyze_requirements(jobs_info_sum, 'tools')
    analysis_job_skills = analyze_requirements(jobs_info_sum, 'skills')

    dict_analysis = {
        'job_desc' : analysis_job_desc,
        'tools' : analysis_job_tools,
        'skills' : analysis_job_skills
    }

    return dict_analysis

if __name__ == "__main__":
    analysis()