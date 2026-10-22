# -*- coding: utf-8 -*-
"""
第1章 实验二：维度模型（星型模型）演示 —— Power BI 迁移 Python 实现
====================================================================
教材原实现：用 Power BI 加载"商场销售数据表.xlsx"，构建星型维度模型
（事实表 + 多张维度表），并进行销售分析可视化。

项目内涵：
1. 维度模型 = 一张事实表（销售记录，可累加的度量）+ 多张维度表
   （日期、产品、品牌、类别、城市，用于从不同角度切片分析）；
2. 这正是商业数据分析中典型的"星型模型"；
3. Power BI 中维度表通过"一对多(1:*)"关系筛选事实表；
   Python 中用 merge 关联后，按维度 groupby 聚合即可复现同样的分析。

模型结构（星型）：
                 日期表
                   │
  品牌 ── 产品信息表 ── 产品销售数据表（事实表）── 商铺城市
              │
            类别
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# 1. 加载 Excel 中的多张表（对应 Power BI 的"获取数据-Excel"）
# ============================================================
xlsx = os.path.join(DATA_DIR, "商场销售数据表.xlsx")
brand   = pd.read_excel(xlsx, sheet_name="品牌")        # 品牌维度
cate    = pd.read_excel(xlsx, sheet_name="类别")        # 类别维度
city    = pd.read_excel(xlsx, sheet_name="商铺城市")    # 城市维度
product = pd.read_excel(xlsx, sheet_name="产品信息表")  # 产品维度
sales   = pd.read_excel(xlsx, sheet_name="产品销售数据表")  # 事实表
dimdate = pd.read_excel(xlsx, sheet_name="日期表")      # 日期维度

print("各表行数：", {"品牌": len(brand), "类别": len(cate), "商铺城市": len(city),
                 "产品信息表": len(product), "产品销售数据表": len(sales), "日期表": len(dimdate)})

# ============================================================
# 2. 构建星型模型：事实表关联各维度表
#    （对应 Power BI 模型视图中 1:* 的关系连线）
# ============================================================
# 注意：事实表中产品编号为小写（a001），产品信息表中为大写（A001），
# 关联前需统一大小写（这本身也是数据清洗的典型环节）
product["产品编号"] = product["产品编号"].str.upper()
sales["产品编号"] = sales["产品编号"].str.upper()

fact = (sales
        .merge(dimdate, left_on="订单日期", right_on="日期", how="left")
        .merge(product[["产品编号", "产品名称", "品牌名称", "产品类别", "采购单价", "销售单价"]],
               on="产品编号", how="left", suffixes=("", "_产品表")))
print("\n关联后的宽表（事实表 + 维度属性）：")
print(fact.head(3))

# ============================================================
# 3. 按维度切片分析（对应 Power BI 报表页的可视化）
# ============================================================

# 3.1 年度销售趋势（日期维度）
year_sale = fact.groupby("年度")["销售额"].sum()
fig, ax = plt.subplots(figsize=(8, 5))
year_sale.plot(kind="line", marker="o", ax=ax, color="#c62828")
ax.set_title("年度销售总额趋势")
ax.set_ylabel("销售额（元）")
ax.set_xlabel("年度")
ax.yaxis.set_major_formatter(lambda x, _: f"{x/10000:.0f}万")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "01_年度销售趋势.png"), dpi=150)
plt.close()

# 3.2 各产品类别销售额（类别维度）
cate_sale = fact.groupby("产品类别")["销售额"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 5))
cate_sale.plot(kind="bar", ax=ax, color="#1565c0")
ax.set_title("各产品类别销售额")
ax.set_ylabel("销售额（元）")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "02_类别销售额.png"), dpi=150)
plt.close()

# 3.3 各品牌销售占比（品牌维度）
brand_sale = fact.groupby("品牌名称")["销售额"].sum()
fig, ax = plt.subplots(figsize=(6, 5))
brand_sale.plot(kind="pie", autopct="%.1f%%", ax=ax)
ax.set_title("各品牌销售额占比")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "03_品牌销售占比.png"), dpi=150)
plt.close()

# 3.4 各城市销售额 TopN（城市维度）
city_sale = fact.groupby("商铺城市")["销售额"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(9, 5))
city_sale.head(10).plot(kind="barh", ax=ax, color="#6a1b9a")
ax.set_title("销售额 Top10 城市")
ax.set_xlabel("销售额（元）")
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "04_城市销售额Top10.png"), dpi=150)
plt.close()

# ============================================================
# 4. 度量值计算（对应 Power BI 中的 DAX 度量值）
#    总销售额 / 总利润（销售额-成本）/ 利润率
# ============================================================
fact["成本"] = fact["采购单价"] * fact["销售数量"]
fact["利润"] = fact["销售额"] - fact["成本"]

total_sales  = fact["销售额"].sum()
total_profit = fact["利润"].sum()
profit_rate  = total_profit / total_sales

print("\n—— 关键度量值（等价于 Power BI 的 DAX）——")
print(f"总销售额 SUM('销售'[销售额])        = {total_sales:,.0f} 元")
print(f"总利润 SUMX('销售',[销售额]-[成本]) = {total_profit:,.0f} 元")
print(f"利润率 DIVIDE([总利润],[总销售额])  = {profit_rate:.2%}")

# 各品类利润率
cate_profit = fact.groupby("产品类别").agg(销售额=("销售额", "sum"),
                                           利润=("利润", "sum"))
cate_profit["利润率"] = cate_profit["利润"] / cate_profit["销售额"]
print("\n各品类利润率：")
print(cate_profit)

print("\n实验二完成，图表已输出到 output/ 目录")
