# Vercel 部署指南

## 🚀 快速部署步骤

### 1. 安装 Vercel CLI（如果还没有）

```bash
npm install -g vercel
```

### 2. 登录 Vercel

```bash
vercel login
```

### 3. 部署

```bash
cd /Users/linxiangning/Desktop/promptauditing/PromptAuditing
vercel
```

按照提示操作：
- Set up and deploy? **Y**
- Which scope? 选择您的账号
- Link to existing project? **N**（首次部署）
- What's your project's name? 输入项目名（如 `prompt-auditing`）
- In which directory is your code located? **./**
- Want to override the settings? **N**

### 4. 设置环境变量

部署完成后，在 Vercel Dashboard 中设置环境变量：

1. 访问 https://vercel.com/dashboard
2. 选择您的项目
3. 进入 **Settings** → **Environment Variables**
4. 添加以下变量：

```
ZZZ_API_KEY=your_api_key_here
ZZZ_BASE_URL=https://api.zhizengzeng.com/v1/
```

### 5. 重新部署

设置完环境变量后，重新部署：

```bash
vercel --prod
```

---

## ⚠️ 当前限制

### Leaderboard 功能
- ❌ **无法使用**（因为 Vercel 无法访问本地的 benchmark 结果文件）
- 如果访问 `/leaderboard`，会显示 "No benchmark results found"

### Prompt Auditing 功能
- ✅ **可以正常使用**
- 用户可以输入 prompt 进行实时审核
- 所有审核功能都正常工作

---

## 🔧 启用 Leaderboard（可选）

如果您想在 Vercel 上也显示 Leaderboard，需要：

### 方案 1：使用 GitHub 存储结果
1. 将 `benchmark_results_*.json` 提交到 Git 仓库
2. 修改 `app.py` 从 Git 仓库读取文件
3. 每次运行新的 benchmark 后，提交新文件并重新部署

### 方案 2：使用数据库
1. 设置一个数据库（如 Vercel Postgres、MongoDB Atlas）
2. 修改代码将 benchmark 结果存储到数据库
3. Leaderboard 从数据库读取数据

### 方案 3：使用对象存储
1. 使用 Vercel Blob Storage 或 AWS S3
2. 上传 benchmark 结果文件
3. 修改代码从对象存储读取

---

## 📝 部署后的 URL

部署成功后，您会得到一个 URL，类似：
```
https://prompt-auditing-xxx.vercel.app
```

### 可用页面：
- **主页（Prompt Auditing）**: https://your-app.vercel.app/
- **Leaderboard**: https://your-app.vercel.app/leaderboard（目前无数据）
- **API - Standards**: https://your-app.vercel.app/api/standards
- **API - Models**: https://your-app.vercel.app/api/models

---

## 🐛 故障排查

### 1. 部署失败
- 检查 `requirements.txt` 是否正确
- 检查 Python 版本（Vercel 默认使用 Python 3.9）

### 2. API 调用失败
- 确认已设置 `ZZZ_API_KEY` 环境变量
- 检查 Vercel Dashboard 的 Logs

### 3. 页面无法访问
- 确认 `vercel.json` 配置正确
- 检查 `api/index.py` 是否正确导入 `app`

---

## 📚 更多资源

- Vercel 文档: https://vercel.com/docs
- Python on Vercel: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- Flask on Vercel: https://vercel.com/guides/using-flask-with-vercel

---

## 🎯 下一步

1. **立即部署**：运行 `vercel` 命令
2. **测试功能**：访问部署后的 URL，测试 Prompt Auditing
3. **（可选）启用 Leaderboard**：选择上述方案之一

有问题随时问我！

