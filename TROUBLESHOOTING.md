# 🔧 故障排除指南
# Troubleshooting Guide

## 常见错误及解决方案

---

## ❌ Error: 'NoneType' object is not subscriptable

### 问题描述
在运行 Benchmark 或使用某些模型时出现此错误：
```
Testing 文心一言 4.0 (ernie-bot-4)... ✗ Error: 'NoneType' object is not subscriptable
```

### 原因分析

这个错误通常由以下几个原因导致：

#### 1. **模型不可用或不支持**
某些模型可能：
- 在智增增平台上不可用
- 需要特殊权限或额外配置
- 模型 ID 不正确
- 在某些地区不可用

#### 2. **API 响应为空**
模型返回了空响应或格式不符合预期：
```python
response.choices[0].message.content  # 返回 None
```

#### 3. **response_format 不支持**
某些模型不支持 `response_format={"type": "json_object"}` 参数。

#### 4. **API 配置问题**
- API 密钥权限不足
- Base URL 配置错误
- 网络连接问题

---

### 解决方案

#### 方案 1：跳过不支持的模型

编辑 `app.py` 或 `benchmark.py`，移除或注释掉不支持的模型：

```python
# 在 app.py 的 /api/models 端点中
"chinese": [
    {"id": "qwen-max", "name": "通义千问 Max", ...},
    {"id": "qwen-plus", "name": "通义千问 Plus", ...},
    {"id": "qwen-turbo", "name": "通义千问 Turbo", ...},
    # {"id": "ernie-bot-4", "name": "文心一言 4.0", ...},  # 暂时注释掉
    {"id": "glm-4", "name": "ChatGLM-4", ...},
    {"id": "deepseek-chat", "name": "DeepSeek Chat", ...},
],
```

#### 方案 2：使用已知可用的模型

只测试确认可用的模型：

```bash
# 只测试 OpenAI 模型
python3 benchmark.py --models openai

# 或者手动指定模型列表
```

#### 方案 3：检查 API 密钥权限

确认你的 API 密钥是否有权限访问该模型：

```bash
# 测试 API 连接
python3 test_api.py
```

#### 方案 4：修改模型 ID

某些模型的 ID 可能不同，尝试其他变体：

**文心一言可能的 ID：**
- `ernie-bot-4`
- `ernie-4.0`
- `ernie-bot-4.0`
- `ERNIE-Bot-4`

**通义千问可能的 ID：**
- `qwen-max`
- `qwen-max-0428`
- `qwen-max-1201`

#### 方案 5：移除 response_format 参数

某些模型不支持 JSON 模式，可以移除这个参数：

```python
# 修改 benchmark.py 或 app.py
response = self.client.chat.completions.create(
    model=model_id,
    messages=[...],
    temperature=0.3,
    # response_format={"type": "json_object"}  # 注释掉这行
)
```

然后手动解析 JSON：
```python
try:
    result = json.loads(content)
except:
    # 尝试从文本中提取 JSON
    import re
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    if json_match:
        result = json.loads(json_match.group())
```

---

### 已修复的改进

我已经在代码中添加了更好的错误处理：

#### 在 `app.py` 中：

```python
# 验证响应
if not response or not response.choices or len(response.choices) == 0:
    return jsonify({'error': 'No response from AI model'}), 500

if not response.choices[0].message or not response.choices[0].message.content:
    return jsonify({'error': 'Empty response from AI model'}), 500

# 解析响应
try:
    result = json.loads(response.choices[0].message.content)
except json.JSONDecodeError as e:
    return jsonify({'error': f'Invalid JSON response: {str(e)}'}), 500
```

#### 在 `benchmark.py` 中：

```python
# 验证响应
if not response or not response.choices or len(response.choices) == 0:
    raise ValueError(f"No response from model {model_id}")

if not response.choices[0].message or not response.choices[0].message.content:
    raise ValueError(f"Empty response content from model {model_id}")

# 解析结果
content = response.choices[0].message.content
if not content:
    raise ValueError(f"Response content is None from model {model_id}")

result = json.loads(content)
```

---

## 🎯 推荐的模型列表

### ✅ 确认可用的模型

这些模型在大多数情况下都能正常工作：

**OpenAI：**
- `gpt-4o` ⭐
- `gpt-4o-mini` ⭐
- `gpt-3.5-turbo` ⭐
- `gpt-4-turbo`

**Anthropic：**
- `claude-3-5-sonnet-20241022` ⭐
- `claude-3-opus-20240229`
- `claude-3-haiku-20240307`

**Google：**
- `gemini-1.5-pro` ⭐
- `gemini-1.5-flash`

**DeepSeek：**
- `deepseek-chat` ⭐
- `deepseek-coder`

**阿里：**
- `qwen-max` ⭐
- `qwen-plus`
- `qwen-turbo`

### ⚠️ 可能不可用的模型

这些模型可能需要特殊配置或在某些情况下不可用：

- `ernie-bot-4` (文心一言 4.0)
- `ernie-bot-turbo`
- `glm-4` (ChatGLM-4)
- `doubao-pro-32k` (豆包)
- `baichuan2-turbo`
- `spark-3.5` (讯飞星火)
- `grok-beta`
- `llama-3-70b`

---

## 🔍 调试步骤

### 1. 测试单个模型

```bash
# 创建测试脚本 test_single_model.py
cat > test_single_model.py << 'EOF'
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("ZZZ_API_KEY"),
    base_url=os.environ.get("ZZZ_BASE_URL", "https://api.zhizengzeng.com/v1/")
)

model_id = "ernie-bot-4"  # 修改为你要测试的模型

try:
    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": "Hello"}],
        temperature=0.3
    )
    print(f"✅ {model_id} is available!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ {model_id} error: {str(e)}")
EOF

python3 test_single_model.py
```

### 2. 查看详细错误

在 `benchmark.py` 或 `app.py` 中添加调试输出：

```python
try:
    response = client.chat.completions.create(...)
    print(f"DEBUG: Response type: {type(response)}")
    print(f"DEBUG: Has choices: {hasattr(response, 'choices')}")
    if hasattr(response, 'choices'):
        print(f"DEBUG: Choices length: {len(response.choices)}")
        if len(response.choices) > 0:
            print(f"DEBUG: Message: {response.choices[0].message}")
except Exception as e:
    print(f"DEBUG: Exception: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
```

### 3. 检查 API 配置

```bash
# 验证环境变量
echo "ZZZ_API_KEY: $ZZZ_API_KEY"
echo "ZZZ_BASE_URL: $ZZZ_BASE_URL"

# 测试 API 连接
python3 test_api.py
```

---

## 📊 运行 Benchmark 的最佳实践

### 1. 从小范围开始

```bash
# 先测试 OpenAI 模型（最稳定）
python3 benchmark.py --models openai

# 如果成功，再测试推荐模型
python3 benchmark.py --models benchmark
```

### 2. 增加延迟避免限流

```bash
# 增加延迟到 2 秒
python3 benchmark.py --models benchmark --delay 2
```

### 3. 查看详细日志

```bash
# 运行时重定向输出
python3 benchmark.py --models benchmark 2>&1 | tee benchmark.log
```

### 4. 手动创建可用模型列表

编辑 `models_list.py`，只包含确认可用的模型：

```python
def get_benchmark_models():
    """获取确认可用的模型"""
    return [
        {"id": "gpt-4o", "name": "GPT-4o", "provider": "OpenAI"},
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "OpenAI"},
        {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet", "provider": "Anthropic"},
        {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "provider": "Google"},
        {"id": "qwen-max", "name": "通义千问 Max", "provider": "Alibaba"},
        {"id": "deepseek-chat", "name": "DeepSeek Chat", "provider": "DeepSeek"},
    ]
```

---

## 💡 联系支持

如果问题持续存在：

1. **查看智增增文档**
   - 访问：https://doc.zhizengzeng.com/
   - 查看支持的模型列表
   - 确认模型 ID 格式

2. **联系智增增客服**
   - 确认你的 API 密钥权限
   - 询问特定模型的可用性
   - 获取正确的模型 ID

3. **使用替代模型**
   - 如果某个模型不可用，使用同类型的其他模型
   - 例如：文心一言不可用 → 使用通义千问或 ChatGLM

---

## ✅ 总结

### 快速修复步骤：

1. ✅ 更新代码（已完成）- 添加了更好的错误处理
2. ✅ 跳过不可用的模型
3. ✅ 使用确认可用的模型列表
4. ✅ 增加 API 调用延迟
5. ✅ 查看详细错误日志

### 推荐的测试命令：

```bash
# 最稳定的测试
python3 benchmark.py --models openai --delay 1

# 如果成功，尝试更多模型
python3 benchmark.py --models benchmark --delay 2
```

**现在重新运行 Benchmark 应该会有更好的错误提示！** 🚀

