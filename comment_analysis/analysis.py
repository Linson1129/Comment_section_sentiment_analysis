import pandas as pd
from snownlp import SnowNLP
def analysis():
    # 1. 读取你的CSV文件
    df = pd.read_csv('comment.csv')

    # 2. 定义情感分析函数
    def analyze_sentiment(text):
        try:
            # SnowNLP情感值范围0-1，越接近1越积极
            return SnowNLP(text).sentiments
        except:
            return 0.5  # 分析失败时返回中性值

    # 3. 应用分析，生成新列
    df['情感得分'] = df['评论内容'].apply(analyze_sentiment)

    # 4. 情感分类（可根据情况调整阈值）
    def classify_sentiment(score):
        if score > 0.6:
            return '正面'
        elif score < 0.4:
            return '负面'
        else:
            return '中性'
    df['情感分类'] = df['情感得分'].apply(classify_sentiment)

    # 5. 计算加权情感指数（简单示例：情感分*点赞数）
    df['情感加权'] = df['情感得分'] * df['点赞数']
    weighted_sentiment_index = df['情感加权'].sum() / df['点赞数'].sum()

    print(f"整体加权情感指数为：{weighted_sentiment_index:.4f}")
    print(df['情感分类'].value_counts())

    # 6. 保存结果到新CSV
    df.to_csv('after_analysis.csv', index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    analysis()