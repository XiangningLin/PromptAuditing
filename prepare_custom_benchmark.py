#!/usr/bin/env python3
"""
准备自定义 Benchmark 数据集
从 benign 和 violation 数据集中采样指定数量
"""

import pandas as pd
import sys

def prepare_custom_dataset(n_good=10, n_bad=30, output_file='custom_benchmark.csv'):
    """准备自定义数据集"""
    
    print(f"\n📊 准备自定义 Benchmark 数据集")
    print(f"{'='*60}")
    print(f"目标: {n_good} 条好的 + {n_bad} 条坏的 = {n_good + n_bad} 条")
    print()
    
    # 读取数据
    print("读取数据集...")
    benign = pd.read_csv('benchmark_benign_prompts.csv')
    violation = pd.read_csv('benchmark_violation_prompts.csv')
    
    print(f"  - 好的数据: {len(benign)} 条")
    print(f"  - 坏的数据: {len(violation)} 条")
    
    # 检查数据是否充足
    if len(benign) < n_good:
        print(f"\n❌ 错误: 好的数据不足 (需要 {n_good}, 只有 {len(benign)})")
        sys.exit(1)
    
    if len(violation) < n_bad:
        print(f"\n❌ 错误: 坏的数据不足 (需要 {n_bad}, 只有 {len(violation)})")
        sys.exit(1)
    
    # 随机采样
    print(f"\n采样数据...")
    sampled_good = benign.sample(n=n_good, random_state=42)
    sampled_bad = violation.sample(n=n_bad, random_state=42)
    
    # 合并
    combined = pd.concat([sampled_good, sampled_bad], ignore_index=True)
    
    # 打乱顺序
    combined = combined.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # 保存
    combined.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n✅ 成功创建数据集: {output_file}")
    print(f"   - 总计: {len(combined)} 条")
    print(f"   - 好的: {len(sampled_good)} 条")
    print(f"   - 坏的: {len(sampled_bad)} 条")
    print()
    print(f"运行 Benchmark:")
    print(f"  python3 benchmark.py --prompt-file {output_file}")
    print()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='准备自定义 Benchmark 数据集')
    parser.add_argument('--good', type=int, default=10, help='好的数据数量 (default: 10)')
    parser.add_argument('--bad', type=int, default=30, help='坏的数据数量 (default: 30)')
    parser.add_argument('--output', type=str, default='custom_benchmark.csv', help='输出文件名')
    
    args = parser.parse_args()
    
    prepare_custom_dataset(args.good, args.bad, args.output)

