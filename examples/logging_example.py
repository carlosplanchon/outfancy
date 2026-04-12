#!/usr/bin/env python3
"""
Example demonstrating the logging system in outfancy.
"""

import logging
import outfancy.table
from outfancy.example_dataset import dataset

def example_default_logging():
    """Example 1: Default logging (WARNING level)"""
    print("=" * 60)
    print("Example 1: Default Logging (WARNING only)")
    print("=" * 60)

    table = outfancy.table.Table()
    result = table.render(dataset[:3])
    print("\nTable rendered. Only warnings/errors shown above.\n")


def example_debug_logging():
    """Example 2: Enable DEBUG logging"""
    print("=" * 60)
    print("Example 2: DEBUG Logging Enabled")
    print("=" * 60)

    # Enable DEBUG logging
    logging.getLogger('outfancy').setLevel(logging.DEBUG)

    table = outfancy.table.Table()
    print("\nRendering with DEBUG enabled (watch for debug messages):\n")
    result = table.render(dataset[:2])
    print("\nYou can see all the internal operations above.\n")

    # Reset to WARNING
    logging.getLogger('outfancy').setLevel(logging.WARNING)


def example_custom_format():
    """Example 3: Custom log format"""
    print("=" * 60)
    print("Example 3: Custom Log Format")
    print("=" * 60)

    logger = logging.getLogger('outfancy')
    logger.setLevel(logging.INFO)

    # Remove default handler
    logger.handlers.clear()

    # Add custom handler with simple format
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(levelname)s] %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    print("\nUsing simple format [LEVEL] message:\n")

    large = outfancy.table.LargeTable()
    result = large.render(dataset[:3])

    print("\nCustom format applied to logs above.\n")


def example_show_methods():
    """Example 4: show_* methods return values"""
    print("=" * 60)
    print("Example 4: show_* Methods Return Values")
    print("=" * 60)

    # Enable DEBUG to see the log messages
    logging.getLogger('outfancy').setLevel(logging.DEBUG)

    table = outfancy.table.Table()

    # These methods now return values instead of printing
    print("\nCalling show methods (they return values now):")
    check_data = table.show_check_data()
    corrector = table.show_corrector()
    max_rows = table.show_maximum_number_of_rows()

    print(f"\nReturned values:")
    print(f"  check_data: {check_data}")
    print(f"  corrector: {corrector}")
    print(f"  max_rows: {max_rows}")
    print()

    # Reset
    logging.getLogger('outfancy').setLevel(logging.WARNING)


def example_file_logging():
    """Example 5: Log to file"""
    print("=" * 60)
    print("Example 5: Logging to File")
    print("=" * 60)

    logger = logging.getLogger('outfancy')
    logger.setLevel(logging.DEBUG)

    # Add file handler
    file_handler = logging.FileHandler('outfancy_debug.log')
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(file_handler)

    print("\nRendering table (logs will be written to outfancy_debug.log)...")

    table = outfancy.table.Table()
    result = table.render(dataset[:2])

    print("Done! Check 'outfancy_debug.log' for detailed logs.\n")

    # Cleanup
    logger.removeHandler(file_handler)
    file_handler.close()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("OUTFANCY LOGGING EXAMPLES")
    print("=" * 60 + "\n")

    example_default_logging()
    input("Press ENTER to continue to next example...")

    example_debug_logging()
    input("Press ENTER to continue to next example...")

    example_custom_format()
    input("Press ENTER to continue to next example...")

    example_show_methods()
    input("Press ENTER to continue to next example...")

    example_file_logging()

    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
