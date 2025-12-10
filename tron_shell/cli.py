"""
Main CLI interface for Tron Shell.
"""

import sys
import click
from rich.console import Console
from rich.table import Table

from .usb_detector import USBDetector
from .flasher import get_flasher, FlashError
from .bootloader import BootloaderManager
from . import __version__


console = Console()


def print_header():
    """Print the Tron Shell header with company and founder information."""
    console.print("\n")
    console.print("[bold cyan]" + "=" * 70 + "[/bold cyan]")
    console.print("[bold yellow]ROOTCASTLE ENGINEERING INNOVATION[/bold yellow]")
    console.print("[bold white]Tron Shell - Universal Microcontroller Flashing Tool[/bold white]")
    console.print("[bold cyan]Founder: Batuhan AYRIBAS[/bold cyan]")
    console.print("[bold cyan]" + "=" * 70 + "[/bold cyan]\n")


@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Show version and exit")
@click.pass_context
def cli(ctx, version):
    """
    Tron Shell - Next-generation CLI for flashing firmware to microcontrollers.

    A unified interface for flashing firmware to multiple hardware platforms
    with automatic USB detection, bootloader management, and debugging capabilities.
    """
    if version:
        click.echo(f"Tron Shell version {__version__}")
        ctx.exit()

    if ctx.invoked_subcommand is None:
        print_header()
        click.echo(ctx.get_help())


@cli.command()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
def list(verbose):
    """List all connected USB devices."""
    print_header()
    console.print("[bold cyan]Scanning for USB devices...[/bold cyan]\n")

    devices = USBDetector.detect_devices()

    if not devices:
        console.print("[yellow]No USB devices found.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Port", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("VID:PID", style="yellow")
    table.add_column("Description")

    for device in devices:
        device_type = USBDetector.identify_device_type(device)
        vid_pid = device.vid_pid or "N/A"

        table.add_row(device.port, device_type, vid_pid, device.description)

    console.print(table)

    if verbose:
        console.print("\n[bold]Detailed Information:[/bold]\n")
        for device in devices:
            console.print(f"[cyan]{device.port}[/cyan]")
            console.print(f"  Manufacturer: {device.manufacturer or 'N/A'}")
            console.print(f"  Product: {device.product or 'N/A'}")
            console.print(f"  Serial: {device.serial_number or 'N/A'}")
            console.print()


@cli.command()
@click.argument("firmware", type=click.Path(exists=True))
@click.option("-p", "--port", help="Serial port (auto-detected if not specified)")
@click.option("-b", "--board", default="arduino:avr:uno", help="Board type (for Arduino)")
@click.option("--baud", type=int, help="Baud rate for flashing")
@click.option("--platform", help="Platform type (arduino, esp32, stm32, auto)")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.option("--verify/--no-verify", default=True, help="Verify after flashing")
@click.option("--reset/--no-reset", default=True, help="Reset device before flashing")
def flash(firmware, port, board, baud, platform, verbose, verify, reset):
    """
    Flash firmware to a microcontroller.

    FIRMWARE: Path to the firmware file (.hex, .bin, .elf, etc.)

    Examples:

      tron flash firmware.hex

      tron flash firmware.bin --port /dev/ttyUSB0

      tron flash sketch.hex --platform arduino --board arduino:avr:mega

      tron flash app.bin --platform esp32 --baud 460800
    """
    try:
        print_header()
        # Auto-detect port if not specified
        if not port:
            console.print("[cyan]Auto-detecting device...[/cyan]")
            device = USBDetector.auto_detect_target()

            if not device:
                console.print("[red]Error: No devices found. Please specify --port[/red]")
                sys.exit(1)

            port = device.port
            console.print(f"[green]Found device on {port}[/green]")

            # Auto-detect platform if not specified
            if not platform:
                platform = USBDetector.identify_device_type(device)
                if platform != "Unknown":
                    console.print(f"[green]Detected platform: {platform}[/green]")

        # Default platform
        if not platform:
            platform = "auto"

        # Reset device if requested
        if reset:
            console.print("[cyan]Resetting device to enter bootloader...[/cyan]")
            BootloaderManager.enter_bootloader(port, platform)

        # Get appropriate flasher
        flasher = get_flasher(platform, port, verbose)

        # Prepare flash options
        flash_options = {}
        if board:
            flash_options["board"] = board
        if baud:
            flash_options["baud"] = baud

        # Flash firmware
        console.print(f"\n[bold cyan]Flashing {firmware} to {port}...[/bold cyan]\n")

        success = flasher.flash(firmware, **flash_options)

        if not success:
            console.print("[red]Flash failed![/red]")
            sys.exit(1)

        console.print("[green]✓ Flash completed successfully![/green]")

        # Verify if requested
        if verify:
            console.print("[cyan]Verifying firmware...[/cyan]")
            if flasher.verify(firmware):
                console.print("[green]✓ Verification successful![/green]")
            else:
                console.print("[yellow]Warning: Verification failed[/yellow]")

        console.print("\n[bold green]Done![/bold green]")

    except FlashError as e:
        console.print(f"[red]Flash Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument("port")
@click.option(
    "--method", type=click.Choice(["dtr", "rts", "1200baud"]), default="dtr", help="Reset method"
)
def reset(port, method):
    """
    Reset a device to enter bootloader mode.

    PORT: Serial port of the device

    Examples:

      tron reset /dev/ttyUSB0

      tron reset COM3 --method 1200baud
    """
    print_header()
    console.print(f"[cyan]Resetting device on {port} using {method} method...[/cyan]")

    success = BootloaderManager.reset_device(port, method)

    if success:
        console.print("[green]✓ Reset successful![/green]")
    else:
        console.print("[red]Reset failed![/red]")
        sys.exit(1)


@cli.command()
@click.argument("port")
@click.option("-v", "--verbose", is_flag=True, help="Show detailed information")
def info(port, verbose):
    """
    Show detailed information about a device.

    PORT: Serial port of the device

    Examples:

      tron info /dev/ttyUSB0

      tron info COM3 --verbose
    """
    print_header()
    device = USBDetector.find_device_by_port(port)

    if not device:
        console.print(f"[red]Device not found on port {port}[/red]")
        sys.exit(1)

    device_type = USBDetector.identify_device_type(device)

    console.print(f"\n[bold cyan]Device Information: {port}[/bold cyan]\n")

    table = Table(show_header=False, box=None)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Port", device.port)
    table.add_row("Type", device_type)
    table.add_row("VID:PID", device.vid_pid or "N/A")
    table.add_row("Manufacturer", device.manufacturer or "N/A")
    table.add_row("Product", device.product or "N/A")
    table.add_row("Description", device.description)

    if verbose and device.serial_number:
        table.add_row("Serial Number", device.serial_number)

    console.print(table)
    console.print()


@cli.command()
def platforms():
    """List supported platforms and their details."""
    print_header()
    console.print("\n[bold cyan]Supported Platforms[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Platform", style="cyan")
    table.add_column("Description")
    table.add_column("Common Boards")

    platforms_info = [
        ("Arduino", "Arduino-compatible boards using AVR", "Uno, Mega, Nano, Leonardo"),
        ("ESP32", "Espressif ESP32/ESP8266 boards", "ESP32-DevKit, NodeMCU, ESP-WROOM"),
        ("STM32", "STMicroelectronics ARM Cortex-M", "Blue Pill, Nucleo, Discovery"),
        ("Generic", "Other microcontrollers", "Custom boards, various MCUs"),
    ]

    for platform, desc, boards in platforms_info:
        table.add_row(platform, desc, boards)

    console.print(table)
    console.print()


def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
