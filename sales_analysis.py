import matplotlib.pyplot as plt
import matplotlib
import operator

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

def get_sales_data():
    while True:
        try:
            input_str = input("请输入销售数据（格式：日期,销售额;日期,销售额...）：\n例如：2026-01,10000;2026-02,12000;2026-03,8000\n")
            sales_data = {}
            # 按分号分割每组数据
            data_groups = input_str.split(';')
            for group in data_groups:
                group = group.strip()
                if not group:
                    continue
                # 按逗号分割日期和销售额
                parts = group.split(',')
                if len(parts) != 2:
                    raise ValueError("格式错误：每组数据应为 日期,销售额")
                date = parts[0].strip()
                amount = float(parts[1].strip())
                sales_data[date] = amount
            
            if len(sales_data) < 2:
                print("错误：至少需要输入两组数据进行分析")
                continue
            return sales_data
        except ValueError as e:
            print(f"错误：{e}，请重新输入")

def calculate_metrics(sales_data):
    metrics = {}
    
    # 按日期排序
    sorted_dates = sorted(sales_data.keys())
    sorted_sales = [sales_data[date] for date in sorted_dates]
    
    # 最高/最低销售额
    max_sales = max(sorted_sales)
    min_sales = min(sorted_sales)
    max_date = [date for date, amount in sales_data.items() if amount == max_sales][0]
    min_date = [date for date, amount in sales_data.items() if amount == min_sales][0]
    
    metrics['最高销售额'] = (max_date, max_sales)
    metrics['最低销售额'] = (min_date, min_sales)
    
    # 环比增长率
    growth_rates = {}
    for i in range(1, len(sorted_dates)):
        prev_sales = sorted_sales[i-1]
        curr_sales = sorted_sales[i]
        rate = ((curr_sales - prev_sales) / prev_sales) * 100
        growth_rates[sorted_dates[i]] = rate
    metrics['环比增长率'] = growth_rates
    
    # Top3月份
    sorted_by_sales = sorted(sales_data.items(), key=operator.itemgetter(1), reverse=True)
    metrics['Top3月份'] = sorted_by_sales[:3]
    
    # 总销售额
    metrics['总销售额'] = sum(sorted_sales)
    
    # 平均销售额
    metrics['平均销售额'] = sum(sorted_sales) / len(sorted_sales)
    
    return metrics, sorted_dates, sorted_sales

def print_analysis(metrics):
    print("\n" + "="*50)
    print("              销售数据分析报告")
    print("="*50)
    
    print(f"\n【总销售额】: {metrics['总销售额']:,.2f} 元")
    print(f"【平均销售额】: {metrics['平均销售额']:,.2f} 元")
    
    print(f"\n【最高销售额】: {metrics['最高销售额'][0]} ({metrics['最高销售额'][1]:,.2f} 元)")
    print(f"【最低销售额】: {metrics['最低销售额'][0]} ({metrics['最低销售额'][1]:,.2f} 元)")
    
    print("\n【环比增长率】:")
    for date, rate in metrics['环比增长率'].items():
        sign = "+" if rate >= 0 else ""
        print(f"  {date}: {sign}{rate:.2f}%")
    
    print("\n【Top 3 销售月份】:")
    for i, (date, amount) in enumerate(metrics['Top3月份'], 1):
        print(f"  第{i}名: {date} ({amount:,.2f} 元)")
    
    print("="*50 + "\n")

def plot_charts(sorted_dates, sorted_sales, sales_data):
    fig = plt.figure(figsize=(15, 10))
    
    # 1. 销售额趋势折线图
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(sorted_dates, sorted_sales, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
    ax1.set_title('销售额趋势折线图', fontsize=12, pad=15)
    ax1.set_xlabel('月份', fontsize=10)
    ax1.set_ylabel('销售额（元）', fontsize=10)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.ticklabel_format(axis='y', style='plain')
    
    # 2. 月度对比柱状图
    ax2 = fig.add_subplot(2, 2, 2)
    bars = ax2.bar(sorted_dates, sorted_sales, color='skyblue', edgecolor='black')
    ax2.set_title('月度销售对比柱状图', fontsize=12, pad=15)
    ax2.set_xlabel('月份', fontsize=10)
    ax2.set_ylabel('销售额（元）', fontsize=10)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.ticklabel_format(axis='y', style='plain')
    # 在柱状图上显示数值
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,.0f}',
                ha='center', va='bottom', fontsize=8)
    
    # 3. 销售占比饼图
    ax3 = fig.add_subplot(2, 1, 2)
    labels = sorted_dates
    sizes = sorted_sales
    explode = [0.05] * len(sizes)  # 稍微分离各个扇形
    
    wedges, texts, autotexts = ax3.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90, textprops={'fontsize': 10})
    
    ax3.set_title('销售占比饼图', fontsize=12, pad=15)
    ax3.axis('equal')  # 保证饼图为正圆形
    
    plt.tight_layout()
    plt.show()

def main():
    print("="*50)
    print("      电商销售数据可视化分析系统")
    print("="*50)
    print("功能：")
    print("  1. 支持输入多组销售数据")
    print("  2. 自动生成趋势折线图、柱状图、饼图")
    print("  3. 输出业务分析报告")
    print("="*50 + "\n")
    
    # 获取销售数据
    sales_data = get_sales_data()
    
    # 计算指标
    metrics, sorted_dates, sorted_sales = calculate_metrics(sales_data)
    
    # 输出分析报告
    print_analysis(metrics)
    
    # 绘制图表
    plot_charts(sorted_dates, sorted_sales, sales_data)

if __name__ == "__main__":
    main()