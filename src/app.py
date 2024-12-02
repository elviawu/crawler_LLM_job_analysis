# src/app.py
import streamlit as st
import plotly.express as px
import pandas as pd
from analysis import analysis, analyze_requirements



st.set_page_config(
    page_title="104職缺分析工具",
    page_icon="../img/img_104.png",
    layout="centered",  # 使用置中布局
    initial_sidebar_state="auto", 
    menu_items=None,
)
           
st.title(":grey[104職缺分析]")
st.write(":grey[輸入職缺關鍵字，讓AI分析幫你職缺技能]")

# 主要輸入區域
with st.container():
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    # 職缺關鍵字輸入
    keyword = st.text_input(
        "請輸入職缺關鍵字",
        value="Data Engineer",
        help="例如：Data Engineer、Python Developer"
    )

    # 地區選擇
    area_code = st.selectbox(
        "選擇地區",
        options=[
            ("6001001000", "台北市"),
            ("6001002000", "新北市"),
            ("6001003000", "宜蘭縣"),
            ("6001004000", "基隆市"),
            ("6001005000", "桃園市"),
            ("6001006000", "新竹縣市"),
            ("6001007000", "苗栗縣"),
            ("6001008000", "台中市"),
            ("6001010000", "彰化縣"),
            ("6001011000", "南投縣"),
            ("6001012000", "雲林縣"),
            ("6001013000", "嘉義縣市"),
            ("6001014000", "台南市"),
            ("6001016000", "高雄市"),
            ("6001018000", "屏東縣"),
            ("6001019000", "台東縣"),
            ("6001020000", "花蓮縣"),
            ("6001021000", "澎湖縣"),
            ("6001022000", "金門縣"),
            ("6001023000", "連江縣")
        ],
        format_func=lambda x: x[1]
    )

# 分析按鈕
if st.button("開始分析", key="analyze_button"):
    with st.spinner("正在分析職缺資料..."):
        try:
            result = analysis(keyword, area_code[0])
            
            if result:
                # 顯示職位描述摘要
                st.markdown("### 職位描述摘要")
                st.markdown(result['job_desc'])
                
                # 工具分析圖表
                st.markdown("### 工具需求分析")
                tools_data = pd.DataFrame([
                    {"tool": tool, "percentage": stats["percentage"]}
                    for tool, stats in result['tools']['tools'].items()
                ])
                if not tools_data.empty:
                    tools_data = tools_data.sort_values('percentage', ascending=False)
                    fig = px.bar(
                        tools_data,
                        y="tool",
                        x="percentage",
                        text=tools_data["percentage"].apply(lambda x: f'{x:.1f}%'),
                        orientation='h'
                    )
                    # 調整圖表樣式
                    fig.update_traces(
                        textposition='outside', # 自動調整文字位置
                        marker_color='#FECDA6',  # 設定bar顏色
                        marker_line_color='rgba(0,0,0,0)',  # 設定bar邊框顏色為透明
                        width=0.8  # 設定bar寬度
                    )  
                    fig.update_layout(
                        yaxis={'categoryorder': 'total ascending'},  # 確保順序正確
                        xaxis_title="使用比例 (%)",
                        yaxis_title="工具名稱",
                        bargap=0.5  # 設定bar之間的間距
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # 技能分析圖表
                st.markdown("### 技能需求分析")
                skills_data = pd.DataFrame([
                    {"skill": skill, "percentage": stats["percentage"]}
                    for skill, stats in result['skills']['skills'].items()
                ])
                if not skills_data.empty:
                    skills_data = skills_data.sort_values('percentage', ascending=False)
                    fig = px.bar(
                        skills_data,
                        y="skill",
                        x="percentage",
                        text=skills_data["percentage"].apply(lambda x: f'{x:.1f}%'),
                        orientation='h'
                    )
                    # 調整圖表樣式
                    fig.update_traces(
                        textposition='outside', # 自動調整文字位置
                        marker_color='#FECDA6',  # 設定bar顏色
                        marker_line_color='rgba(0,0,0,0)',  # 設定bar邊框顏色為透明
                        marker_line_width=0.8  # 設定bar邊框寬度
                    )  
                    fig.update_layout(
                        yaxis={'categoryorder': 'total ascending'},  # 確保順序正確
                        xaxis_title="使用比例 (%)",
                        yaxis_title="技能名稱",
                        bargap=0.5  # 設定bar之間的間距
                    )
                    st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"分析過程中發生錯誤：{str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# 頁腳
st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: #666;">
    Powered by OpenAI GPT-3.5
</div>
""", unsafe_allow_html=True)

