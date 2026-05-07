import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
import operator

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

def parse_sales_data(input_str):
    """解析用户输入的销售数据"""
    sales_data = {}
    try:
        data_groups = input_str.split(';')
        for group in data_groups:
            group = group.strip()
            if not group:
                continue
            parts = group.split(',')
            if len(parts) != 2:
                return None, "格式错误：每组数据应为 日期,销售额"
            date = parts[0].strip()
            amount = float(parts[1].strip())
            sales_data[date] = amount
        
        if len(sales_data) < 2:
            return None, "至少需要输入两组数据进行分析"
        
        return sales_data, None
    except ValueError:
        return None, "格式错误：销售额应为数字"

def calculate_metrics(sales_data):
    """计算销售指标"""
    metrics = {}
    
    sorted_dates = sorted(sales_data.keys())
    sorted_sales = [sales_data[date] for date in sorted_dates]
    
    max_sales = max(sorted_sales)
    min_sales = min(sorted_sales)
    max_date = [date for date, amount in sales_data.items() if amount == max_sales][0]
    min_date = [date for date, amount in sales_data.items() if amount == min_sales][0]
    
    metrics['最高销售额'] = (max_date, max_sales)
    metrics['最低销售额'] = (min_date, min_sales)
    
    growth_rates = {}
    for i in range(1, len(sorted_dates)):
        prev_sales = sorted_sales[i-1]
        curr_sales = sorted_sales[i]
        rate = ((curr_sales - prev_sales) / prev_sales) * 100
        growth_rates[sorted_dates[i]] = rate
    metrics['环比增长率'] = growth_rates
    
    sorted_by_sales = sorted(sales_data.items(), key=operator.itemgetter(1), reverse=True)
    metrics['Top3月份'] = sorted_by_sales[:3]
    
    metrics['总销售额'] = sum(sorted_sales)
    metrics['平均销售额'] = sum(sorted_sales) / len(sorted_sales)
    
    return metrics, sorted_dates, sorted_sales

def plot_trend_chart(sorted_dates, sorted_sales):
    """绘制趋势折线图"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sorted_dates, sorted_sales, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
    ax.set_title('销售额趋势折线图', fontsize=14)
    ax.set_xlabel('月份', fontsize=12)
    ax.set_ylabel('销售额（元）', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.ticklabel_format(axis='y', style='plain')
    return fig

def plot_bar_chart(sorted_dates, sorted_sales):
    """绘制柱状图"""
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(sorted_dates, sorted_sales, color='skyblue', edgecolor='black')
    ax.set_title('月度销售对比柱状图', fontsize=14)
    ax.set_xlabel('月份', fontsize=12)
    ax.set_ylabel('销售额（元）', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.ticklabel_format(axis='y', style='plain')
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,.0f}', ha='center', va='bottom', fontsize=10)
    return fig

def plot_pie_chart(sorted_dates, sorted_sales):
    """绘制饼图"""
    fig, ax = plt.subplots(figsize=(8, 8))
    explode = [0.05] * len(sorted_sales)
    ax.pie(sorted_sales, explode=explode, labels=sorted_dates, autopct='%1.1f%%',
           shadow=True, startangle=90, textprops={'fontsize': 10})
    ax.set_title('销售占比饼图', fontsize=14)
    ax.axis('equal')
    return fig

def main():
    st.set_page_config(page_title="电商销售数据分析系统", layout="wide")
    
    st.title("📊 电商销售数据可视化分析系统")
    st.markdown("---")
    
    # 输入区域
    st.subheader("📝 输入销售数据")
    input_data = st.text_area(
        "请输入销售数据",
        placeholder="格式：日期,销售额;日期,销售额...\n\n示例：\n2026-01,10000;2026-02,12000;2026-03,8000;2026-04,15000;2026-05,11000;2026-06,18000",
        height=150
    )
    
    if st.button("开始分析", type="primary"):
        if not input_data.strip():
            st.error("请输入销售数据")
            return
        
        sales_data, error = parse_sales_data(input_data)
        if error:
            st.error(error)
            return
        
        # 计算指标
        metrics, sorted_dates, sorted_sales = calculate_metrics(sales_data)
        
        # 显示分析报告
        st.markdown("---")
        st.subheader("📈 业务分析报告")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**总销售额**: ¥{metrics['总销售额']:,.2f}")
            st.info(f"**平均销售额**: ¥{metrics['平均销售额']:,.2f}")
        
        with col2:
            st.success(f"**最高销售额**: {metrics['最高销售额'][0]} (¥{metrics['最高销售额'][1]:,.2f})")
            st.warning(f"**最低销售额**: {metrics['最低销售额'][0]} (¥{metrics['最低销售额'][1]:,.2f})")
        
        # 环比增长率
        st.markdown("#### 📊 环比增长率")
        growth_data = []
        for date, rate in metrics['环比增长率'].items():
            sign = "+" if rate >= 0 else ""
            growth_data.append({"月份": date, "增长率": f"{sign}{rate:.2f}%"})
        
        st.table(growth_data)
        
        # Top3月份
        st.markdown("#### 🏆 Top 3 销售月份")
        for i, (date, amount) in enumerate(metrics['Top3月份'], 1):
            st.markdown(f"**第{i}名**: {date} — ¥{amount:,.2f}")
        
        # 图表展示
        st.markdown("---")
        st.subheader("📉 数据可视化图表")
        
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(plot_trend_chart(sorted_dates, sorted_sales))
        with col2:
            st.pyplot(plot_bar_chart(sorted_dates, sorted_sales))
        
        st.pyplot(plot_pie_chart(sorted_dates, sorted_sales))

if __name__ == "__main__":
    main()