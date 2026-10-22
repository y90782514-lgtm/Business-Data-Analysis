# -*- coding: utf-8 -*-
"""
第1章 实验（附）：sale.csv 简单数据分析
========================================
sale.csv 是章节根目录的配套练习数据，字段：year, market, sale, profit。
用于演示最基础的数据读取、聚合与可视化（Excel 透视的 Python 等价实现）。
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(DATA_DIR, "sale.csv"), encoding="gbk")
df.columns = ["年度", "市场", "销售额", "利润"]
print(df.head())
print("\n数据概览：")
print(df.describe())

# 按年份透视：各市场销售额（等价于 Excel 数据透视表）
pivot = df.pivot_table(index="年度", columns="市场", values="销售额", aggfunc="sum")
print("\n各年度各市场销售额透视表：")
print(pivot)

fig, ax = plt.subplots(figsize=(8, 5))
pivot.plot(kind="bar", ax=ax)
ax.set_title("各年度各市场销售额")
ax.set_ylabel("销售额")
ax.set_xlabel("年度")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "05_sale各市场销售额.png"), dpi=150)
plt.close()

# 利润率对比
df["利润率"] = df["利润"] / df["销售额"]
market_rate = df.groupby("市场")["利润率"].mean()
fig, ax = plt.subplots(figsize=(6, 5))
market_rate.plot(kind="bar", ax=ax, color="#ef6c00")
ax.set_title("各市场平均利润率")
ax.set_ylabel("利润率")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "06_sale各市场利润率.png"), dpi=150)
plt.close()

print("\n附加实验完成")
