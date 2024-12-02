# openai_service.py
from openai import OpenAI
from typing import Dict, List
from config import OPENAI_API_KEY

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)  # 創建 OpenAI 客戶端

    def generate_job_summary(self, job_data: Dict) -> str:
        """
        生成職位摘要
        """
        # 確保輸入數據可以被序列化
        description = str(job_data.get('description', 'N/A'))
        
        prompt = f"""
        請分析以下職位的工作內容與職責，整合並生成一個簡潔的摘要，並使用條列式表達：

        工作內容: {description}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一個專業的人力資源顧問，善於分析職位信息並提供有見地的總結。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API 調用失敗: {e}")
            return "無法生成摘要"

    def batch_generate_summaries(self, jobs_data: List[Dict]) -> List[Dict]:
        """
        批量生成職位摘要
        """
        summaries = []
        for job in jobs_data:
            summary = self.generate_job_summary(job)
            job_with_summary = job.copy()
            job_with_summary['summary'] = summary
            summaries.append(job_with_summary)
        return summaries
    

