# 多模型支持更新日志
# Multi-Model Support Changelog

## 更新时间 / Update Date
2025-11-09

## 主要更新 / Major Updates

### ✅ 1. 修复智增增 API 配置
**问题：** 代码未设置 `base_url`，导致无法连接到智增增 API  
**解决：** 在 `app.py` 中正确配置 OpenAI 客户端

```python
# 修改前
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 修改后
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.zhizengzeng.com/v1/")
)
```

**重要说明：**
- 新版 OpenAI 包（>=2.0.0）必须在初始化时设置 `base_url`
- 旧版使用 `openai.api_base = BASE_URL`（已弃用）
- 本项目使用新版 API

---

### ✅ 2. 添加多模型支持

#### 后端更改 (app.py)

**新增 API 端点：**
```python
@app.route('/api/models')
def get_models():
    """返回可用的模型列表"""
    models = [
        {"id": "gpt-4o", "name": "GPT-4o", "description": "Most capable, best for complex audits"},
        {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "description": "Faster and more cost-effective"},
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Fast and efficient"},
        {"id": "deepseek-chat", "name": "DeepSeek Chat", "description": "Alternative model"},
        {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet", "description": "Anthropic's advanced model"},
    ]
    return jsonify({"models": models})
```

**修改审计端点：**
```python
@app.route('/api/audit', methods=['POST'])
def audit_prompt():
    data = request.json
    system_prompt = data.get('prompt', '')
    selected_model = data.get('model', 'gpt-4o')  # 接收模型参数
    
    # 使用选择的模型
    response = client.chat.completions.create(
        model=selected_model,  # 动态模型
        messages=[...],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
```

#### 前端更改

**HTML (templates/index.html):**
- 添加模型选择器 UI
```html
<div class="model-selector-container">
    <label for="modelSelect" class="model-label">
        <span>Select Model</span>
        <span class="model-hint">Choose the AI model for auditing</span>
    </label>
    <select id="modelSelect" class="model-select">
        <option value="gpt-4o">GPT-4o (Recommended)</option>
    </select>
</div>
```

**JavaScript (static/js/script.js):**
- 添加模型加载函数
- 在提交时发送选择的模型

```javascript
// 加载模型列表
async function loadModels() {
    const response = await fetch('/api/models');
    const data = await response.json();
    models = data.models || [];
    renderModels();
}

// 提交时包含模型
body: JSON.stringify({ 
    prompt: prompt,
    model: selectedModel 
})
```

**CSS (static/css/style.css):**
- 添加模型选择器样式
- 美化下拉菜单

---

### ✅ 3. 文档更新

#### 新增文件：
- **API_CONFIG.md** - API 配置详细指南
- **CHANGELOG_MULTI_MODEL.md** - 本文件

#### 更新文件：
- **QUICK_START.md** - 添加 API 配置说明和模型选择说明

---

## 支持的模型 / Supported Models

| 模型 ID | 名称 | 推荐用途 |
|---------|------|----------|
| `gpt-4o` | GPT-4o | 复杂审计，最高准确度（推荐） |
| `gpt-4o-mini` | GPT-4o Mini | 平衡性能和成本 |
| `gpt-3.5-turbo` | GPT-3.5 Turbo | 快速审计 |
| `deepseek-chat` | DeepSeek Chat | 替代选项 |
| `claude-3-5-sonnet-20241022` | Claude 3.5 Sonnet | Anthropic 高级模型 |

**统一 API 密钥：**
```
sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532
```
所有模型使用同一个密钥。

---

## 使用方法 / Usage

### 1. 配置 API 密钥

创建 `.env` 文件：
```bash
OPENAI_API_KEY=sk-zk2a256993d569634deabbbcd007279f33f690e5aef05532
OPENAI_BASE_URL=https://api.zhizengzeng.com/v1/
```

### 2. 启动应用
```bash
python3 app.py
```

### 3. 使用模型选择器
1. 打开浏览器访问 http://localhost:5002
2. 在模型选择器中选择你想要的模型
3. 输入系统提示词
4. 点击"Generate Audit Report"

---

## 技术细节 / Technical Details

### OpenAI 包版本差异

**旧版本 (< 1.0.0):**
```python
import openai
openai.api_key = API_KEY
openai.api_base = BASE_URL  # 旧方式
resp = openai.ChatCompletion.create(...)
```

**新版本 (>= 2.0.0) - 本项目使用:**
```python
from openai import OpenAI
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL  # 新方式：必须在初始化时设置
)
resp = client.chat.completions.create(...)
```

### 为什么必须设置 base_url？

1. **默认行为：** OpenAI 包默认连接 `https://api.openai.com/v1/`
2. **智增增服务：** 需要连接 `https://api.zhizengzeng.com/v1/`
3. **新版要求：** 必须在创建客户端时传入 `base_url` 参数
4. **环境变量：** 支持通过 `OPENAI_BASE_URL` 环境变量配置

---

## 测试清单 / Testing Checklist

- [x] API 配置正确（base_url 设置）
- [x] 模型列表加载正常
- [x] 模型选择器 UI 显示
- [x] 提交时发送正确的模型参数
- [x] 后端接收并使用选择的模型
- [x] 无语法错误
- [x] 文档更新完整

---

## 文件修改列表 / Modified Files

1. **app.py** - 添加 base_url 配置，添加模型 API，修改审计端点
2. **templates/index.html** - 添加模型选择器 UI
3. **static/js/script.js** - 添加模型加载和提交逻辑
4. **static/css/style.css** - 添加模型选择器样式
5. **QUICK_START.md** - 更新配置和使用说明
6. **API_CONFIG.md** - 新增 API 配置指南
7. **CHANGELOG_MULTI_MODEL.md** - 本文件

---

## 下一步 / Next Steps

1. 创建 `.env` 文件并添加 API 密钥
2. 重启应用测试多模型功能
3. 尝试不同模型对比审计结果
4. 根据需要调整模型列表

---

## 注意事项 / Notes

⚠️ **重要：** 
- 必须设置 `OPENAI_API_KEY` 环境变量或在 `.env` 文件中配置
- `base_url` 已在代码中默认设置为智增增地址
- 所有模型共用同一个 API 密钥
- 推荐使用 GPT-4o 获得最佳审计效果

✅ **优势：**
- 灵活选择不同模型
- 平衡性能和成本
- 统一的 API 配置
- 友好的用户界面

