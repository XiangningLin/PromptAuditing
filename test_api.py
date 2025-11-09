#!/usr/bin/env python3
"""
测试智增增 API 配置
Test Zhizengzeng API Configuration
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
# 优先使用 ZZZ_API_KEY，向后兼容 OPENAI_API_KEY
API_KEY = os.environ.get("ZZZ_API_KEY") or os.environ.get("OPENAI_API_KEY")
BASE_URL = os.environ.get("ZZZ_BASE_URL") or os.environ.get("OPENAI_BASE_URL", "https://api.zhizengzeng.com/v1/")

# 检查 API Key 是否存在
if not API_KEY:
    print("❌ 错误：未找到 API Key！")
    print("❌ Error: API Key not found!")
    print("\n请设置环境变量 / Please set environment variable:")
    print("  export ZZZ_API_KEY='your-api-key-here'")
    print("\n或者在项目根目录创建 .env 文件：")
    print("Or create a .env file in project root:")
    print("  ZZZ_API_KEY=your-api-key-here")
    exit(1)

print("=" * 60)
print("智增增 API 配置测试")
print("Zhizengzeng API Configuration Test")
print("=" * 60)
print(f"\n✓ API Key: {API_KEY[:20]}...{API_KEY[-10:]}")
print(f"✓ Base URL: {BASE_URL}")
print("\n正在测试连接...\nTesting connection...\n")

try:
    # 创建客户端（新版 OpenAI 包方式）
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )
    
    # 测试简单的聊天请求
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'API connection successful!' in Chinese."}
        ],
        max_tokens=50
    )
    
    result = response.choices[0].message.content
    
    print("✅ 连接成功！/ Connection Successful!")
    print(f"\n模型响应 / Model Response:")
    print(f"  {result}")
    print(f"\n使用的模型 / Model Used: {response.model}")
    print(f"Token 使用 / Tokens Used: {response.usage.total_tokens}")
    
    print("\n" + "=" * 60)
    print("🎉 配置正确！应用可以正常使用。")
    print("🎉 Configuration is correct! App is ready to use.")
    print("=" * 60)
    
except Exception as e:
    print("❌ 连接失败！/ Connection Failed!")
    print(f"\n错误信息 / Error Message:")
    print(f"  {str(e)}")
    print("\n请检查：/ Please check:")
    print("  1. API Key 是否正确 / Is API Key correct?")
    print("  2. Base URL 是否正确 / Is Base URL correct?")
    print("  3. 网络连接是否正常 / Is network connection working?")
    print("  4. .env 文件是否存在 / Does .env file exist?")
    print("\n" + "=" * 60)
    exit(1)

