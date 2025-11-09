# API Configuration Guide
# API 配置指南

## 智增增 API 配置

本项目已配置为使用智增增（Zhizengzeng）的 API 服务。

### 配置步骤

1. **创建 `.env` 文件**
   
   在项目根目录创建 `.env` 文件：
   ```bash
   touch .env
   ```

2. **添加 API 密钥**
   
   在 `.env` 文件中添加以下内容：
   ```bash
   # 你的智增增 API 密钥
   OPENAI_API_KEY=sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532
   
   # 智增增 API 地址（可选，默认已设置）
   OPENAI_BASE_URL=https://api.zhizengzeng.com/v1/
   ```

3. **保存并重启应用**
   ```bash
   python3 app.py
   ```

### 支持的模型

应用支持以下模型（通过下拉菜单选择）：

| 模型 ID | 名称 | 说明 |
|---------|------|------|
| `gpt-4o` | GPT-4o | 最强大，适合复杂审计（推荐） |
| `gpt-4o-mini` | GPT-4o Mini | 更快速且经济实惠 |
| `gpt-3.5-turbo` | GPT-3.5 Turbo | 快速高效 |
| `deepseek-chat` | DeepSeek Chat | 替代模型 |
| `claude-3-5-sonnet-20241022` | Claude 3.5 Sonnet | Anthropic 高级模型 |

### 技术说明

#### OpenAI 包版本差异

**旧版本（< 1.0.0）：**
```python
import openai
openai.api_key = API_KEY
openai.api_base = BASE_URL
```

**新版本（>= 2.0.0）- 本项目使用：**
```python
from openai import OpenAI
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL  # 关键：必须在初始化时设置
)
```

#### 为什么必须设置 base_url？

- 默认情况下，OpenAI 包会连接到 `https://api.openai.com/v1/`
- 要使用智增增服务，**必须**将 `base_url` 设置为 `https://api.zhizengzeng.com/v1/`
- 在新版 OpenAI 包中，`base_url` 必须在创建 `OpenAI` 客户端时传入

### 验证配置

启动应用后，如果配置正确：
- 页面会加载模型选择器
- 提交审计请求时会使用选择的模型
- 不会出现 API 连接错误

如果出现错误：
1. 检查 `.env` 文件是否存在
2. 确认 API 密钥正确
3. 确认 `base_url` 设置正确
4. 重启应用

### 统一 API 密钥

你提供的密钥：
```
sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532
```

此密钥可用于所有支持的模型。只需在 `.env` 文件中设置一次即可。

