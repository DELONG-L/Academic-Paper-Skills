"""Reusable Matplotlib helpers for compact academic paper figures.

This module is intentionally small. Copy or import it into project-local plotting
scripts, then keep figure-specific data loading in the project repository.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import matplotlib

matplotlib.use("Agg", force=True)

import matplotlib.pyplot as plt
import numpy as np


PALETTE: Mapping[str, str] = {
    "method": "#0F4D92",
    "method_light": "#8FB7DD",
    "baseline": "#767676",
    "baseline_light": "#C9CDD1",
    "neutral": "#D9D9D9",
    "boundary": "#B64342",
    "allowed": "#2E7D6B",
    "forbidden": "#B64342",
    "accent": "#D89A00",
    "ink": "#222222",
    "grid": "#E6E8EB",
}

DEFAULT_COLORS: Sequence[str] = (
    PALETTE["method"],
    PALETTE["baseline"],
    PALETTE["boundary"],
    PALETTE["allowed"],
    PALETTE["accent"],
    PALETTE["neutral"],
)


@dataclass(frozen=True)
class FigureStyle:
    font_size: float = 8.0
    label_size: float = 8.0
    tick_size: float = 7.0
    legend_size: float = 7.0
    axes_linewidth: float = 0.8
    line_width: float = 1.4
    marker_size: float = 4.0
    use_tex: bool = False
    font_family: tuple[str, ...] = ("Arial", "Helvetica", "DejaVu Sans", "sans-serif")


def apply_style(style: FigureStyle | None = None) -> FigureStyle:
    """Apply compact publication rcParams and return the style used."""

    style = style or FigureStyle()
    plt.rcParams.update(
        {
            "font.family": list(style.font_family),
            "font.size": style.font_size,
            "axes.labelsize": style.label_size,
            "axes.titlesize": style.label_size,
            "xtick.labelsize": style.tick_size,
            "ytick.labelsize": style.tick_size,
            "legend.fontsize": style.legend_size,
            "axes.linewidth": style.axes_linewidth,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": PALETTE["ink"],
            "axes.labelcolor": PALETTE["ink"],
            "xtick.color": PALETTE["ink"],
            "ytick.color": PALETTE["ink"],
            "legend.frameon": False,
            "lines.linewidth": style.line_width,
            "lines.markersize": style.marker_size,
            "text.usetex": style.use_tex,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )
    return style


def figure_size(target: str = "single", height_ratio: float = 0.62) -> tuple[float, float]:
    """Return final-size figure dimensions in inches."""

    widths = {
        "single": 3.25,
        "double": 6.90,
        "wide": 7.20,
        "half": 4.80,
    }
    if target not in widths:
        raise ValueError(f"unknown target {target!r}; choose one of {sorted(widths)}")
    width = widths[target]
    return width, width * height_ratio


def create_figure(
    nrows: int = 1,
    ncols: int = 1,
    *,
    target: str = "single",
    height_ratio: float = 0.62,
    style: FigureStyle | None = None,
    **kwargs,
):
    """Create a styled figure and flattened axes array."""

    apply_style(style)
    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=figure_size(target, height_ratio),
        squeeze=False,
        **kwargs,
    )
    return fig, axes.ravel()


def clean_axis(ax, *, grid: str | None = "y") -> None:
    """Apply light axis cleanup."""

    if grid == "y":
        ax.grid(axis="y", color=PALETTE["grid"], linewidth=0.6, zorder=0)
    elif grid == "x":
        ax.grid(axis="x", color=PALETTE["grid"], linewidth=0.6, zorder=0)
    elif grid == "both":
        ax.grid(axis="both", color=PALETTE["grid"], linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(length=3, width=0.7)


def grouped_bar(
    ax,
    categories: Sequence[str],
    series: Sequence[Sequence[float]],
    labels: Sequence[str],
    *,
    colors: Sequence[str] | None = None,
    errors: Sequence[Sequence[float]] | None = None,
    ylabel: str | None = None,
    annotate: bool = False,
    value_fmt: str = "{:.2f}",
    hatches: Sequence[str | None] | None = None,
):
    """Draw grouped bars and return the BarContainer objects."""

    values = np.asarray(series, dtype=float)
    if values.ndim != 2:
        raise ValueError("series must be a 2D sequence: n_series x n_categories")
    n_series, n_categories = values.shape
    if len(categories) != n_categories:
        raise ValueError("category count must match series width")
    if len(labels) != n_series:
        raise ValueError("label count must match number of series")

    err = None if errors is None else np.asarray(errors, dtype=float)
    if err is not None and err.shape != values.shape:
        raise ValueError("errors must have the same shape as series")

    colors = list(colors or DEFAULT_COLORS[:n_series])
    hatches = list(hatches or [None] * n_series)
    x = np.arange(n_categories)
    total_width = 0.78
    bar_width = total_width / max(n_series, 1)
    offsets = (np.arange(n_series) - (n_series - 1) / 2.0) * bar_width

    containers = []
    for idx, label in enumerate(labels):
        bars = ax.bar(
            x + offsets[idx],
            values[idx],
            width=bar_width * 0.92,
            label=label,
            color=colors[idx % len(colors)],
            edgecolor=PALETTE["ink"],
            linewidth=0.5,
            yerr=None if err is None else err[idx],
            capsize=2 if err is not None else 0,
            hatch=hatches[idx],
            zorder=3,
        )
        containers.append(bars)
        if annotate:
            annotate_bars(ax, bars, fmt=value_fmt)

    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    if ylabel:
        ax.set_ylabel(ylabel)
    clean_axis(ax, grid="y")
    return containers


def annotate_bars(ax, bars, *, fmt: str = "{:.2f}", fontsize: float = 6.5, padding: float = 1.5) -> None:
    """Annotate bars with their heights."""

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            fmt.format(height),
            xy=(bar.get_x() + bar.get_width() / 2.0, height),
            xytext=(0, padding),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=fontsize,
        )


def line_panel(
    ax,
    x: Sequence[float],
    y_series: Sequence[Sequence[float]],
    labels: Sequence[str],
    *,
    colors: Sequence[str] | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    markers: Sequence[str] | None = None,
):
    """Draw a compact multi-line panel."""

    x_values = np.asarray(x, dtype=float)
    y_values = np.asarray(y_series, dtype=float)
    if y_values.ndim != 2:
        raise ValueError("y_series must be 2D: n_series x len(x)")
    if y_values.shape[1] != len(x_values):
        raise ValueError("each y series must match x length")
    if len(labels) != y_values.shape[0]:
        raise ValueError("label count must match y series count")

    colors = list(colors or DEFAULT_COLORS[: y_values.shape[0]])
    markers = list(markers or ["o", "s", "^", "D", "v", "P"])
    for idx, label in enumerate(labels):
        ax.plot(
            x_values,
            y_values[idx],
            label=label,
            color=colors[idx % len(colors)],
            marker=markers[idx % len(markers)],
            zorder=3,
        )
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    clean_axis(ax, grid="y")
    return ax


def pareto_scatter(
    ax,
    x: Sequence[float],
    y: Sequence[float],
    labels: Sequence[str] | None = None,
    *,
    highlight: Iterable[int] = (),
    xlabel: str | None = None,
    ylabel: str | None = None,
):
    """Draw a small Pareto/frontier-style scatter plot."""

    x_values = np.asarray(x, dtype=float)
    y_values = np.asarray(y, dtype=float)
    if x_values.shape != y_values.shape:
        raise ValueError("x and y must have the same shape")
    highlight_set = set(highlight)

    for idx, (x_i, y_i) in enumerate(zip(x_values, y_values)):
        is_highlight = idx in highlight_set
        ax.scatter(
            [x_i],
            [y_i],
            s=38 if is_highlight else 24,
            color=PALETTE["method"] if is_highlight else PALETTE["baseline_light"],
            edgecolor=PALETTE["ink"],
            linewidth=0.5,
            zorder=4 if is_highlight else 3,
        )
        if labels:
            ax.annotate(labels[idx], (x_i, y_i), xytext=(3, 3), textcoords="offset points", fontsize=6.5)

    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    clean_axis(ax, grid="both")
    return ax


def label_panel(ax, label: str, *, x: float = -0.12, y: float = 1.05) -> None:
    """Add a bold panel label such as A, B, or C."""

    ax.text(x, y, label, transform=ax.transAxes, fontweight="bold", va="bottom", ha="left")


def save_figure(
    fig,
    out_base: str | Path,
    *,
    formats: Sequence[str] = ("pdf", "svg", "png"),
    dpi: int = 300,
    pad_inches: float = 0.03,
) -> list[Path]:
    """Save a figure to multiple formats and return created paths."""

    base = Path(out_base)
    if base.suffix:
        base = base.with_suffix("")
    base.parent.mkdir(parents=True, exist_ok=True)

    saved: list[Path] = []
    for fmt in formats:
        path = base.with_suffix("." + fmt.lstrip("."))
        fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=pad_inches)
        saved.append(path)
    return saved
