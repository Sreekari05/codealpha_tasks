import csv
import os

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def display_report(report, total_value):
    """
    Display portfolio summary using Rich tables.
    """

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]📈 Stock Portfolio Summary[/bold cyan]",
            border_style="green"
        )
    )

    table = Table(
        show_header=True,
        header_style="bold magenta",
        show_lines=True
    )

    table.add_column("Stock", style="cyan", justify="center")
    table.add_column("Quantity", style="yellow", justify="center")
    table.add_column("Price ($)", style="green", justify="right")
    table.add_column("Investment ($)", style="bold blue", justify="right")

    for item in report:
        table.add_row(
            item["stock"],
            str(item["quantity"]),
            f"${item['price']}",
            f"${item['investment']}"
        )

    console.print(table)

    console.print(
        Panel.fit(
            f"[bold green]Total Investment Value: ${total_value}[/bold green]",
            border_style="blue"
        )
    )


def save_to_csv(report, total_value):
    """
    Save portfolio report to CSV file.
    """

    os.makedirs("data", exist_ok=True)

    file_path = "data/portfolio_report.csv"

    with open(file_path, mode="w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Stock",
                "Quantity",
                "Price",
                "Investment Value"
            ]
        )

        for item in report:
            writer.writerow(
                [
                    item["stock"],
                    item["quantity"],
                    item["price"],
                    item["investment"]
                ]
            )

        writer.writerow([])

        writer.writerow(
            [
                "Total Investment",
                "",
                "",
                total_value
            ]
        )

    console.print(
        f"\n✅ [bold green]CSV Report Saved:[/bold green] {file_path}"
    )


def save_to_txt(report, total_value):
    """
    Save portfolio report to TXT file.
    """

    os.makedirs("data", exist_ok=True)

    file_path = "data/portfolio_report.txt"

    with open(file_path, mode="w") as file:

        file.write("STOCK PORTFOLIO SUMMARY\n")
        file.write("=" * 60 + "\n\n")

        file.write(
            f"{'Stock':<10}"
            f"{'Quantity':<10}"
            f"{'Price($)':<15}"
            f"{'Investment($)':<15}\n"
        )

        file.write("-" * 60 + "\n")

        for item in report:

            file.write(
                f"{item['stock']:<10}"
                f"{item['quantity']:<10}"
                f"{item['price']:<15}"
                f"{item['investment']:<15}\n"
            )

        file.write("-" * 60 + "\n")
        file.write(
            f"Total Investment Value = ${total_value}\n"
        )

    console.print(
        f"✅ [bold green]TXT Report Saved:[/bold green] {file_path}"
    )