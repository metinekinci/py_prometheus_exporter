import psutil
from prometheus_client import start_http_server, Gauge

# Collect CPU metrics
def collect_cpu_metrics(cpu_gauge):
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    for core, percent in enumerate(cpu_percent):
        cpu_gauge.labels(core=str(core)).set(percent)

# Collect memory metrics
def collect_memory_metrics(memory_gauge):
    memory = psutil.virtual_memory()
    memory_gauge.labels("total").set(memory.total)
    memory_gauge.labels("available").set(memory.available)
    memory_gauge.labels("used").set(memory.used)
    memory_gauge.labels("percent").set(memory.percent)

# Collect disk metrics
def collect_disk_metrics(disk_gauge):
    disk = psutil.disk_usage("/")
    disk_gauge.labels("total").set(disk.total)
    disk_gauge.labels("used").set(disk.used)
    disk_gauge.labels("free").set(disk.free)
    disk_gauge.labels("percent").set(disk.percent)

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
