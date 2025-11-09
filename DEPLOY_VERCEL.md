# 🚀 Vercel 部署指南

## 📋 前置准备

### 1. 安装 Vercel CLI（如果还没有）

```bash
npm install -g vercel
```

### 2. 登录 Vercel

```bash
vercel login
```

---

## 🔧 部署步骤

### 方法一：使用 Vercel CLI（推荐）

#### 1. 确保所有变更已保存

```bash
# 查看修改的文件
git status
```

#### 2. 添加并提交变更

```bash
# 添加所有变更
git add .

# 提交变更（附带描述）
git commit -m "Update: Add Material Design dropdown and security fixes"
```

#### 3. 部署到 Vercel

**首次部署（预览环境）：**
```bash
vercel
```

系统会询问几个问题：
- `Set up and deploy?` → 输入 `Y`
- `Which scope?` → 选择你的账号
- `Link to existing project?` → 如果是新项目选 `N`
- `What's your project's name?` → 输入项目名称（如 `prompt-auditing`）
- `In which directory is your code located?` → 按 Enter（当前目录）

**部署到生产环境：**
```bash
vercel --prod
```

#### 4. 配置环境变量

在 Vercel 仪表板或使用 CLI 设置：

```bash
# 方式1：使用 CLI
vercel env add ZZZ_API_KEY

# 系统会提示：
# What's the value of ZZZ_API_KEY?
# 粘贴你的 API key

# 为哪些环境设置？选择：
# Production, Preview, Development (通常选择全部)
```

或者在 Vercel Dashboard 中设置：
1. 进入项目设置
2. 找到 "Environment Variables"
3. 添加：
   - Name: `ZZZ_API_KEY`
   - Value: 你的 API key
   - Environments: Production, Preview, Development

同样设置 `ZZZ_BASE_URL`（如果需要）：
```bash
vercel env add ZZZ_BASE_URL
# Value: https://api.zhizengzeng.com/v1/
```

#### 5. 查看部署状态

```bash
# 查看最近的部署
vercel list

# 查看项目日志
vercel logs
```

---

### 方法二：通过 GitHub 自动部署（更推荐）

#### 1. 确保代码已推送到 GitHub

```bash
# 添加变更
git add .

# 提交变更
git commit -m "Update: Add Material Design dropdown and security fixes"

# 推送到 GitHub
git push origin main
```

#### 2. 连接 Vercel 到 GitHub

1. 访问 [Vercel Dashboard](https://vercel.com)
2. 点击 "Add New..." → "Project"
3. 从 GitHub 导入你的仓库
4. Vercel 会自动检测到 Flask 应用

#### 3. 配置项目

- **Framework Preset**: 选择 "Other"
- **Build Command**: 留空（Vercel 会自动处理）
- **Output Directory**: 留空
- **Install Command**: `pip install -r requirements.txt`

#### 4. 添加环境变量

在项目设置中添加：
- `ZZZ_API_KEY`: 你的 API key
- `ZZZ_BASE_URL`: `https://api.zhizengzeng.com/v1/`

#### 5. 点击 "Deploy"

之后每次 `git push`，Vercel 都会自动部署！

---

## ✅ 验证部署

部署完成后，你会得到一个 URL，例如：
```
https://prompt-auditing.vercel.app
```

访问这个 URL，检查：
- ✅ 页面正常加载
- ✅ 下拉菜单可以正常展开
- ✅ 可以选择不同的 AI 模型
- ✅ 可以提交审计请求

---

## 🔍 常见问题

### Q: 部署后 API 调用失败？
**A:** 检查环境变量是否正确设置：
```bash
vercel env ls
```

### Q: 需要更新环境变量？
**A:** 更新后需要重新部署：
```bash
vercel env rm ZZZ_API_KEY
vercel env add ZZZ_API_KEY
vercel --prod
```

### Q: 如何查看错误日志？
**A:** 使用 Vercel CLI：
```bash
vercel logs --follow
```
或在 Vercel Dashboard 的 "Logs" 标签查看。

### Q: 如何回滚到之前的版本？
**A:** 在 Vercel Dashboard：
1. 进入 "Deployments"
2. 找到之前的部署
3. 点击 "..." → "Promote to Production"

---

## 📝 快速命令参考

```bash
# 首次部署（预览）
vercel

# 部署到生产环境
vercel --prod

# 查看部署列表
vercel list

# 查看日志
vercel logs

# 添加环境变量
vercel env add <NAME>

# 查看环境变量
vercel env ls

# 删除环境变量
vercel env rm <NAME>

# 打开项目仪表板
vercel open
```

---

## 🎯 重要提示

1. **不要提交 `.env` 文件到 Git**（已在 `.gitignore` 中）
2. **环境变量必须在 Vercel 设置**，不能使用本地 `.env`
3. **每次修改代码后**，需要 commit 并部署：
   ```bash
   git add .
   git commit -m "Your changes"
   vercel --prod
   ```
4. **API Key 安全**：确保 API key 只在 Vercel 环境变量中设置

---

## 🌐 域名配置（可选）

如果你有自己的域名：

1. 在 Vercel Dashboard 进入项目设置
2. 点击 "Domains"
3. 添加你的域名
4. 按照指引配置 DNS

---

**部署成功后，你的应用就可以在互联网上访问了！** 🎉

