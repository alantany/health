import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import io

# 设置页面配置
st.set_page_config(page_title="COVID-19国家数据分析", layout="wide")

# 数据加载函数
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    response = requests.get(url)
    if response.status_code == 200:
        data = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        st.success("数据加载成功")
        return data
    else:
        st.error(f"数据加载失败: {response.status_code}")
        return pd.DataFrame()

# 加载数据
full_data = load_data()

# 页面标题
st.title("COVID-19国家数据分析平台")

if full_data.empty:
    st.warning("没有数据可以显示。请检查数据源或网络连接。")
else:
    # 选择国家
    countries = sorted(full_data['location'].unique())
    selected_country = st.selectbox("选择一个国家进行详细分析", countries)

    # 只过滤选定国家的数据
    data = full_data[full_data['location'] == selected_country].copy()

    # 数据概览
    st.header("数据概览")
    st.write(f"国家: {selected_country}")
    st.write(f"数据时间范围: 从 {data['date'].min()} 到 {data['date'].max()}")

    # 显示所选国家的数据趋势
    st.header(f"{selected_country}的COVID-19数据趋势")

    # 新增病例趋势
    st.subheader("每日新增病例")
    chart_type = st.selectbox("选择图表类型 (新增病例)", ["柱状图", "折线图", "散点图", "饼图", "箱线图", "热力图", "面积图", "直方图"])
    if chart_type == "柱状图":
        fig = px.bar(data, x='date', y='new_cases', title=f"{selected_country}的每日新增病例")
    elif chart_type == "折线图":
        fig = px.line(data, x='date', y='new_cases', title=f"{selected_country}的每日新增病例")
    elif chart_type == "散点图":
        fig = px.scatter(data, x='date', y='new_cases', title=f"{selected_country}的每日新增病例")
    elif chart_type == "饼图":
        fig = px.pie(data, values='new_cases', names='date', title=f"{selected_country}的每日新增病例")
    elif chart_type == "箱线图":
        fig = px.box(data, x='date', y='new_cases', title=f"{selected_country}的每日新增病例")
    elif chart_type == "热力图":
        fig = px.density_heatmap(data, x='date', y='new_cases', title=f"{selected_country}的每日新增病例")
    elif chart_type == "面积图":
        fig = px.area(data, x='date', y='new_cases', title=f"{selected_country}的每日新增病例")
    else:  # 直方图
        fig = px.histogram(data, x='new_cases', title=f"{selected_country}的每日新增病例分布")
    st.plotly_chart(fig)

    # 累计病例趋势
    st.subheader("累计病例")
    chart_type = st.selectbox("选择图表类型 (累计病例)", ["柱状图", "折线图", "散点图", "饼图", "箱线图", "热力图", "面积图", "直方图"])
    if chart_type == "柱状图":
        fig = px.bar(data, x='date', y='total_cases', title=f"{selected_country}的累计病例")
    elif chart_type == "折线图":
        fig = px.line(data, x='date', y='total_cases', title=f"{selected_country}的累计病例")
    elif chart_type == "散点图":
        fig = px.scatter(data, x='date', y='total_cases', title=f"{selected_country}的累计病例")
    elif chart_type == "饼图":
        fig = px.pie(data, values='total_cases', names='date', title=f"{selected_country}的累计病例")
    elif chart_type == "箱线图":
        fig = px.box(data, x='date', y='total_cases', title=f"{selected_country}的累计病例")
    elif chart_type == "热力图":
        fig = px.density_heatmap(data, x='date', y='total_cases', title=f"{selected_country}的累计病例")
    elif chart_type == "面积图":
        fig = px.area(data, x='date', y='total_cases', title=f"{selected_country}的累计病例")
    else:  # 直方图
        fig = px.histogram(data, x='total_cases', title=f"{selected_country}的累计病例分布")
    st.plotly_chart(fig)

    # 死亡率趋势
    st.subheader("死亡率趋势")
    data['death_rate'] = (data['total_deaths'] / data['total_cases'] * 100).fillna(0)
    chart_type = st.selectbox("选择图表类型 (死亡率)", ["柱状图", "折线图", "散点图", "饼图", "箱线图", "热力图", "面积图", "直方图"])
    if chart_type == "柱状图":
        fig = px.bar(data, x='date', y='death_rate', title=f"{selected_country}的死亡率趋势")
    elif chart_type == "折线图":
        fig = px.line(data, x='date', y='death_rate', title=f"{selected_country}的死亡率趋势")
    elif chart_type == "散点图":
        fig = px.scatter(data, x='date', y='death_rate', title=f"{selected_country}的死亡率趋势")
    elif chart_type == "饼图":
        fig = px.pie(data, values='death_rate', names='date', title=f"{selected_country}的死亡率趋势")
    elif chart_type == "箱线图":
        fig = px.box(data, x='date', y='death_rate', title=f"{selected_country}的死亡率趋势")
    elif chart_type == "热力图":
        fig = px.density_heatmap(data, x='date', y='death_rate', title=f"{selected_country}的死亡率趋势")
    elif chart_type == "面积图":
        fig = px.area(data, x='date', y='death_rate', title=f"{selected_country}的死亡率趋势")
    else:  # 直方图
        fig = px.histogram(data, x='death_rate', title=f"{selected_country}的死亡率分布")
    st.plotly_chart(fig)

    # 疫苗接种情况
    if 'people_vaccinated_per_hundred' in data.columns:
        st.subheader("疫苗接种率")
        chart_type = st.selectbox("选择图表类型 (疫苗接种)", ["柱状图", "折线图", "散点图", "饼图", "箱线图", "热力图", "面积图", "直方图"])
        if chart_type == "柱状图":
            fig = px.bar(data, x='date', y='people_vaccinated_per_hundred', title=f"{selected_country}的疫苗接种率")
        elif chart_type == "折线图":
            fig = px.line(data, x='date', y='people_vaccinated_per_hundred', title=f"{selected_country}的疫苗接种率")
        elif chart_type == "散点图":
            fig = px.scatter(data, x='date', y='people_vaccinated_per_hundred', title=f"{selected_country}的疫苗接种率")
        elif chart_type == "饼图":
            fig = px.pie(data, values='people_vaccinated_per_hundred', names='date', title=f"{selected_country}的疫苗接种率")
        elif chart_type == "箱线图":
            fig = px.box(data, x='date', y='people_vaccinated_per_hundred', title=f"{selected_country}的疫苗接种率")
        elif chart_type == "热力图":
            fig = px.density_heatmap(data, x='date', y='people_vaccinated_per_hundred', title=f"{selected_country}的疫苗接种率")
        elif chart_type == "面积图":
            fig = px.area(data, x='date', y='people_vaccinated_per_hundred', title=f"{selected_country}的疫苗接种率")
        else:  # 直方图
            fig = px.histogram(data, x='people_vaccinated_per_hundred', title=f"{selected_country}的疫苗接种率分布")
        st.plotly_chart(fig)

    # 全球数据比较
    st.header("全球数据比较")

    # 获取最新有效数据
    latest_data = full_data[~full_data['location'].isin(['World', 'International', 'European Union', 'Asia', 'Europe', 'European Union (27)', 'High-income countries', 'Upper-middle-income countries'])]
    latest_data = latest_data.sort_values('date', ascending=False).groupby('location').first().reset_index()

    st.write(f"数据更新日期范围: 从 {latest_data['date'].min()} 到 {latest_data['date'].max()}")
    st.write(f"分析的国家/地区数量: {len(latest_data)}")

    # 总病例数前10的国家
    st.subheader("总病例数前10的国家")
    chart_type = st.selectbox("选择图表类型 (总病例数)", ["柱状图", "折线图", "散点图", "饼图", "箱线图", "热力图", "面积图", "直方图"])
    top_10_cases = latest_data.nlargest(10, 'total_cases')
    if chart_type == "柱状图":
        fig = px.bar(top_10_cases, x='location', y='total_cases', title="总病例数前10的国家")
    elif chart_type == "折线图":
        fig = px.line(top_10_cases, x='location', y='total_cases', title="总病例数前10的国家")
    elif chart_type == "散点图":
        fig = px.scatter(top_10_cases, x='location', y='total_cases', title="总病例数前10的国家")
    elif chart_type == "饼图":
        fig = px.pie(top_10_cases, values='total_cases', names='location', title="总病例数前10的国家")
    elif chart_type == "箱线图":
        fig = px.box(top_10_cases, x='location', y='total_cases', title="总病例数前10的国家")
    elif chart_type == "热力图":
        fig = px.density_heatmap(top_10_cases, x='location', y='total_cases', title="总病例数前10的国家")
    elif chart_type == "面积图":
        fig = px.area(top_10_cases, x='location', y='total_cases', title="总病例数前10的国家")
    else:  # 直方图
        fig = px.histogram(top_10_cases, x='total_cases', title="总病例数前10的国家分布")
    st.plotly_chart(fig)

    # 每百万人口病例数前10的国家
    st.subheader("每百万人口病例数前10的国家")
    chart_type = st.selectbox("选择图表类型 (每百万人口病例数)", ["柱状图", "折线图", "散点图", "饼图", "箱线图", "热力图", "面积图", "直方图"])
    top_10_cases_per_million = latest_data.nlargest(10, 'total_cases_per_million')
    if chart_type == "柱状图":
        fig = px.bar(top_10_cases_per_million, x='location', y='total_cases_per_million', title="每百万人口病例数前10的国家")
    elif chart_type == "折线图":
        fig = px.line(top_10_cases_per_million, x='location', y='total_cases_per_million', title="每百万人口病例数前10的国家")
    elif chart_type == "散点图":
        fig = px.scatter(top_10_cases_per_million, x='location', y='total_cases_per_million', title="每百万人口病例数前10的国家")
    elif chart_type == "饼图":
        fig = px.pie(top_10_cases_per_million, values='total_cases_per_million', names='location', title="每百万人口病例数前10的国家")
    elif chart_type == "箱线图":
        fig = px.box(top_10_cases_per_million, x='location', y='total_cases_per_million', title="每百万人口病例数前10的国家")
    elif chart_type == "热力图":
        fig = px.density_heatmap(top_10_cases_per_million, x='location', y='total_cases_per_million', title="每百万人口病例数前10的国家")
    elif chart_type == "面积图":
        fig = px.area(top_10_cases_per_million, x='location', y='total_cases_per_million', title="每百万人口病例数前10的国家")
    else:  # 直方图
        fig = px.histogram(top_10_cases_per_million, x='total_cases_per_million', title="每百万人口病例数前10的国家分布")
    st.plotly_chart(fig)

    # 显示部分原始数据
    st.write("原始数据示例（前5行）:")
    st.write(latest_data.head())

    # 全球地图可视化
    st.subheader("全球COVID-19病例分布")
    map_data = latest_data[['location', 'total_cases', 'total_cases_per_million']]
    fig = px.choropleth(map_data, 
                        locations="location", 
                        locationmode="country names",
                        color="total_cases",
                        hover_name="location",
                        color_continuous_scale="Viridis",
                        title="全球COVID-19总病例分布")
    st.plotly_chart(fig)

    # 3D散点图
    st.subheader("3D视图：总病例、每百万人口病例数和死亡率")
    fig = px.scatter_3d(latest_data, 
                        x='total_cases', 
                        y='total_cases_per_million', 
                        z='total_deaths_per_million',
                        color='location',
                        hover_name='location',
                        title="3D视图：总病例、每百万人口病例数和死亡率")
    st.plotly_chart(fig)

    # 动态时间序列图
    st.subheader("动态时间序列：每日新增病例")
    top_10_countries = latest_data.nlargest(10, 'total_cases')['location'].tolist()
    time_series_data = full_data[full_data['location'].isin(top_10_countries)]

    # 填充 NaN 值
    time_series_data['new_cases'] = time_series_data['new_cases'].fillna(0)

    # 创建一个新的列作为大小参数，确保没有负值
    time_series_data['size'] = time_series_data['new_cases'].clip(lower=0) + 1

    # 计算大小的范围
    size_min = 5
    size_max = 30
    size_range = time_series_data['size'].max() - time_series_data['size'].min()
    time_series_data['normalized_size'] = (time_series_data['size'] - time_series_data['size'].min()) / size_range * (size_max - size_min) + size_min

    fig = px.scatter(time_series_data, 
                     x="date", 
                     y="new_cases",
                     color="location",
                     size="normalized_size",  # 使用新创建的 'normalized_size' 列
                     hover_name="location",
                     animation_frame="date",
                     animation_group="location",
                     range_y=[0, time_series_data['new_cases'].max()],
                     title="动态时间序列：每日新增病例（前10个国家）")

    st.plotly_chart(fig)

    # 交互式仪表板
    st.subheader("交互式仪表板")
    dashboard_data = latest_data.nlargest(10, 'total_cases')
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=("总病例数", "每百万人口病例数", "总死亡数", "死亡率"))
    
    fig.add_trace(go.Bar(x=dashboard_data['location'], y=dashboard_data['total_cases'], name="总病例数"),
                  row=1, col=1)
    fig.add_trace(go.Bar(x=dashboard_data['location'], y=dashboard_data['total_cases_per_million'], name="每百万人口病例数"),
                  row=1, col=2)
    fig.add_trace(go.Bar(x=dashboard_data['location'], y=dashboard_data['total_deaths'], name="总死亡数"),
                  row=2, col=1)
    fig.add_trace(go.Bar(x=dashboard_data['location'], y=dashboard_data['total_deaths'] / dashboard_data['total_cases'] * 100, name="死亡率"),
                  row=2, col=2)
    
    fig.update_layout(height=800, title_text="COVID-19 数据仪表板（前10个国家）")
    st.plotly_chart(fig)

# 显示数据来源
st.markdown("数据来源: [Our World in Data](https://github.com/owid/covid-19-data)")