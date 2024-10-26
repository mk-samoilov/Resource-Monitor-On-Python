# Performance Monitor

A real-time system performance monitoring tool built with Python and PySide6 (Qt for Python).

## Features

- Real-time graphical display of CPU usage
- Real-time graphical display of GPU usage (currently using CPU data as a placeholder)
- Real-time graphical display of RAM usage
- Sleek, dark-themed interface
- Ability to switch between different metrics using a toolbar

## Requirements

- Python 3.6+
- PySide6
- psutil

The application window will appear, displaying the CPU usage graph by default. Use the toolbar at the top to switch between CPU, GPU, and RAM graphs.

## How it works

- The application uses separate threads to collect system performance data at regular intervals.
- Custom widget classes (CpuGraphWidget, GpuGraphWidget, RamGraphWidget) are used to draw the graphs.
- The main window (MainWindow) sets up the user interface and manages the different graph widgets.
- The graphs update in real-time, providing a visual representation of system resource usage.
