import streamlit as st
import statistics
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

def parse_numbers(input_str):
    """解析用户输入的数字"""
    try:
        num_strings = [s.strip() for s in input_str.split(',')]
        num_strings = [s for s in num_strings if s]
        numbers = [float(s) for s in num_strings]
        if len(numbers) == 0:
            return None, "请至少输入一个数字"
        return numbers, None
    except ValueError:
        return None, "格式错误：请输入有效的数字，用逗号分隔"

def calculate_statistics(numbers):
    """计算统计量"""
    stats = {}
    stats['数量'] = len(numbers)
    stats['平均值'] = statistics.mean(numbers)
    stats['中位数'] = statistics.median(numbers)
    stats['最大值'] = max(numbers)
    stats['最小值'] = min(numbers)
    stats['方差'] = statistics.variance(numbers)
    stats['标准差'] = statistics.stdev(numbers)
    return stats

def plot_charts(numbers):
    """绘制图表"""
    fig = plt.figure(figsize=(12, 5))
    
    # 散点图
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.scatter(range(len(numbers)), numbers, color='blue', s=50)
    ax1.set_title('数据分布散点图', fontsize=12)
    ax1.set_xlabel('数据序号', fontsize=10)
    ax1.set_ylabel('数值', fontsize=10)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 直方图
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.hist(numbers, bins='auto', color='green', alpha=0.7)
    ax2.set_title('数据直方图', fontsize=12)
    ax2.set_xlabel('数值', fontsize=10)
    ax2.set_ylabel('频数', fontsize=10)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    return fig

def main():
    st.set_page_config(page_title="数据统计小工具", layout="wide")
    
    st.title("📊 数据统计小工具")
    st.markdown("---")
    
    # 输入区域
    st.subheader("📝 输入数据")
    input_data = st.text_area(
        "请输入一串数字，用逗号分隔",
        placeholder="示例：1,2,3,4,5,6,7,8,9,10\n\n或：10.5,20.3,15.8,25.2,18.9",
        height=100
    )
    
    if st.button("开始计算", type="primary"):
        if not input_data.strip():
            st.error("请输入数据")
            return
        
        numbers, error = parse_numbers(input_data)
        if error:
            st.error(error)
            return
        
        # 计算统计量
        stats = calculate_statistics(numbers)
        
        # 显示结果
        st.markdown("---")
        st.subheader("📈 统计结果")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**数量**: {stats['数量']}")
            st.info(f"**平均值**: {stats['平均值']:.4f}")
        
        with col2:
            st.success(f"**最大值**: {stats['最大值']:.4f}")
            st.warning(f"**最小值**: {stats['最小值']:.4f}")
        
        with col3:
            st.info(f"**方差**: {stats['方差']:.4f}")
            st.info(f"**标准差**: {stats['标准差']:.4f}")
        
        st.markdown("#### 📉 数据可视化")
        st.pyplot(plot_charts(numbers))

if __name__ == "__main__":
    main()