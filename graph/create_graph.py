import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
def create_graph():
    matplotlib.use('TkAgg')
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    # 1. 读取已有分类的CSV文件
    df = pd.read_csv('after_analysis.csv')

    # 查看数据结构和列名
    print("数据列名:", df.columns.tolist())

    # 2. 绘制饼状图：整体情感分布
    plt.figure(figsize=(14, 6))

    # 子图1：饼状图
    plt.subplot(1, 2, 1)

    # 确保情感分类列存在
    sentiment_col = '情感分类'
    sentiment_counts = df[sentiment_col].value_counts()

    # 定义颜色
    color_map = {
        '正面': '#4CAF50',  # 绿色
        '中性': '#FFC107',  # 黄色
        '负面': '#F44336',  # 红色
    }

    # 为每个类别分配颜色
    colors = [color_map.get(str(x), '#2196F3') for x in sentiment_counts.index]

    wedges, texts, autotexts = plt.pie(
        sentiment_counts.values,
        labels=sentiment_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        explode=[0.05] * len(sentiment_counts),
        shadow=True
    )
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)

    plt.title('评论情感分布', fontsize=14, fontweight='bold', pad=20)
    plt.axis('equal')

    plt.subplot(1, 2, 2)
    gender_col = '性别'
    # 创建透视表（百分比）
    pivot_table = pd.crosstab(
        index=df[gender_col],
        columns=df[sentiment_col],
        normalize='index'
    ) * 100

    # 绘制堆叠柱状图
    bar_width = 0.6
    bottom = np.zeros(len(pivot_table))

    for i, sentiment in enumerate(pivot_table.columns):
        values = pivot_table[sentiment].values
        color = color_map.get(str(sentiment), '#2196F3')

        plt.bar(
            range(len(pivot_table)),
            values,
            bar_width,
            bottom=bottom,
            label=sentiment,
            color=color,
            edgecolor='white',
            alpha=0.8
        )

        # 添加百分比标签
        for j, val in enumerate(values):
            if val > 5:  # 只显示大于5%的标签
                plt.text(
                    j,
                    bottom[j] + val/2,
                    f'{val:.0f}%',
                    ha='center',
                    va='center',
                    color='white' if val > 30 else 'black',
                    fontsize=9
                )
        bottom += values

    plt.xticks(range(len(pivot_table)), pivot_table.index)
    plt.xlabel('性别')
    plt.ylabel('比例 (%)')
    plt.title('性别与情感分布', fontsize=14, fontweight='bold', pad=20)
    plt.legend(title='情感分类', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.ylim(0, 100)
    plt.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    plt.savefig('result.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("\n" + "="*50)
    print("数据统计摘要")
    print("="*50)
    print(f"总评论数: {len(df)}")
    print(f"性别分布:\n{df[gender_col].value_counts()}")
    print(f"\n情感分布:\n{sentiment_counts}")
    print(f"\n性别-情感交叉表(百分比):")
    print(pivot_table.round(1))

if __name__ == '__main__':

    create_graph()