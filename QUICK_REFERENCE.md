# 🚀 快速参考卡片
# Quick Reference Card

## 📊 数据集概览

```
总提示词数：270+
├── 种子数据：140 个 (70 好 + 70 坏)
└── 生成数据：130 个 (组合和变体)

分类：
├── Deception & Misinformation (欺骗与误导)
├── Manipulation (操纵)
└── Privacy Violation (隐私侵犯)
```

---

## ⚡ 常用命令

### 查看数据

```bash
# 查看种子数据
head -20 seed_prompts.csv

# 查看生成数据
head -20 generated_prompts.csv

# 统计数量
wc -l *.csv
```

### 生成新数据

```bash
# 生成 130 个新提示词
python3 generate_prompts.py

# 输出：generated_prompts.csv
```

### 分析数据

```bash
# 完整分析
python3 analyze_dataset.py

# 输出：dataset_summary.json
```

### 运行测试

```bash
# Benchmark 所有模型
python3 benchmark.py --models benchmark

# 只测试 OpenAI 模型
python3 benchmark.py --models openai

# 增加延迟避免限流
python3 benchmark.py --models benchmark --delay 2
```

### 运行网站

```bash
# 启动 Flask 应用
python3 app.py

# 访问：http://localhost:5002
```

---

## 📁 文件速查

| 文件 | 用途 | 何时使用 |
|------|------|---------|
| `seed_prompts.csv` | 基础种子数据 | 训练、测试基础 |
| `generated_prompts.csv` | 生成的组合 | 测试鲁棒性 |
| `generate_prompts.py` | 生成器脚本 | 需要更多数据 |
| `analyze_dataset.py` | 分析工具 | 查看统计信息 |
| `benchmark.py` | 性能测试 | 对比模型表现 |
| `app.py` | Web 应用 | 在线审计 |

---

## 🎯 典型工作流

### 1. 开发和测试

```bash
# 步骤 1：查看现有数据
python3 analyze_dataset.py

# 步骤 2：生成测试案例
python3 generate_prompts.py

# 步骤 3：运行测试
python3 benchmark.py --models benchmark

# 步骤 4：分析结果
# 查看 benchmark_report_*.txt
```

### 2. 添加新的种子数据

```bash
# 步骤 1：编辑 seed_prompts.csv
nano seed_prompts.csv

# 步骤 2：验证格式
python3 -c "import pandas as pd; print(pd.read_csv('seed_prompts.csv').tail())"

# 步骤 3：重新生成
python3 generate_prompts.py

# 步骤 4：测试
python3 benchmark.py --models benchmark
```

### 3. 部署到生产

```bash
# 步骤 1：设置环境变量
export ZZZ_API_KEY="your-api-key"
export ZZZ_BASE_URL="https://api.zhizengzeng.com/v1/"

# 步骤 2：启动应用
python3 app.py

# 步骤 3：测试
curl http://localhost:5002/api/models
```

---

## 🔍 数据格式

### seed_prompts.csv

```csv
category,subcategory,standard_id,label,prompt
Deception & Misinformation,Capability Deception,1.1,bad,"提示词内容..."
Deception & Misinformation,Capability Deception,1.1,good,"提示词内容..."
```

### generated_prompts.csv

```csv
id,type,expected_label,categories,details,prompt
GEN_0001,combined_bad,FAIL,Privacy Violation,"{...}","提示词内容..."
```

---

## 💡 使用技巧

### Python 快速加载

```python
import pandas as pd

# 加载数据
seed = pd.read_csv('seed_prompts.csv')
generated = pd.read_csv('generated_prompts.csv')

# 筛选坏例子
bad_examples = seed[seed['label'] == 'bad']

# 按分类筛选
deception = seed[seed['category'] == 'Deception & Misinformation']

# 随机抽样
sample = seed.sample(10)
```

### 批量测试

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("ZZZ_API_KEY"),
    base_url=os.environ.get("ZZZ_BASE_URL")
)

def test_prompt(prompt, model='gpt-4o'):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 测试所有坏例子
for _, row in bad_examples.iterrows():
    result = test_prompt(row['prompt'])
    print(f"{row['subcategory']}: {result[:50]}...")
```

### 统计分析

```python
# 按分类统计
print(seed.groupby('category')['label'].value_counts())

# 计算平均长度
seed['length'] = seed['prompt'].str.len()
print(seed.groupby('label')['length'].mean())

# 找出最长的提示词
longest = seed.nlargest(5, 'length')
print(longest[['subcategory', 'length']])
```

---

## 🎨 可视化（可选）

### 使用 pandas

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('seed_prompts.csv')

# 分类分布
df['category'].value_counts().plot(kind='bar')
plt.title('Prompts by Category')
plt.show()

# 长度分布
df['prompt'].str.len().hist(bins=20)
plt.title('Prompt Length Distribution')
plt.show()
```

---

## 🔧 故障排除

### 问题：生成器运行失败

```bash
# 检查文件是否存在
ls -lh seed_prompts.csv

# 验证 CSV 格式
python3 -c "import pandas as pd; pd.read_csv('seed_prompts.csv')"
```

### 问题：Benchmark 某些模型失败

```bash
# 测试单个模型
python3 -c "
from openai import OpenAI
import os
client = OpenAI(
    api_key=os.environ.get('ZZZ_API_KEY'),
    base_url=os.environ.get('ZZZ_BASE_URL')
)
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': 'Hello'}]
)
print(response.choices[0].message.content)
"
```

### 问题：环境变量未设置

```bash
# 检查环境变量
echo $ZZZ_API_KEY
echo $ZZZ_BASE_URL

# 临时设置
export ZZZ_API_KEY="your-key"
export ZZZ_BASE_URL="https://api.zhizengzeng.com/v1/"

# 永久设置（添加到 .env 文件）
echo 'ZZZ_API_KEY=your-key' >> .env
echo 'ZZZ_BASE_URL=https://api.zhizengzeng.com/v1/' >> .env
```

---

## 📈 性能优化

### 加速生成

```python
# 并行生成（修改 generate_prompts.py）
from concurrent.futures import ThreadPoolExecutor

def generate_parallel():
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(combine_bad_prompts, ...),
            executor.submit(add_good_context_to_bad, ...),
            executor.submit(create_subtle_violations, ...),
            executor.submit(generate_category_specific_combinations, ...)
        ]
        results = [f.result() for f in futures]
    return results
```

### 缓存结果

```python
# 缓存 API 调用结果
import json
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_audit(prompt, model):
    # 审计逻辑
    return result
```

---

## 🎯 最佳实践

### 1. 数据管理

- ✅ 定期备份 CSV 文件
- ✅ 使用版本控制（Git）
- ✅ 记录数据集变更
- ✅ 保持数据平衡

### 2. 测试策略

- ✅ 从简单案例开始
- ✅ 逐步增加复杂度
- ✅ 记录失败案例
- ✅ 定期重新测试

### 3. 持续改进

- ✅ 分析模型错误
- ✅ 添加新的种子数据
- ✅ 更新生成策略
- ✅ 优化审计标准

---

## 📞 获取帮助

### 文档

- `SEED_PROMPTS_README.md` - 完整指南
- `DATASET_SUMMARY.md` - 数据集总结
- `TROUBLESHOOTING.md` - 故障排除
- `BENCHMARK_GUIDE.md` - Benchmark 指南

### 快速诊断

```bash
# 运行完整诊断
python3 -c "
import os
import pandas as pd

print('环境检查：')
print(f'  API Key: {'✓' if os.environ.get('ZZZ_API_KEY') else '✗'}')
print(f'  Base URL: {'✓' if os.environ.get('ZZZ_BASE_URL') else '✗'}')

print('\n文件检查：')
files = ['seed_prompts.csv', 'generated_prompts.csv', 'standards.json']
for f in files:
    try:
        if f.endswith('.csv'):
            df = pd.read_csv(f)
            print(f'  {f}: ✓ ({len(df)} 行)')
        else:
            import json
            with open(f) as file:
                json.load(file)
            print(f'  {f}: ✓')
    except:
        print(f'  {f}: ✗')
"
```

---

## 🎉 快速成功案例

### 5 分钟快速开始

```bash
# 1. 查看数据（30 秒）
head -5 seed_prompts.csv

# 2. 生成新数据（1 分钟）
python3 generate_prompts.py

# 3. 分析统计（30 秒）
python3 analyze_dataset.py

# 4. 测试单个模型（2 分钟）
python3 benchmark.py --models openai

# 5. 启动网站（30 秒）
python3 app.py
```

### 10 分钟完整测试

```bash
# 1. 设置环境（1 分钟）
export ZZZ_API_KEY="your-key"
export ZZZ_BASE_URL="https://api.zhizengzeng.com/v1/"

# 2. 生成数据（1 分钟）
python3 generate_prompts.py

# 3. 运行 Benchmark（5 分钟）
python3 benchmark.py --models benchmark --delay 1

# 4. 查看结果（1 分钟）
cat benchmark_report_*.txt

# 5. 启动网站（1 分钟）
python3 app.py
# 访问 http://localhost:5002

# 6. 测试审计（1 分钟）
# 在网站上粘贴测试提示词
```

---

**保存此文件作为快速参考！** 📌

所有命令都经过测试，可以直接使用。




