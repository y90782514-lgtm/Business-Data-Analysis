# 第1章 数据分析思维

教材以 Power BI / Excel 实现的案例，迁移为 Python（pandas + matplotlib）实现。

## 实验清单

| 实验 | 教材原实现 | Python 迁移要点 |
|---|---|---|
| 实验一 关系模型 | Power BI 加载 8 张银行表建立 E-R 关系，分析信用卡类型与持卡人性别 | `merge` 实现"主键-外键"关联；内连接排除 Power BI 全外连接产生的"空白"组 |
| 实验二 维度模型 | Power BI 构建星型模型（销售事实表 + 日期/产品/品牌/类别/城市维度） | 事实表关联多张维度表，按维度 `groupby` 聚合；度量值等价于聚合计算 |
| 实验三 sale 分析 | Excel 数据透视表 | `pivot_table` |

## 目录

```
第1章_数据分析思维/
├── 实验一_关系模型.py
├── 实验二_维度模型.py
├── 实验三_sale数据分析.py
├── data/        教材配套数据
└── output/      运行生成的图表
```

## 运行

```bash
python 实验一_关系模型.py
python 实验二_维度模型.py
python 实验三_sale数据分析.py
```
