# CDA一级认证教材《商业数据分析》实验仓库

将教材中以 Power BI / Excel 实现的案例迁移为 Python 实现（pandas + matplotlib），
每个实验脚本保留对教材原分析逻辑的对照说明，用于理解数据模型内涵。

## 目录结构

```
├── README.md
├── requirements.txt
└── chapter01/                    第1章 数据分析思维
    ├── 实验一_关系模型.py        Power BI 关系模型演示 → pandas merge + 可视化
    ├── 实验二_维度模型.py        Power BI 维度(星型)模型演示 → 事实表关联维度表分析
    ├── 实验三_sale数据分析.py    Excel 透视表练习 → pandas pivot_table
    ├── data/                     教材配套数据
    └── output/                   运行生成的图表
```

## 实验内容

### 第1章 数据分析思维

| 实验 | 教材原实现 | Python 迁移要点 |
|---|---|---|
| 实验一 关系模型 | Power BI 加载 8 张银行表建立 E-R 关系，分析信用卡类型与持卡人性别 | `merge` 实现"主键-外键"关联；内连接排除 Power BI 全外连接产生的"空白"组 |
| 实验二 维度模型 | Power BI 构建星型模型（销售事实表 + 日期/产品/品牌/类别/城市维度） | 事实表关联多张维度表，按维度 `groupby` 聚合；度量值等价于聚合计算 |
| 实验三 sale 分析 | Excel 数据透视表 | `pivot_table` |

## 运行环境

- Python 3.12（本地 conda 环境 `data_visualization`）
- 安装依赖：`pip install -r requirements.txt`

## 运行方式

```bash
cd chapter01
python 实验一_关系模型.py
python 实验二_维度模型.py
python 实验三_sale数据分析.py
```

图表输出至 `chapter01/output/`。

## 说明

- 数据 CSV 为 GBK 编码，脚本中已用 `encoding="gbk"` 读取
- 数据版权归教材《CDA一级认证教材：商业数据分析》配套资源所有，仅用于学习
