from __future__ import annotations

import json
import sys
from typing import Optional

import typer

import outfancy.table
from outfancy.chart import LineChart

app = typer.Typer(help="Render tables and charts in the terminal.")


def _read_input(file: Optional[str]) -> str:
    if file:
        with open(file) as f:
            return f.read()
    return sys.stdin.read()


def _parse_csv(text: str, delimiter: str = ",", has_headers: bool = False) -> tuple[list[str] | None, list[tuple]]:
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return None, []
    if has_headers:
        headers = [h.strip() for h in lines[0].split(delimiter)]
        rows = [tuple(l.split(delimiter)) for l in lines[1:]]
        return headers, rows
    rows = [tuple(l.split(delimiter)) for l in lines]
    return None, rows


def _parse_json(text: str) -> tuple[list[str] | None, list[tuple]]:
    data = json.loads(text)
    if not data:
        return None, []
    if isinstance(data[0], dict):
        labels = list(data[0].keys())
        rows = [tuple(str(v) for v in row.values()) for row in data]
        return labels, rows
    rows = [tuple(str(v) for v in row) for row in data]
    return None, rows


@app.command()
def table(
    file: Optional[str] = typer.Argument(None, help="Input file (default: stdin)"),
    separator: Optional[str] = typer.Option(None, "--separator", "-s", help="Column separator in output"),
    labels: Optional[str] = typer.Option(None, "--labels", "-l", help="Comma-separated column headers"),
    no_labels: bool = typer.Option(False, "--no-labels", help="Hide column headers"),
    order: Optional[str] = typer.Option(None, "--order", "-o", help="Column indices to show, e.g. 0,2,1"),
    width_equal: bool = typer.Option(False, "--width-equal", help="Assign equal width to all columns"),
    tsv: bool = typer.Option(False, "--tsv", help="Parse input as TSV"),
    json_input: bool = typer.Option(False, "--json", help="Parse input as JSON"),
    has_headers: bool = typer.Option(False, "--has-headers", help="Treat first row as column headers (CSV/TSV only)"),
):
    """Render tabular data as a formatted table."""
    text = _read_input(file)

    if json_input:
        detected_labels, rows = _parse_json(text)
    elif tsv:
        detected_labels, rows = _parse_csv(text, delimiter="\t", has_headers=has_headers)
    else:
        detected_labels, rows = _parse_csv(text, delimiter=",", has_headers=has_headers)

    if not rows:
        typer.echo("No data to render.", err=True)
        raise typer.Exit(1)

    label_list: list[str] | bool | None
    if no_labels:
        label_list = False
    elif labels:
        label_list = [l.strip() for l in labels.split(",")]
    elif detected_labels:
        label_list = detected_labels
    else:
        label_list = None

    order_list = [int(i) for i in order.split(",")] if order else None
    width = False if width_equal else None

    t = outfancy.table.Table()
    typer.echo(t.render(
        data=rows,
        separator=separator,
        label_list=label_list,
        order=order_list,
        width=width,
    ))


@app.command()
def chart(
    file: Optional[str] = typer.Argument(None, help="Input file with x,y pairs (default: stdin)"),
    name: str = typer.Option("", "--name", "-n", help="Chart title"),
    color: bool = typer.Option(False, "--color", "-c", help="Enable ANSI colors"),
    no_interpolation: bool = typer.Option(False, "--no-interpolation", help="Disable interpolation"),
):
    """Render x,y data as a line chart."""
    text = _read_input(file)
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        typer.echo("No data to render.", err=True)
        raise typer.Exit(1)

    dataset = []
    for line in lines:
        parts = line.split(",")
        if len(parts) < 2:
            continue
        try:
            dataset.append((float(parts[0].strip()), float(parts[1].strip())))
        except ValueError:
            continue

    if not dataset:
        typer.echo("No valid x,y pairs found.", err=True)
        raise typer.Exit(1)

    c = LineChart()
    c.plot(dataset)
    typer.echo(c.render(
        plot_name=name,
        color=color,
        interpolation=not no_interpolation,
    ))


def main():
    app()
