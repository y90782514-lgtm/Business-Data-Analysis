# -*- coding: utf-8 -*-
"""
第1章 实验一：关系模型（E-R模型）演示 —— Power BI 迁移 Python 实现
====================================================================
教材原实现：用 Power BI 加载银行数据集的 8 张表，建立表间关系（E-R 图），
并演示跨表分析（信用卡类型 与 持卡人性别 的关系）。

项目内涵：
1. 关系模型通过"主键-外键"将多张表关联，形成一个整体的数据网络；
2. Power BI 中"多对一(*:1)"关系，在 Python 中对应 pandas 的 merge 连接；
3. Power BI 中跨表的可视化（如 card 的 type 按 clients 的 sex 计数），
   在 Python 中需要先 merge 关联，再 groupby 聚合，最后绘图。

表关系（对应教材 Power BI 中的 E-R 图）：
    clients --1:N-- disp --N:1-- accounts --1:N-- loans
                    disp --1:N-- card
    accounts --1:N-- order / trans
    clients/accounts --N:1-- district
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]   # 中文显示
plt.rcParams["axes.unicode_minus"] = False

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT_DIR, exist_ok=True)

# 所有 CSV 均为 GBK 编码
ENC = "gbk"


def load(name):
    return pd.read_csv(os.path.join(DATA_DIR, name), encoding=ENC)


# ============================================================
# 1. 加载 8 张表（对应 Power BI 的"获取数据"）
# ============================================================
accounts = load("accounts.csv")    # 账户表（主键 account_id）
clients  = load("clients.csv")     # 客户表（主键 client_id）
disp     = load("disp.csv")        # 处置权限表（连接客户与账户的桥梁）
card     = load("card.csv")        # 信用卡表（外键 disp_id）
district = load("district.csv")    # 地区统计表（主键 A1 即 district_id）
loans    = load("loans.csv")       # 贷款表（外键 account_id）
order    = load("order.csv")       # 永久订单表（外键 account_id）
trans    = load("trans.csv")       # 交易流水表（外键 account_id，大表）

print("各表行数：")
for name, df in [("accounts", accounts), ("clients", clients), ("disp", disp),
                 ("card", card), ("district", district), ("loans", loans),
                 ("order", order), ("trans", trans)]:
    print(f"  {name:<10} {len(df):>8} 行, 列: {list(df.columns)}")

# ============================================================
# 2. 建立表间关系（对应 Power BI 的"管理关系"）
#    Power BI：accounts[district_id] *:1 district[A1]
#              clients[district_id]  *:1 district[A1]
#    Python：  merge(on=关联键)
# ============================================================
print("\n—— 演示：账户表连接地区表（accounts *:1 district）——")
acc_dist = accounts.merge(district, left_on="district_id", right_on="A1")
print(acc_dist[["account_id", "district_id", "A10", "A11"]].head())

print("\n—— 演示：客户-权限-账户 三表连接（教材 Power BI E-R 图的核心链路）——")
client_account = (clients.merge(disp, on="client_id")
                         .merge(accounts, on="account_id", suffixes=("_客户", "_账户")))
print(client_account[["client_id", "sex", "account_id", "type", "frequency"]].head())

# ============================================================
# 3. 跨表分析：信用卡类型 与 持卡人性别 的关系
#    （对应教材 Power BI 报表页的堆积柱形图：
#      X 轴 = card.type，Y 轴 = sex 的计数，图例 = sex）
# ============================================================
# disp 表也有一列 type（所有者/用户），与卡的 type 重名，
# 连接时只取 disp_id 与 client_id 两个关键列，避免列名冲突
card_sex = (card.merge(disp[["disp_id", "client_id"]], on="disp_id")
                .merge(clients, on="client_id"))

# Power BI 默认是全连接，没有信用卡的客户会出现"空白"组；
# 我们不关注该组，因此用内连接（how="inner"）直接排除。
pivot = card_sex.pivot_table(index="type", columns="sex",
                             values="card_id", aggfunc="count", fill_value=0)
print("\n信用卡类型 × 持卡人性别 计数表：")
print(pivot)

fig, ax = plt.subplots(figsize=(8, 5))
pivot.plot(kind="bar", stacked=True, ax=ax,
           color=["#1f4db5", "#4a90e2"])
ax.set_title("信用卡类型与持卡人性别的分析（Power BI 报表复现）")
ax.set_xlabel("卡类型")
ax.set_ylabel("sex 的计数")
ax.legend(title="sex")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "01_信用卡类型与性别.png"), dpi=150)
plt.close()

# ============================================================
# 4. 更多跨表分析示例（加深对关系模型的理解）
# ============================================================
# 4.1 各地区贷款金额（loans *:1 accounts *:1 district）
loan_region = (loans.merge(accounts, on="account_id")
                    .merge(district, left_on="district_id", right_on="A1"))
top_region = (loan_region.groupby("A1")["amount"].sum()
                         .sort_values(ascending=False).head(10))
fig, ax = plt.subplots(figsize=(8, 5))
top_region.plot(kind="bar", ax=ax, color="#2e7d32")
ax.set_title("贷款总额 Top10 地区（地区编号 A1）")
ax.set_xlabel("地区编号")
ax.set_ylabel("贷款总额")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "02_各地区贷款总额.png"), dpi=150)
plt.close()

# 4.2 贷款状态分布（status: A=正常归还, B=有欠款, C/D=坏账等）
fig, ax = plt.subplots(figsize=(6, 5))
loans["status"].value_counts().plot(kind="pie", autopct="%.1f%%", ax=ax)
ax.set_title("贷款状态分布")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "03_贷款状态分布.png"), dpi=150)
plt.close()

print("\n实验一完成，图表已输出到 output/ 目录")
