#!/usr/bin/env python3
"""
Generate a benchmark leaderboard from one or more benchmark result files.

Usage examples:
    python benchmark_leaderboard.py
    python benchmark_leaderboard.py --results benchmark_results_20251110_161654.json
    python benchmark_leaderboard.py --results file1.json file2.json --top 5
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional


RESULTS_PATTERN = "benchmark_results_*.json"


@dataclass
class ModelStats:
    """Aggregated statistics for a single model across result files."""

    name: str
    total_tests: int = 0
    success_tests: int = 0
    correct_assessments: int = 0
    latency_sum: float = 0.0
    latency_count: int = 0
    total_tokens: int = 0
    sources: List[Path] = field(default_factory=list)

    def update(self, data: Dict, source: Path) -> None:
        """Merge statistics from a summary entry."""
        tests = data.get("total_tests", 0) or 0
        successes = data.get("success_tests", 0) or 0
        correct = data.get("correct_assessments", 0) or 0
        avg_latency = data.get("avg_latency")
        latencies = data.get("latencies")
        tokens = data.get("total_tokens", 0) or 0

        self.total_tests += tests
        self.success_tests += successes
        self.correct_assessments += correct
        self.total_tokens += tokens

        # Prefer precise latency sum if we have individual latencies, otherwise use avg * count
        if isinstance(latencies, list) and latencies:
            self.latency_sum += sum(latencies)
            self.latency_count += len(latencies)
        elif avg_latency is not None and tests:
            self.latency_sum += float(avg_latency) * tests
            self.latency_count += tests

        if source not in self.sources:
            self.sources.append(source)

    @property
    def accuracy(self) -> float:
        if self.total_tests == 0:
            return 0.0
        return self.correct_assessments / self.total_tests

    @property
    def success_rate(self) -> float:
        if self.total_tests == 0:
            return 0.0
        return self.success_tests / self.total_tests

    @property
    def avg_latency(self) -> Optional[float]:
        if self.latency_count == 0:
            return None
        return self.latency_sum / self.latency_count

    @property
    def avg_tokens(self) -> Optional[float]:
        if self.success_tests == 0:
            return None
        return self.total_tokens / self.success_tests


def discover_latest_results() -> List[Path]:
    """Return the newest benchmark result file if available."""
    files = sorted(Path(".").glob(RESULTS_PATTERN), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[:1]


def load_leaderboard(paths: Iterable[Path]) -> Dict[str, ModelStats]:
    """Aggregate statistics from the given benchmark result files."""
    leaderboard: Dict[str, ModelStats] = {}

    for path in paths:
        try:
            with path.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
        except FileNotFoundError:
            print(f"[WARN] Benchmark file not found: {path}", file=sys.stderr)
            continue
        except json.JSONDecodeError as exc:
            print(f"[WARN] Failed to parse {path}: {exc}", file=sys.stderr)
            continue

        summary = payload.get("summary")
        if not summary:
            print(f"[WARN] No summary section in {path}", file=sys.stderr)
            continue

        for model_id, data in summary.items():
            name = data.get("name", model_id)
            model_stats = leaderboard.setdefault(model_id, ModelStats(name=name))
            model_stats.update(data, source=path)

    return leaderboard


def format_percentage(value: float) -> str:
    return f"{value * 100:5.1f}%"


def build_table(models: Iterable[ModelStats], top: Optional[int]) -> str:
    """Return a formatted leaderboard table."""
    header = (
        f"{'Rank':>4}  {'Model':<28}  {'Accuracy':>9}  {'Success':>9}  "
        f"{'Tests':>5}  {'Avg Latency':>11}  {'Avg Tokens':>11}"
    )
    rows = [header, "-" * len(header)]

    sorted_models = sorted(
        models,
        key=lambda m: (
            round(m.accuracy, 6),
            round(m.success_rate, 6),
            m.total_tests,
        ),
        reverse=True,
    )

    if top is not None:
        sorted_models = sorted_models[:top]

    for idx, model in enumerate(sorted_models, start=1):
        accuracy = format_percentage(model.accuracy)
        success = format_percentage(model.success_rate)
        tests = f"{model.total_tests:5d}"
        if model.avg_latency is None:
            avg_latency = "   N/A"
        else:
            avg_latency = f"{model.avg_latency:7.2f}s"
        if model.avg_tokens is None:
            avg_tokens = "     N/A"
        else:
            avg_tokens = f"{model.avg_tokens:7.1f}"

        rows.append(
            f"{idx:>4}  {model.name:<28}  {accuracy:>9}  {success:>9}  "
            f"{tests}  {avg_latency:>11}  {avg_tokens:>11}"
        )

    return "\n".join(rows)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a benchmark leaderboard from result files.")
    parser.add_argument(
        "--results",
        nargs="*",
        type=Path,
        help="Paths to benchmark_results_*.json files. Defaults to the newest file if omitted.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="Limit the number of rows shown in the leaderboard.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    if args.results:
        paths = [path for path in args.results if path]
    else:
        paths = discover_latest_results()
        if paths:
            print(f"[INFO] Using latest benchmark file: {paths[0].name}")

    if not paths:
        print("No benchmark result files found. Run benchmark.py first.", file=sys.stderr)
        return 1

    leaderboard = load_leaderboard(paths)
    if not leaderboard:
        print("No leaderboard data extracted. Check the provided files.", file=sys.stderr)
        return 1

    print(build_table(leaderboard.values(), args.top))

    # Optional: list data sources when multiple files were aggregated
    unique_sources = sorted({src for stats in leaderboard.values() for src in stats.sources})
    if len(unique_sources) > 1:
        print("\nSources:")
        for src in unique_sources:
            print(f"  - {src}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())




