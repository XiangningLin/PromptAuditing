#!/bin/bash

# 🚀 快速部署脚本 - Vercel
# Quick Deploy Script for Vercel

echo "========================================"
echo "🚀 Prompt Auditing - Vercel 部署"
echo "========================================"
echo ""

# 检查是否有未提交的更改
if [[ -n $(git status -s) ]]; then
    echo "📝 发现未提交的更改..."
    echo ""
    git status -s
    echo ""
    read -p "是否要提交这些更改？(y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        read -p "请输入提交信息: " commit_message
        
        if [ -z "$commit_message" ]; then
            commit_message="Update: Deploy changes"
        fi
        
        echo ""
        echo "📦 添加文件..."
        git add .
        
        echo "💾 提交更改..."
        git commit -m "$commit_message"
        
        echo "✅ 提交完成！"
    else
        echo "⚠️  跳过提交步骤"
    fi
else
    echo "✅ 没有未提交的更改"
fi

echo ""
echo "========================================"
read -p "选择部署环境 (1=预览, 2=生产环境): " -n 1 -r env_choice
echo ""
echo "========================================"
echo ""

if [[ $env_choice == "2" ]]; then
    echo "🚀 部署到生产环境..."
    echo ""
    vercel --prod
else
    echo "🔍 部署到预览环境..."
    echo ""
    vercel
fi

echo ""
echo "========================================"
echo "✅ 部署完成！"
echo "========================================"
echo ""
echo "💡 有用的命令："
echo "  - 查看日志: vercel logs"
echo "  - 查看部署: vercel list"
echo "  - 打开仪表板: vercel open"
echo ""

