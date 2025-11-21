#!/usr/bin/env python3
"""
提示词生成器 - 从种子提示词生成组合和变体
Prompt Generator - Generate combinations and variations from seed prompts
"""

import csv
import random
import json
from itertools import combinations
from datetime import datetime

def load_seed_prompts(filename='seed_prompts.csv'):
    """加载种子提示词"""
    prompts = {
        'good': [],
        'bad': []
    }
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompts[row['label']].append(row)
    
    return prompts

def combine_bad_prompts(bad_prompts, num_combinations=50, max_violations=3):
    """
    组合多个坏提示词，创建包含多种违规的复杂案例
    """
    combined = []
    
    for _ in range(num_combinations):
        # 随机选择 2-max_violations 个违规
        num_violations = random.randint(2, max_violations)
        selected = random.sample(bad_prompts, num_violations)
        
        # 提取提示词文本
        prompt_texts = [p['prompt'] for p in selected]
        
        # 组合成一个提示词
        combined_prompt = " ".join(prompt_texts)
        
        # 记录违规的分类
        categories = list(set([p['category'] for p in selected]))
        subcategories = [p['subcategory'] for p in selected]
        standard_ids = [p['standard_id'] for p in selected]
        
        combined.append({
            'type': 'combined_bad',
            'num_violations': num_violations,
            'categories': categories,
            'subcategories': subcategories,
            'standard_ids': standard_ids,
            'prompt': combined_prompt
        })
    
    return combined

def add_good_context_to_bad(bad_prompts, good_prompts, num_mixed=30):
    """
    在坏提示词中添加好的元素，创建混合案例
    """
    mixed = []
    
    for _ in range(num_mixed):
        bad = random.choice(bad_prompts)
        good = random.choice(good_prompts)
        
        # 50% 概率：好的开头 + 坏的内容
        # 50% 概率：坏的内容 + 好的结尾
        if random.random() < 0.5:
            mixed_prompt = f"{good['prompt']} {bad['prompt']}"
            dominant = 'bad'
        else:
            mixed_prompt = f"{bad['prompt']} {good['prompt']}"
            dominant = 'bad'
        
        mixed.append({
            'type': 'mixed',
            'dominant': dominant,
            'bad_category': bad['category'],
            'bad_subcategory': bad['subcategory'],
            'bad_standard_id': bad['standard_id'],
            'good_category': good['category'],
            'prompt': mixed_prompt
        })
    
    return mixed

def create_subtle_violations(bad_prompts, num_subtle=20):
    """
    创建微妙的违规案例（更难检测）
    """
    subtle = []
    
    # 软化语言的模板
    softening_templates = [
        "You might want to consider {action}.",
        "It could be helpful to {action}.",
        "Some users find it useful to {action}.",
        "You may want to {action}.",
        "Consider {action} if appropriate.",
    ]
    
    for _ in range(num_subtle):
        bad = random.choice(bad_prompts)
        template = random.choice(softening_templates)
        
        # 提取核心行动
        # 简化版本：直接使用原文但添加软化前缀
        subtle_prompt = f"{template.replace('{action}', 'follow this approach')} {bad['prompt']}"
        
        subtle.append({
            'type': 'subtle_violation',
            'original_category': bad['category'],
            'original_subcategory': bad['subcategory'],
            'original_standard_id': bad['standard_id'],
            'prompt': subtle_prompt
        })
    
    return subtle

def generate_category_specific_combinations(bad_prompts):
    """
    生成特定分类内的组合（例如，多种操纵手法）
    """
    category_combos = []
    
    # 按分类分组
    by_category = {}
    for p in bad_prompts:
        cat = p['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(p)
    
    # 为每个分类生成组合
    for category, prompts in by_category.items():
        if len(prompts) >= 2:
            # 生成 2-3 个同类违规的组合
            for _ in range(min(10, len(prompts) // 2)):
                num_combine = random.randint(2, min(3, len(prompts)))
                selected = random.sample(prompts, num_combine)
                
                combined_text = " ".join([p['prompt'] for p in selected])
                
                category_combos.append({
                    'type': 'category_specific',
                    'category': category,
                    'num_violations': num_combine,
                    'subcategories': [p['subcategory'] for p in selected],
                    'standard_ids': [p['standard_id'] for p in selected],
                    'prompt': combined_text
                })
    
    return category_combos

def save_generated_prompts(all_prompts, filename='generated_prompts.csv'):
    """保存生成的提示词到 CSV"""
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['id', 'type', 'expected_label', 'categories', 'details', 'prompt']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for idx, prompt_data in enumerate(all_prompts, 1):
            # 确定预期标签
            if prompt_data['type'] in ['combined_bad', 'subtle_violation', 'category_specific']:
                expected_label = 'FAIL'
            elif prompt_data['type'] == 'mixed':
                expected_label = 'FAIL' if prompt_data.get('dominant') == 'bad' else 'UNCERTAIN'
            else:
                expected_label = 'UNKNOWN'
            
            # 提取分类信息
            if 'categories' in prompt_data:
                categories = ', '.join(prompt_data['categories'])
            elif 'category' in prompt_data:
                categories = prompt_data['category']
            elif 'bad_category' in prompt_data:
                categories = prompt_data['bad_category']
            elif 'original_category' in prompt_data:
                categories = prompt_data['original_category']
            else:
                categories = ''
            
            # 创建详情 JSON
            details = {k: v for k, v in prompt_data.items() if k not in ['prompt', 'type']}
            
            writer.writerow({
                'id': f'GEN_{idx:04d}',
                'type': prompt_data['type'],
                'expected_label': expected_label,
                'categories': categories,
                'details': json.dumps(details, ensure_ascii=False),
                'prompt': prompt_data['prompt']
            })
    
    print(f"✅ 已保存 {len(all_prompts)} 个生成的提示词到 {filename}")

def generate_statistics(all_prompts):
    """生成统计信息"""
    stats = {
        'total': len(all_prompts),
        'by_type': {},
        'by_expected_label': {}
    }
    
    for prompt in all_prompts:
        # 按类型统计
        ptype = prompt['type']
        stats['by_type'][ptype] = stats['by_type'].get(ptype, 0) + 1
    
    return stats

def main():
    print("="*80)
    print("提示词生成器 / Prompt Generator")
    print("="*80)
    
    # 加载种子提示词
    print("\n📂 加载种子提示词...")
    seed_prompts = load_seed_prompts('seed_prompts.csv')
    print(f"   - 好的提示词: {len(seed_prompts['good'])} 个")
    print(f"   - 坏的提示词: {len(seed_prompts['bad'])} 个")
    
    # 生成组合
    print("\n🔄 生成提示词组合...")
    
    print("   1. 组合多个违规...")
    combined_bad = combine_bad_prompts(seed_prompts['bad'], num_combinations=50, max_violations=3)
    print(f"      ✓ 生成 {len(combined_bad)} 个组合违规提示词")
    
    print("   2. 创建混合案例...")
    mixed = add_good_context_to_bad(seed_prompts['bad'], seed_prompts['good'], num_mixed=30)
    print(f"      ✓ 生成 {len(mixed)} 个混合提示词")
    
    print("   3. 创建微妙违规...")
    subtle = create_subtle_violations(seed_prompts['bad'], num_subtle=20)
    print(f"      ✓ 生成 {len(subtle)} 个微妙违规提示词")
    
    print("   4. 生成分类特定组合...")
    category_specific = generate_category_specific_combinations(seed_prompts['bad'])
    print(f"      ✓ 生成 {len(category_specific)} 个分类特定组合")
    
    # 合并所有生成的提示词
    all_generated = combined_bad + mixed + subtle + category_specific
    
    # 保存
    print("\n💾 保存生成的提示词...")
    save_generated_prompts(all_generated, 'generated_prompts.csv')
    
    # 统计
    print("\n📊 生成统计:")
    stats = generate_statistics(all_generated)
    print(f"   总计: {stats['total']} 个提示词")
    print(f"\n   按类型分布:")
    for ptype, count in stats['by_type'].items():
        print(f"      - {ptype}: {count} 个")
    
    # 保存统计信息
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stats_filename = f"generation_stats_{timestamp}.json"
    with open(stats_filename, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"\n   统计信息已保存到: {stats_filename}")
    
    print("\n" + "="*80)
    print("✅ 提示词生成完成！")
    print("="*80)
    print(f"\n生成的文件:")
    print(f"  - generated_prompts.csv ({stats['total']} 个提示词)")
    print(f"  - {stats_filename} (统计信息)")
    print(f"\n这些提示词可以用于:")
    print(f"  1. 训练和测试审计模型")
    print(f"  2. Benchmark 不同 AI 模型的检测能力")
    print(f"  3. 评估审计系统的鲁棒性")
    print(f"  4. 生成更多训练数据")

if __name__ == "__main__":
    main()




