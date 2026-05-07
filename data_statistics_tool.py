import statistics
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

def get_numbers_input():
    while True:
        try:
            input_str = input("请输入一串数字，用逗号分隔：")
            # 去除空格并按逗号分割
            num_strings = [s.strip() for s in input_str.split(',')]
            # 过滤空字符串
            num_strings = [s for s in num_strings if s]
            # 转换为数字列表
            numbers = [float(s) for s in num_strings]
            if len(numbers) == 0:
                print("错误：请至少输入一个数字")
                continue
            return numbers
        except ValueError:
            print("错误：请输入有效的数字，用逗号分隔")

def calculate_statistics(numbers):
    stats = {}
    stats['数量'] = len(numbers)
    stats['平均值'] = statistics.mean(numbers)
    stats['中位数'] = statistics.median(numbers)
    stats['最大值'] = max(numbers)
    stats['最小值'] = min(numbers)
    stats['方差'] = statistics.variance(numbers)
    stats['标准差'] = statistics.stdev(numbers)
    return stats

def print_results(stats):
    print("\n" + "="*40)
    print("         数据统计结果")
    print("="*40)
    for key, value in stats.items():
        print(f"{key:^10}: {value:.4f}")
    print("="*40 + "\n")

def plot_chart(numbers):
    plt.figure(figsize=(10, 6))
    
    # 绘制数据点
    plt.subplot(1, 2, 1)
    plt.scatter(range(len(numbers)), numbers, color='blue', s=50)
    plt.title('数据分布散点图')
    plt.xlabel('数据序号')
    plt.ylabel('数值')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 绘制直方图
    plt.subplot(1, 2, 2)
    plt.hist(numbers, bins='auto', color='green', alpha=0.7)
    plt.title('数据直方图')
    plt.xlabel('数值')
    plt.ylabel('频数')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()

def main():
    print("="*40)
    print("      数据统计小工具")
    print("="*40)
    print("功能：计算平均值、中位数、最大值、最小值、方差、标准差")
    print("="*40 + "\n")
    
    # 获取输入数据
    numbers = get_numbers_input()
    
    # 计算统计量
    stats = calculate_statistics(numbers)
    
    # 输出结果
    print_results(stats)
    
    # 绘制图表
    plot_chart(numbers)

if __name__ == "__main__":
    main()