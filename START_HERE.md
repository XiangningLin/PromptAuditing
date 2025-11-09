# 🚀 从这里开始 / START HERE

## 欢迎使用多模型 Prompt Auditing 系统！

本项目支持 **34+ 个 AI 模型**，包括 OpenAI、Anthropic、Google、阿里、百度、智谱等。

---

## ⚡ 5 分钟快速开始

### 1️⃣ 配置 API 密钥（30 秒）

创建 `.env` 文件（推荐使用新命名）：
```bash
echo 'ZZZ_API_KEY=sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532' > .env
echo 'ZZZ_BASE_URL=https://api.zhizengzeng.com/v1/' >> .env
```

> 💡 **注意**：也支持旧命名 `OPENAI_API_KEY`（向后兼容），但推荐使用 `ZZZ_API_KEY` 因为支持 34+ 个不同提供商，不只是 OpenAI。

### 2️⃣ 测试连接（30 秒）

```bash
python3 test_api.py
```

看到 ✅ 就成功了！

### 3️⃣ 查看支持的模型（30 秒）

```bash
python3 models_list.py
```

你会看到 34+ 个可用模型的列表。

### 4️⃣ 启动 Web 应用（1 分钟）

```bash
python3 app.py
```

打开浏览器访问：http://localhost:5002

### 5️⃣ 运行 Benchmark（3 分钟）

```bash
python3 benchmark.py --models benchmark
```

对比 12 个主流模型的性能！

---

## 📚 详细文档

| 想了解... | 查看文档 |
|----------|---------|
| 🎯 **快速开始** | [QUICK_START.md](QUICK_START.md) |
| 🤖 **所有模型列表** | [MODELS_SUMMARY.md](MODELS_SUMMARY.md) |
| 🏆 **Benchmark 指南** | [BENCHMARK_GUIDE.md](BENCHMARK_GUIDE.md) |
| ⚙️ **API 配置** | [API_CONFIG.md](API_CONFIG.md) |
| 📝 **更新总结** | [UPDATE_SUMMARY.md](UPDATE_SUMMARY.md) |

---

## 🎯 三种使用方式

### 方式 1：Web 界面（推荐新手）

```bash
python3 app.py
```

- ✅ 直观的 UI
- ✅ 实时切换模型
- ✅ 无需编程

### 方式 2：Benchmark 测试（推荐对比）

```bash
python3 benchmark.py --models benchmark
```

- ✅ 自动化测试
- ✅ 性能对比
- ✅ 详细报告

### 方式 3：命令行脚本（推荐开发者）

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532",
    base_url="https://api.zhizengzeng.com/v1/"
)

response = client.chat.completions.create(
    model="gpt-4o",  # 或任何其他模型
    messages=[{"role": "user", "content": "Hello!"}]
)
```

---

## 🌟 支持的模型（34+）

### 推荐模型

| 模型 | 提供商 | 特点 |
|------|--------|------|
| `gpt-4o` | OpenAI | 🏆 最强大 |
| `claude-3-5-sonnet-20241022` | Anthropic | 🧠 优秀推理 |
| `gemini-1.5-pro` | Google | 🔍 Google 最强 |
| `qwen-max` | Alibaba | 🇨🇳 中文最强 |
| `deepseek-chat` | DeepSeek | 💰 高性价比 |

查看 [MODELS_SUMMARY.md](MODELS_SUMMARY.md) 获取完整列表。

---

## ❓ 常见问题

### Q: 需要多个 API 密钥吗？
**A:** 不需要！所有 34+ 个模型使用同一个智增增 API 密钥（`ZZZ_API_KEY`）。

### Q: 为什么改名为 ZZZ_API_KEY？
**A:** 因为支持 34+ 个不同提供商（OpenAI、Anthropic、Google、阿里、百度等），用 `OPENAI_API_KEY` 容易误导。`ZZZ_API_KEY`（Zhizengzeng）更准确。旧命名仍然兼容。

### Q: 哪个模型最好？
**A:** 取决于任务：
- 复杂任务 → `gpt-4o`
- 中文任务 → `qwen-max`
- 快速响应 → `gpt-3.5-turbo`
- 性价比 → `deepseek-chat`

### Q: 如何对比不同模型？
**A:** 运行 benchmark：
```bash
python3 benchmark.py --models benchmark
```

### Q: 遇到错误怎么办？
**A:** 
1. 运行 `python3 test_api.py` 测试连接
2. 查看 [UPDATE_SUMMARY.md](UPDATE_SUMMARY.md) 的故障排除部分
3. 检查 API 密钥是否正确

---

## 🎊 就这么简单！

1. ✅ 配置 API 密钥
2. ✅ 测试连接
3. ✅ 选择使用方式
4. ✅ 开始使用

**统一 API 密钥**：`sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532`

> 💡 **重要提示**：推荐使用新的环境变量命名 `ZZZ_API_KEY` 而不是 `OPENAI_API_KEY`，因为我们支持 34+ 个不同提供商，不只是 OpenAI。查看 [NAMING_CHANGE.md](NAMING_CHANGE.md) 了解详情。

**立即开始** → `python3 app.py` 🚀

