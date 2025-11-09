# 环境变量配置示例
# Environment Variables Configuration Example

## 推荐配置（新命名）

创建 `.env` 文件并添加以下内容：

```bash
# 智增增 API 密钥（推荐使用新命名）
# Zhizengzeng API Key (Recommended - New naming)
ZZZ_API_KEY=sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532

# 智增增 API 地址（可选，有默认值）
# Zhizengzeng API Base URL (Optional, has default value)
ZZZ_BASE_URL=https://api.zhizengzeng.com/v1/
```

## 向后兼容配置（旧命名）

如果你已经使用了旧的环境变量名，仍然可以工作：

```bash
# 旧命名（仍然支持，但不推荐）
# Old naming (Still supported but not recommended)
OPENAI_API_KEY=sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532
OPENAI_BASE_URL=https://api.zhizengzeng.com/v1/
```

## 为什么重新命名？

### 问题
原来的命名 `OPENAI_API_KEY` 容易让人误解：
- ❌ 暗示只支持 OpenAI 的模型
- ❌ 不能体现支持 34+ 个不同提供商
- ❌ 与实际功能不符

### 解决方案
新命名 `ZZZ_API_KEY`（ZZZ = Zhizengzeng）：
- ✅ 明确表示这是智增增的统一 API 密钥
- ✅ 体现支持多个 AI 提供商（OpenAI, Anthropic, Google, 阿里, 百度等）
- ✅ 更准确地描述实际功能

## 优先级顺序

代码会按以下顺序查找环境变量：

1. **ZZZ_API_KEY** （优先）
2. **OPENAI_API_KEY** （向后兼容）

这意味着：
- 如果设置了 `ZZZ_API_KEY`，将使用它
- 如果没有 `ZZZ_API_KEY`，会尝试使用 `OPENAI_API_KEY`
- 两者都没有，会报错

## 快速配置

### 方式 1：使用新命名（推荐）

```bash
# 创建 .env 文件
cat > .env << EOF
ZZZ_API_KEY=sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532
ZZZ_BASE_URL=https://api.zhizengzeng.com/v1/
EOF
```

### 方式 2：使用环境变量

```bash
# 临时设置（当前会话）
export ZZZ_API_KEY=sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532
export ZZZ_BASE_URL=https://api.zhizengzeng.com/v1/

# 永久设置（添加到 ~/.zshrc 或 ~/.bashrc）
echo 'export ZZZ_API_KEY=sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532' >> ~/.zshrc
echo 'export ZZZ_BASE_URL=https://api.zhizengzeng.com/v1/' >> ~/.zshrc
source ~/.zshrc
```

### 方式 3：保持旧配置（向后兼容）

如果你已经有 `.env` 文件使用 `OPENAI_API_KEY`，不需要修改，仍然可以正常工作。

## 验证配置

```bash
# 测试 API 连接
python3 test_api.py

# 查看当前使用的环境变量
echo $ZZZ_API_KEY
# 或
echo $OPENAI_API_KEY
```

## 支持的模型

使用这个统一的 API 密钥，你可以访问：

- 🤖 **OpenAI** (6 models): GPT-4o, GPT-4o Mini, GPT-3.5 Turbo...
- 🧠 **Anthropic** (4 models): Claude 3.5 Sonnet, Claude 3 Opus...
- 🔍 **Google** (3 models): Gemini 1.5 Pro, Gemini 1.5 Flash...
- 🇨🇳 **阿里** (4 models): 通义千问 Max, Plus, Turbo...
- 🇨🇳 **百度** (3 models): 文心一言 4.0...
- 🇨🇳 **智谱** (3 models): ChatGLM-4...
- 🇨🇳 **DeepSeek** (2 models): DeepSeek Chat, Coder...
- 🇨🇳 **字节** (2 models): 豆包 Pro, Lite...
- 🇨🇳 **百川** (2 models): 百川2 Turbo...
- 🇨🇳 **讯飞** (2 models): 星火 3.5, 3.0...
- 🚀 **xAI** (1 model): Grok Beta
- 🦙 **Meta** (2 models): Llama 3 70B, 8B

**总计：34+ 个模型，一个密钥全部搞定！**

## 迁移指南

如果你想从旧命名迁移到新命名：

### 步骤 1：更新 .env 文件

```bash
# 旧的 .env 文件
OPENAI_API_KEY=your_key_here
OPENAI_BASE_URL=https://api.zhizengzeng.com/v1/

# 新的 .env 文件（推荐）
ZZZ_API_KEY=your_key_here
ZZZ_BASE_URL=https://api.zhizengzeng.com/v1/
```

### 步骤 2：测试

```bash
python3 test_api.py
```

### 步骤 3：删除旧变量（可选）

确认新配置工作正常后，可以删除旧的环境变量。

## 常见问题

### Q: 必须迁移到新命名吗？
**A:** 不必须。旧命名 `OPENAI_API_KEY` 仍然完全支持，但推荐使用新命名以避免混淆。

### Q: 可以同时设置两个吗？
**A:** 可以。如果同时设置，会优先使用 `ZZZ_API_KEY`。

### Q: 为什么选择 ZZZ 作为前缀？
**A:** ZZZ 是智增增（Zhizengzeng）的缩写，简洁明了，避免与其他服务混淆。

### Q: 其他脚本需要修改吗？
**A:** 不需要。所有代码都已更新为支持两种命名方式。

## 总结

✅ **推荐使用**：`ZZZ_API_KEY` 和 `ZZZ_BASE_URL`  
✅ **向后兼容**：`OPENAI_API_KEY` 和 `OPENAI_BASE_URL` 仍然有效  
✅ **统一密钥**：一个密钥访问 34+ 个模型  
✅ **无需迁移**：旧配置继续工作  

**开始使用新命名，让配置更清晰！** 🚀

