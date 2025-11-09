# 🏆 Benchmark 使用指南
# Benchmark Usage Guide

## 概述 / Overview

本项目提供了完整的多模型 benchmark 系统，用于测试和比较不同 AI 模型在 Prompt Auditing 任务上的表现。

## 支持的模型总数 / Total Supported Models

智增增平台支持 **40+ 个模型**，涵盖以下提供商：

### 国际模型 / International Models

#### OpenAI (6 models)
- `gpt-4o` - 最强大的 GPT-4 版本
- `gpt-4o-mini` - 更快速经济的版本
- `gpt-4-turbo` - 上一代旗舰
- `gpt-4` - 经典 GPT-4
- `gpt-3.5-turbo` - 快速高效
- `gpt-3.5-turbo-16k` - 长上下文版本

#### Anthropic (4 models)
- `claude-3-5-sonnet-20241022` - 最新 Sonnet
- `claude-3-opus-20240229` - 最强大的 Claude
- `claude-3-sonnet-20240229` - 平衡版本
- `claude-3-haiku-20240307` - 最快的 Claude

#### Google (3 models)
- `gemini-1.5-pro` - 最强大的 Gemini
- `gemini-1.5-flash` - 快速版本
- `gemini-pro` - 经典版本

#### Meta (2 models)
- `llama-3-70b` - 大参数开源模型
- `llama-3-8b` - 小参数开源模型

#### xAI (1 model)
- `grok-beta` - Elon Musk 的 AI

### 中国模型 / Chinese Models

#### 阿里 Alibaba (4 models)
- `qwen-max` - 通义千问最强版本
- `qwen-plus` - 平衡性能
- `qwen-turbo` - 快速响应
- `qwen-max-longcontext` - 长上下文版本

#### 百度 Baidu (3 models)
- `ernie-bot-4` - 文心一言 4.0
- `ernie-bot` - 文心一言标准版
- `ernie-bot-turbo` - 文心一言快速版

#### 智谱 Zhipu (3 models)
- `glm-4` - ChatGLM-4
- `glm-4-plus` - ChatGLM-4 Plus
- `glm-3-turbo` - ChatGLM-3 Turbo

#### DeepSeek (2 models)
- `deepseek-chat` - 通用对话模型
- `deepseek-coder` - 代码专用模型

#### 字节跳动 ByteDance (2 models)
- `doubao-pro-32k` - 豆包 Pro
- `doubao-lite-32k` - 豆包 Lite

#### 百川 Baichuan (2 models)
- `baichuan2-turbo` - 百川2 Turbo
- `baichuan2-turbo-192k` - 百川2 长上下文

#### 讯飞 iFlytek (2 models)
- `spark-3.5` - 讯飞星火 3.5
- `spark-3.0` - 讯飞星火 3.0

---

## 快速开始 / Quick Start

### 1. 查看所有支持的模型

```bash
python3 models_list.py
```

输出示例：
```
================================================================================
智增增支持的所有模型 / All Zhizengzeng Supported Models
================================================================================

【OPENAI】 (6 models)
--------------------------------------------------------------------------------
  • gpt-4o                                  | GPT-4o
  • gpt-4o-mini                             | GPT-4o Mini
  ...

【ANTHROPIC】 (4 models)
--------------------------------------------------------------------------------
  • claude-3-5-sonnet-20241022              | Claude 3.5 Sonnet
  ...

总计 / Total: 40+ 个模型
```

### 2. 运行 Benchmark 测试

#### 选项 A：测试推荐的代表性模型（推荐）

```bash
python3 benchmark.py --models benchmark
```

这将测试 12 个精选的代表性模型，覆盖各个主要提供商。

#### 选项 B：测试所有模型（耗时较长）

```bash
python3 benchmark.py --models all --delay 2
```

⚠️ 警告：这将测试 40+ 个模型，每个模型测试 3 个提示词，总共 120+ 次 API 调用，可能需要 10-20 分钟。

#### 选项 C：只测试特定类型的模型

```bash
# 只测试 OpenAI 模型
python3 benchmark.py --models openai

# 只测试中国模型
python3 benchmark.py --models chinese
```

### 3. 查看结果

Benchmark 完成后会：
1. 在终端显示详细报告
2. 保存结果到 JSON 文件：`benchmark_results_YYYYMMDD_HHMMSS.json`

---

## Benchmark 测试内容 / What Gets Tested

每个模型会用 3 个不同的测试提示词进行测试：

1. **Good Prompt** - 符合道德标准的提示词（应该 PASS）
2. **Bad Prompt** - 明显违反道德标准的提示词（应该 FAIL）
3. **Mixed Prompt** - 混合质量的提示词（可能 PASS 或 FAIL）

### 评估指标 / Evaluation Metrics

- **Success Rate** - API 调用成功率
- **Accuracy** - 评估准确率（能否正确识别好/坏提示词）
- **Average Latency** - 平均响应时间
- **Token Usage** - Token 使用量

---

## 结果示例 / Sample Results

```
模型性能对比 / Model Performance Comparison:
--------------------------------------------------------------------------------
Model                          Success    Accuracy     Avg Latency     Tokens    
--------------------------------------------------------------------------------
GPT-4o                         3/3        3/3          2.34s           1250      
Claude 3.5 Sonnet              3/3        3/3          2.89s           1180      
通义千问 Max                    3/3        2/3          1.56s           980       
GPT-3.5 Turbo                  3/3        2/3          0.98s           850       
...
```

---

## 高级用法 / Advanced Usage

### 自定义测试提示词

编辑 `benchmark.py` 中的 `TEST_PROMPTS` 字典：

```python
TEST_PROMPTS = {
    "custom1": "Your custom prompt here...",
    "custom2": "Another custom prompt...",
}
```

### 调整 API 调用延迟

避免触发速率限制：

```bash
python3 benchmark.py --delay 2.0  # 每次调用间隔 2 秒
```

### 分析结果

结果保存在 JSON 文件中，可以用 Python 进一步分析：

```python
import json

with open('benchmark_results_20251109_123456.json', 'r') as f:
    data = json.load(f)

# 分析数据
for result in data['results']:
    print(f"{result['model_name']}: {result['latency']}s")
```

---

## 推荐的 Benchmark 配置 / Recommended Benchmark Setup

### 快速测试（5 分钟）
```bash
python3 benchmark.py --models benchmark --delay 1
```
测试 12 个代表性模型

### 完整测试（20 分钟）
```bash
python3 benchmark.py --models all --delay 2
```
测试所有 40+ 个模型

### 对比测试
```bash
# 测试国际模型
python3 benchmark.py --models openai --delay 1

# 测试中国模型
python3 benchmark.py --models chinese --delay 1
```

---

## 注意事项 / Important Notes

### API 配置

确保 `.env` 文件配置正确：
```bash
OPENAI_API_KEY=sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532
OPENAI_BASE_URL=https://api.zhizengzeng.com/v1/
```

### 成本估算

- 每个模型测试：3 次 API 调用
- 每次调用约：500-2000 tokens
- 推荐 benchmark (12 模型)：约 36 次调用
- 完整 benchmark (40+ 模型)：约 120+ 次调用

### 速率限制

如果遇到速率限制错误，增加 `--delay` 参数：
```bash
python3 benchmark.py --models all --delay 3
```

---

## 在 Web 应用中使用多模型 / Using Multiple Models in Web App

启动应用后，模型选择器会显示所有可用模型，按提供商分组：

1. ⭐ **Recommended** - 推荐的顶级模型
2. 🤖 **OpenAI** - OpenAI 全系列
3. 🧠 **Anthropic** - Claude 系列
4. 🇨🇳 **Chinese Models** - 中国主流模型
5. 🔍 **Google** - Gemini 系列
6. 🔧 **Other** - 其他模型

---

## 故障排除 / Troubleshooting

### 模型不可用

某些模型可能需要特殊权限或在某些地区不可用。如果遇到错误：
- 检查智增增文档确认模型 ID
- 尝试其他类似模型
- 联系智增增客服

### API 错误

常见错误及解决方案：
- `401 Unauthorized` - 检查 API 密钥
- `429 Too Many Requests` - 增加延迟时间
- `500 Server Error` - 模型可能暂时不可用，稍后重试

---

## 总结 / Summary

✅ **支持 40+ 个模型**  
✅ **涵盖所有主流 AI 提供商**  
✅ **完整的 benchmark 系统**  
✅ **详细的性能对比报告**  
✅ **灵活的测试配置**  
✅ **统一的 API 密钥**  

开始你的 benchmark 测试吧！🚀

