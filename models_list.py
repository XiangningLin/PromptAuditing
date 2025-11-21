"""
智增增支持的模型完整列表
Zhizengzeng Supported Models Complete List
Updated based on 2025.11.20 Official Log - Consolidated
"""

ZHIZENGZENG_MODELS = {
    # OpenAI Models
    "openai": [
        # GPT-5.1 Series (Nov 2025)
        {"id": "gpt-5.1", "name": "GPT-5.1", "provider": "OpenAI", "type": "chat"},
        {"id": "gpt-5.1-chat-latest", "name": "GPT-5.1 Chat Latest", "provider": "OpenAI", "type": "chat"},
        
        # # GPT-5 Pro Series (Oct 2025)
        # {"id": "gpt-5-pro", "name": "GPT-5 Pro", "provider": "OpenAI", "type": "chat"},
        # {"id": "gpt-5-pro-2025-10-06", "name": "GPT-5 Pro (Oct 06)", "provider": "OpenAI", "type": "chat"},
        
        # # GPT-5 Base Series (Aug 2025)
        # {"id": "gpt-5", "name": "GPT-5", "provider": "OpenAI", "type": "chat"},
        # {"id": "gpt-5-mini", "name": "GPT-5 Mini", "provider": "OpenAI", "type": "chat"},
        # {"id": "gpt-5-nano", "name": "GPT-5 Nano", "provider": "OpenAI", "type": "chat"},
        
        # # GPT-4.1 Series (Apr 2025)
        # {"id": "gpt-4.1", "name": "GPT-4.1", "provider": "OpenAI", "type": "chat"},
        # {"id": "gpt-4.1-mini", "name": "GPT-4.1 Mini", "provider": "OpenAI", "type": "chat"},
        # {"id": "gpt-4.1-nano", "name": "GPT-4.1 Nano", "provider": "OpenAI", "type": "chat"},
        
        # # GPT-4.5 Series (Feb 2025)
        # {"id": "gpt-4.5-preview", "name": "GPT-4.5 Preview", "provider": "OpenAI", "type": "chat"},
        # {"id": "gpt-4.5-preview-2025-02-27", "name": "GPT-4.5 Preview (Feb 27)", "provider": "OpenAI", "type": "chat"},

        # # Baseline
        {"id": "gpt-4o", "name": "GPT-4o", "provider": "OpenAI", "type": "chat"},
    ],

    # Anthropic (Claude) Models
    "anthropic": [
        # 2025 Models (Verified from API)
        {"id": "claude-3-7-sonnet-20250219", "name": "Claude 3.7 Sonnet", "provider": "Anthropic", "type": "chat"},
        {"id": "claude-haiku-4-5-20251001", "name": "Claude Haiku 4.5", "provider": "Anthropic", "type": "chat"},
        {"id": "claude-sonnet-4-5-20250929", "name": "Claude Sonnet 4.5", "provider": "Anthropic", "type": "chat"},
        {"id": "claude-opus-4-1-20250805", "name": "Claude Opus 4.1", "provider": "Anthropic", "type": "chat"},
        
        # Baseline (2024)
        {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet (Baseline)", "provider": "Anthropic", "type": "chat"},
    ],

    # Google (Gemini) Models
    "google": [
        # Gemini 3 Series (Nov 2025)
        {"id": "gemini-3-pro-preview", "name": "Gemini 3 Pro Preview", "provider": "Google", "type": "chat"},
        
        # Gemini 2.5 Series (Jun/Aug 2025)
        {"id": "gemini-2.5-pro", "name": "Gemini 2.5 Pro", "provider": "Google", "type": "chat"},
        {"id": "gemini-2.5-flash-lite", "name": "Gemini 2.5 Flash Lite", "provider": "Google", "type": "chat"},
        
    ],

    # DeepSeek Models
    "deepseek": [
        # DeepSeek V3/R1 Series (Jan/May/Aug 2025)
        {"id": "deepseek-chat", "name": "DeepSeek V3.1 (Chat)", "provider": "DeepSeek", "type": "chat"},
        {"id": "deepseek-reasoner", "name": "DeepSeek R1-0528 (Reasoner)", "provider": "DeepSeek", "type": "chat"},
    ],

    # xAI Models
    "xai": [
        # Grok 4 Series (Jul 2025)
        {"id": "grok-4-0709", "name": "Grok 4 (0709)", "provider": "xAI", "type": "chat"},
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
    """获取推荐用于 benchmark 的所有 2025 Chat 模型"""
    benchmark_list = []
    
    # 遍历所有提供商，收集所有 chat 类型的模型
    for provider, models in ZHIZENGZENG_MODELS.items():
        for model in models:
            if model.get("type") == "chat":
                benchmark_list.append({
                    "id": model["id"], 
                    "name": model["name"], 
                    "provider": model["provider"], 
                    "tier": "2025-All"
                })
    
    return benchmark_list

def print_all_models():
    """打印所有模型"""
    print("\n" + "="*80)
    print("智增增支持的所有模型 (2025 Consolidated + User Custom)")
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
