# Custom Prometheus Exporter in Python

This document provides an explanation of a custom Prometheus exporter script written in Python. The script utilizes the psutil library to collect CPU, memory, and disk metrics from the host system and exposes them as Prometheus metrics over HTTP on port 8000.

## Requirements

To run this custom exporter, you need the following prerequisites:

- `Python`: The script is written in Python and requires Python installed on the system.
- `psutil library`: Install the psutil Python library, which allows easy access to system details like CPU, memory, and disk usage.
- `prometheus_client library`: Install the prometheus_client library, which provides a Python client for Prometheus metrics.

You can install the required libraries using the following commands:

```bash
pip install psutil prometheus_client
```

## Script Explanation

The script consists of three functions to collect CPU, memory, and disk metrics respectively, and a main block that creates Prometheus gauges and continuously collects and updates the metrics.

## Functions That Collect Metrics

There are there function collect_cpu_metrics function collects CPU utilization metrics for each core of the system and updates the corresponding Prometheus gauge.

```python
def collect_cpu_metrics(cpu_gauge):
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    for core, percent in enumerate(cpu_percent):
        cpu_gauge.labels(core=str(core)).set(percent)
```

- This function uses psutil.cpu_percent(interval=1, percpu=True) to obtain the CPU utilization percentage. By setting interval=1, the function calculates the average CPU usage over a 1-second interval. The percpu=True argument returns a list of percentages for each CPU core.
- The function iterates through the list using enumerate to retrieve both the core index and the corresponding percentage value.
- For each core, the Prometheus gauge cpu_gauge is updated using set(percent) with a label representing the core number.
- This function is called periodically by the main block to ensure that CPU metrics are collected and updated in Prometheus at regular intervals.


> **_NOTE:_** The other two collecting functions, `collect_memory_metrics` and `collect_disk_metrics`, follow the same pattern, they retrieve memory and disk metrics, respectively, and update the corresponding Prometheus gauges with appropriate labels.

## Main Block

The main part of the script creates Prometheus gauges for CPU, memory, and disk metrics. It then exposes them over HTTP on port 8000 using the `start_http_server` function. The script enters an infinite loop, continuously collecting the metrics and updating the Prometheus gauges at one-second intervals.

```python
if __name__ == "__main__":
    # Create Prometheus gauges for CPU, memory, and disk metrics
    cpu_gauge = Gauge("cpu_percent", "CPU utilization percentage", ["core"])
    memory_gauge = Gauge("memory_usage", "Memory usage", ["type"])
    disk_gauge = Gauge("disk_usage", "Disk usage", ["type"])

    # Expose the metrics on port 8000
    start_http_server(8000)

    while True:
        # Collect metrics and update Prometheus gauges
        collect_cpu_metrics(cpu_gauge)
        collect_memory_metrics(memory_gauge)
        collect_disk_metrics(disk_gauge)
```

## Running the Script

To execute the script, run it in your Python environment. The exporter will start collecting and exposing system metrics at http://localhost:8000/metrics.

Once the exporter is running, you can configure Prometheus to scrape the metrics from this endpoint to collect and visualize the system statistics over time.
