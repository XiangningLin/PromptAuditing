#!/usr/bin/env python3
"""
数据集分析工具 - 分析和可视化种子提示词数据集
Dataset Analysis Tool - Analyze and visualize seed prompts dataset
"""

import pandas as pd
import json
from collections import Counter, defaultdict

def analyze_seed_prompts(filename='seed_prompts.csv'):
    """分析种子提示词数据集"""
    df = pd.read_csv(filename)
    
    print("\n" + "="*80)
    print("📊 种子提示词数据集分析 / Seed Prompts Dataset Analysis")
    print("="*80)
    
    # 基本统计
    print("\n📈 基本统计 / Basic Statistics:")
    print(f"   总提示词数 / Total Prompts: {len(df)}")
    print(f"   好例子 / Good Examples: {len(df[df['label']=='good'])} ({len(df[df['label']=='good'])/len(df)*100:.1f}%)")
    print(f"   坏例子 / Bad Examples: {len(df[df['label']=='bad'])} ({len(df[df['label']=='bad'])/len(df)*100:.1f}%)")
    print(f"   分类数 / Categories: {df['category'].nunique()}")
    print(f"   子分类数 / Subcategories: {df['subcategory'].nunique()}")
    
    # 按分类统计
    print("\n📂 按分类统计 / Statistics by Category:")
    print("-" * 80)
    print(f"{'Category':<35} {'Good':<8} {'Bad':<8} {'Total':<8}")
    print("-" * 80)
    
    for category in df['category'].unique():
        cat_df = df[df['category'] == category]
        good_count = len(cat_df[cat_df['label'] == 'good'])
        bad_count = len(cat_df[cat_df['label'] == 'bad'])
        total = len(cat_df)
        print(f"{category:<35} {good_count:<8} {bad_count:<8} {total:<8}")
    
    print("-" * 80)
    
    # 按子分类统计
    print("\n📋 按子分类统计 / Statistics by Subcategory:")
    print("-" * 80)
    print(f"{'Subcategory':<35} {'ID':<6} {'Good':<6} {'Bad':<6} {'Total':<6}")
    print("-" * 80)
    
    for _, row in df.groupby(['category', 'subcategory', 'standard_id']).size().reset_index(name='count').iterrows():
        subcat_df = df[(df['category'] == row['category']) & 
                       (df['subcategory'] == row['subcategory'])]
        good_count = len(subcat_df[subcat_df['label'] == 'good'])
        bad_count = len(subcat_df[subcat_df['label'] == 'bad'])
        
        # 截断长名称
        subcat_name = row['subcategory'][:33] + '..' if len(row['subcategory']) > 35 else row['subcategory']
        
        print(f"{subcat_name:<35} {row['standard_id']:<6} {good_count:<6} {bad_count:<6} {row['count']:<6}")
    
    print("-" * 80)
    
    # 提示词长度分析
    print("\n📏 提示词长度分析 / Prompt Length Analysis:")
    df['length'] = df['prompt'].str.len()
    df['word_count'] = df['prompt'].str.split().str.len()
    
    print(f"   平均字符数 / Avg Characters: {df['length'].mean():.0f}")
    print(f"   平均词数 / Avg Words: {df['word_count'].mean():.0f}")
    print(f"   最短 / Min: {df['length'].min()} 字符")
    print(f"   最长 / Max: {df['length'].max()} 字符")
    
    print("\n   按标签分组 / By Label:")
    for label in ['good', 'bad']:
        label_df = df[df['label'] == label]
        print(f"   {label.upper():<6} - 平均: {label_df['length'].mean():.0f} 字符, {label_df['word_count'].mean():.0f} 词")
    
    return df

def analyze_generated_prompts(filename='generated_prompts.csv'):
    """分析生成的提示词数据集"""
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"\n⚠️  文件 {filename} 不存在。请先运行 generate_prompts.py")
        return None
    
    print("\n" + "="*80)
    print("🔄 生成提示词数据集分析 / Generated Prompts Dataset Analysis")
    print("="*80)
    
    # 基本统计
    print("\n📈 基本统计 / Basic Statistics:")
    print(f"   总提示词数 / Total Prompts: {len(df)}")
    
    # 按类型统计
    print("\n📂 按类型统计 / Statistics by Type:")
    print("-" * 80)
    print(f"{'Type':<30} {'Count':<10} {'Percentage':<12}")
    print("-" * 80)
    
    for ptype, count in df['type'].value_counts().items():
        percentage = count / len(df) * 100
        print(f"{ptype:<30} {count:<10} {percentage:>6.1f}%")
    
    print("-" * 80)
    
    # 按预期标签统计
    print("\n🏷️  按预期标签统计 / Statistics by Expected Label:")
    print("-" * 80)
    print(f"{'Expected Label':<30} {'Count':<10} {'Percentage':<12}")
    print("-" * 80)
    
    for label, count in df['expected_label'].value_counts().items():
        percentage = count / len(df) * 100
        print(f"{label:<30} {count:<10} {percentage:>6.1f}%")
    
    print("-" * 80)
    
    # 提示词长度分析
    print("\n📏 提示词长度分析 / Prompt Length Analysis:")
    df['length'] = df['prompt'].str.len()
    df['word_count'] = df['prompt'].str.split().str.len()
    
    print(f"   平均字符数 / Avg Characters: {df['length'].mean():.0f}")
    print(f"   平均词数 / Avg Words: {df['word_count'].mean():.0f}")
    print(f"   最短 / Min: {df['length'].min()} 字符")
    print(f"   最长 / Max: {df['length'].max()} 字符")
    
    print("\n   按类型分组 / By Type:")
    for ptype in df['type'].unique():
        type_df = df[df['type'] == ptype]
        print(f"   {ptype:<25} - 平均: {type_df['length'].mean():.0f} 字符, {type_df['word_count'].mean():.0f} 词")
    
    # 分析组合违规
    print("\n🔗 组合违规分析 / Combined Violations Analysis:")
    combined_df = df[df['type'].isin(['combined_bad', 'category_specific'])]
    
    if len(combined_df) > 0:
        details_list = combined_df['details'].apply(json.loads)
        
        # 统计违规数量分布
        violation_counts = []
        for details in details_list:
            if 'num_violations' in details:
                violation_counts.append(details['num_violations'])
        
        if violation_counts:
            counter = Counter(violation_counts)
            print("\n   违规数量分布 / Violation Count Distribution:")
            for num, count in sorted(counter.items()):
                print(f"   {num} 个违规 / violations: {count} 个提示词 ({count/len(violation_counts)*100:.1f}%)")
    
    return df

def compare_datasets(seed_df, generated_df):
    """比较种子数据集和生成数据集"""
    if generated_df is None:
        return
    
    print("\n" + "="*80)
    print("🔍 数据集对比 / Dataset Comparison")
    print("="*80)
    
    print("\n📊 数量对比 / Quantity Comparison:")
    print(f"   种子提示词 / Seed Prompts: {len(seed_df)}")
    print(f"   生成提示词 / Generated Prompts: {len(generated_df)}")
    print(f"   总计 / Total: {len(seed_df) + len(generated_df)}")
    print(f"   增长率 / Growth Rate: {len(generated_df)/len(seed_df)*100:.1f}%")
    
    print("\n📏 长度对比 / Length Comparison:")
    seed_df['length'] = seed_df['prompt'].str.len()
    generated_df['length'] = generated_df['prompt'].str.len()
    
    print(f"   种子提示词平均长度 / Seed Avg: {seed_df['length'].mean():.0f} 字符")
    print(f"   生成提示词平均长度 / Generated Avg: {generated_df['length'].mean():.0f} 字符")
    print(f"   差异 / Difference: {generated_df['length'].mean() - seed_df['length'].mean():.0f} 字符 "
          f"({(generated_df['length'].mean() / seed_df['length'].mean() - 1) * 100:+.1f}%)")

def export_summary(seed_df, generated_df, output_file='dataset_summary.json'):
    """导出数据集摘要"""
    summary = {
        'seed_prompts': {
            'total': len(seed_df),
            'good': len(seed_df[seed_df['label'] == 'good']),
            'bad': len(seed_df[seed_df['label'] == 'bad']),
            'categories': seed_df['category'].nunique(),
            'subcategories': seed_df['subcategory'].nunique(),
            'avg_length': int(seed_df['prompt'].str.len().mean()),
            'by_category': {}
        }
    }
    
    # 按分类统计
    for category in seed_df['category'].unique():
        cat_df = seed_df[seed_df['category'] == category]
        summary['seed_prompts']['by_category'][category] = {
            'total': len(cat_df),
            'good': len(cat_df[cat_df['label'] == 'good']),
            'bad': len(cat_df[cat_df['label'] == 'bad'])
        }
    
    # 生成提示词统计
    if generated_df is not None:
        summary['generated_prompts'] = {
            'total': len(generated_df),
            'avg_length': int(generated_df['prompt'].str.len().mean()),
            'by_type': {}
        }
        
        for ptype in generated_df['type'].unique():
            type_df = generated_df[generated_df['type'] == ptype]
            summary['generated_prompts']['by_type'][ptype] = {
                'count': len(type_df),
                'percentage': round(len(type_df) / len(generated_df) * 100, 1)
            }
    
    # 总计
    total_prompts = len(seed_df) + (len(generated_df) if generated_df is not None else 0)
    summary['total_dataset'] = {
        'total_prompts': total_prompts,
        'seed_prompts': len(seed_df),
        'generated_prompts': len(generated_df) if generated_df is not None else 0
    }
    
    # 保存
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 数据集摘要已保存到: {output_file}")

def main():
    print("\n" + "="*80)
    print("🔬 数据集分析工具 / Dataset Analysis Tool")
    print("="*80)
    
    # 分析种子提示词
    seed_df = analyze_seed_prompts('seed_prompts.csv')
    
    # 分析生成的提示词
    generated_df = analyze_generated_prompts('generated_prompts.csv')
    
    # 对比数据集
    compare_datasets(seed_df, generated_df)
    
    # 导出摘要
    export_summary(seed_df, generated_df, 'dataset_summary.json')
    
    print("\n" + "="*80)
    print("✅ 分析完成！/ Analysis Complete!")
    print("="*80)
    
    print("\n📁 生成的文件 / Generated Files:")
    print("   - dataset_summary.json (数据集摘要)")
    
    print("\n💡 使用建议 / Usage Suggestions:")
    print("   1. 使用种子数据训练基础模型")
    print("   2. 使用生成数据测试模型鲁棒性")
    print("   3. 定期运行 generate_prompts.py 生成新的测试案例")
    print("   4. 根据模型表现调整种子数据")

if __name__ == "__main__":
    main()




