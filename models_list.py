"""
智增增支持的模型完整列表
Zhizengzeng Supported Models Complete List
"""

ZHIZENGZENG_MODELS = {
    # OpenAI Models
    "openai": [
        {"id": "gpt-4o", "name": "GPT-4o", "provider": "OpenAI", "type": "chat"},
        {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "provider": "OpenAI", "type": "chat"},
        {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "provider": "OpenAI", "type": "chat"},
        {"id": "gpt-4", "name": "GPT-4", "provider": "OpenAI", "type": "chat"},
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "OpenAI", "type": "chat"},
        {"id": "gpt-3.5-turbo-16k", "name": "GPT-3.5 Turbo 16K", "provider": "OpenAI", "type": "chat"},
    ],
    
    # Anthropic Models
    "anthropic": [
        {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet", "provider": "Anthropic", "type": "chat"},
        {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus", "provider": "Anthropic", "type": "chat"},
        {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet", "provider": "Anthropic", "type": "chat"},
        {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku", "provider": "Anthropic", "type": "chat"},
    ],
    
    # DeepSeek Models
    "deepseek": [
        {"id": "deepseek-chat", "name": "DeepSeek Chat", "provider": "DeepSeek", "type": "chat"},
        {"id": "deepseek-coder", "name": "DeepSeek Coder", "provider": "DeepSeek", "type": "chat"},
    ],
    
    # Google Models
    "google": [
        {"id": "gemini-pro", "name": "Gemini Pro", "provider": "Google", "type": "chat"},
        {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "provider": "Google", "type": "chat"},
        {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash", "provider": "Google", "type": "chat"},
    ],
    
    # 阿里 Alibaba Models
    "alibaba": [
        {"id": "qwen-turbo", "name": "通义千问 Turbo", "provider": "Alibaba", "type": "chat"},
        {"id": "qwen-plus", "name": "通义千问 Plus", "provider": "Alibaba", "type": "chat"},
        {"id": "qwen-max", "name": "通义千问 Max", "provider": "Alibaba", "type": "chat"},
        {"id": "qwen-max-longcontext", "name": "通义千问 Max Long", "provider": "Alibaba", "type": "chat"},
    ],
    
    # 百度 Baidu Models
    "baidu": [
        {"id": "ernie-bot", "name": "文心一言", "provider": "Baidu", "type": "chat"},
        {"id": "ernie-bot-turbo", "name": "文心一言 Turbo", "provider": "Baidu", "type": "chat"},
        {"id": "ernie-bot-4", "name": "文心一言 4.0", "provider": "Baidu", "type": "chat"},
    ],
    
    # 智谱 Zhipu Models
    "zhipu": [
        {"id": "glm-4", "name": "ChatGLM-4", "provider": "Zhipu", "type": "chat"},
        {"id": "glm-4-plus", "name": "ChatGLM-4 Plus", "provider": "Zhipu", "type": "chat"},
        {"id": "glm-3-turbo", "name": "ChatGLM-3 Turbo", "provider": "Zhipu", "type": "chat"},
    ],
    
    # 字节 ByteDance Models
    "bytedance": [
        {"id": "doubao-pro-32k", "name": "豆包 Pro 32K", "provider": "ByteDance", "type": "chat"},
        {"id": "doubao-lite-32k", "name": "豆包 Lite 32K", "provider": "ByteDance", "type": "chat"},
    ],
    
    # 百川 Baichuan Models
    "baichuan": [
        {"id": "baichuan2-turbo", "name": "百川2 Turbo", "provider": "Baichuan", "type": "chat"},
        {"id": "baichuan2-turbo-192k", "name": "百川2 Turbo 192K", "provider": "Baichuan", "type": "chat"},
    ],
    
    # 讯飞 iFlytek Models
    "iflytek": [
        {"id": "spark-3.5", "name": "讯飞星火 3.5", "provider": "iFlytek", "type": "chat"},
        {"id": "spark-3.0", "name": "讯飞星火 3.0", "provider": "iFlytek", "type": "chat"},
    ],
    
    # xAI Models
    "xai": [
        {"id": "grok-beta", "name": "Grok Beta", "provider": "xAI", "type": "chat"},
    ],
    
    # Meta Models
    "meta": [
        {"id": "llama-3-70b", "name": "Llama 3 70B", "provider": "Meta", "type": "chat"},
        {"id": "llama-3-8b", "name": "Llama 3 8B", "provider": "Meta", "type": "chat"},
    ],
}

def get_all_models():
    """获取所有模型的扁平列表"""
    all_models = []
    for provider, models in ZHIZENGZENG_MODELS.items():
        all_models.extend(models)
    return all_models

def get_models_by_provider(provider):
    """根据提供商获取模型"""
    return ZHIZENGZENG_MODELS.get(provider, [])

def get_benchmark_models():
    """获取推荐用于 benchmark 的模型（代表性模型）"""
    return [
        # OpenAI 顶级模型
        {"id": "gpt-4o", "name": "GPT-4o", "provider": "OpenAI", "tier": "premium"},
        {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "provider": "OpenAI", "tier": "mid"},
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "OpenAI", "tier": "budget"},
        
        # Anthropic 顶级模型
        {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet", "provider": "Anthropic", "tier": "premium"},
        {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku", "provider": "Anthropic", "tier": "budget"},
        
        # 中国主流模型
        {"id": "deepseek-chat", "name": "DeepSeek Chat", "provider": "DeepSeek", "tier": "mid"},
        {"id": "qwen-max", "name": "通义千问 Max", "provider": "Alibaba", "tier": "premium"},
        {"id": "qwen-turbo", "name": "通义千问 Turbo", "provider": "Alibaba", "tier": "budget"},
        {"id": "glm-4", "name": "ChatGLM-4", "provider": "Zhipu", "tier": "mid"},
        {"id": "ernie-bot-4", "name": "文心一言 4.0", "provider": "Baidu", "tier": "premium"},
        
        # Google
        {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "provider": "Google", "tier": "premium"},
        {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash", "provider": "Google", "tier": "budget"},
    ]

def print_all_models():
    """打印所有模型"""
    print("\n" + "="*80)
    print("智增增支持的所有模型 / All Zhizengzeng Supported Models")
    print("="*80 + "\n")
    
    total = 0
    for provider, models in ZHIZENGZENG_MODELS.items():
        print(f"\n【{provider.upper()}】 ({len(models)} models)")
        print("-" * 80)
        for model in models:
            print(f"  • {model['id']:40} | {model['name']}")
            total += 1
    
    print("\n" + "="*80)
    print(f"总计 / Total: {total} 个模型")
    print("="*80 + "\n")

if __name__ == "__main__":
    print_all_models()
    
    print("\n推荐 Benchmark 模型 / Recommended Benchmark Models:")
    print("-" * 80)
    for model in get_benchmark_models():
        print(f"  [{model['tier']:8}] {model['id']:40} | {model['name']}")

