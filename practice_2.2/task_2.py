import psutil

def cpu_usage():
    return psutil.cpu_percent(interval=1, percpu=False)

def memory_usage():
    ram = psutil.virtual_memory()
    return ram.percent

def disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent

def main():
    cpu = cpu_usage()
    memory = memory_usage()
    disk = disk_usage()

    print(f"Загрузка CPU: {cpu}%")
    print(f"Использование оперативной памяти: {memory}%")
    print(f"Загруженность диска: {disk}%")

if __name__ == "__main__":
    main()