# 商业数据分析（Business Data Analysis）

> 本仓库是我的数据分析学习与实践作品集，包含两部分内容：
> ① 教材案例的 Python 复现；② 期末大作业（数据分析实战项目）。

## 仓库导航

```
Business-Data-Analysis/
├── README.md             ← 你在这里
├── requirements.txt      ← Python 依赖清单
│
├── 教材复现/              ← 第一大类：教材案例 → Python 迁移
│   └── 第1章_数据分析思维/
│       ├── 实验一_关系模型.py       Power BI 关系模型 → pandas merge
│       ├── 实验二_维度模型.py       Power BI 星型模型 → 事实表关联维度表
│       ├── 实验三_sale数据分析.py   Excel 透视表 → pivot_table
│       ├── data/                   教材配套数据
│       └── output/                 运行生成的图表
│
└── 期末大作业/            ← 第二大类：期末数据分析实战项目
    └── README.md         项目说明（建设中）
```

## 关于「教材复现」

将教材中原本用 Power BI / Excel 实现的案例，迁移为 Python（pandas + matplotlib）实现，
每个实验脚本都保留了对教材原分析逻辑的对照说明，帮助理解数据模型的内涵。

- 关系模型（E-R 模型）→ 用 `merge` 实现多表"主键-外键"关联
- 维度模型（星型模型）→ 事实表关联多张维度表，按维度聚合分析
- 数据透视 → 用 `pivot_table` 复现 Excel 透视表

详细说明见 [`教材复现/第1章_数据分析思维/`](教材复现/第1章_数据分析思维/)。

## 关于「期末大作业」

（待补充，项目完成后更新此节及对应目录）

## 运行环境

- Python 3.12（本地 conda 环境 `data_visualization`）
- 安装依赖：`pip install -r requirements.txt`

## 运行方式

```bash
cd "教材复现/第1章_数据分析思维"
python 实验一_关系模型.py
python 实验二_维度模型.py
python 实验三_sale数据分析.py
```

图表输出至对应目录的 `output/` 下。

## 说明

- 教材数据 CSV 为 GBK 编码，脚本中已用 `encoding="gbk"` 读取
- 教材数据版权归教材配套资源所有，仅用于学习
