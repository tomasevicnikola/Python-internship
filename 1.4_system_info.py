import argparse
import os
import subprocess


def get_distro():
    try:
        result = subprocess.run(
            ["grep", "PRETTY_NAME", "/etc/os-release"],
            capture_output=True,
            text=True,
            check=True
        )
        distro = result.stdout.split("=")[1].strip().replace('"', "")
        print("Distro Information:")
        print(distro)
    except Exception:
        print("Distro info not available")


def get_memory():
    try:
        result = subprocess.run(
            ["free", "-m"],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.splitlines()
        memory_line = lines[1].split()

        total = memory_line[1]
        used = memory_line[2]
        free = memory_line[3]

        print("Memory Information:")
        print(f"Total: {total} MB")
        print(f"Used: {used} MB")
        print(f"Free: {free} MB")
    except Exception:
        print("Memory info not available")


def get_cpu():
    try:
        model_result = subprocess.run(
            ["grep", "model name", "/proc/cpuinfo"],
            capture_output=True,
            text=True,
            check=True
        )
        speed_result = subprocess.run(
            ["grep", "cpu MHz", "/proc/cpuinfo"],
            capture_output=True,
            text=True,
            check=True
        )

        model = model_result.stdout.splitlines()[0].split(":")[1].strip()
        speed = speed_result.stdout.splitlines()[0].split(":")[1].strip()
        cores = os.cpu_count()

        print("CPU Information:")
        print(f"Model: {model}")
        print(f"Core numbers: {cores}")
        print(f"Speed: {speed} MHz")
    except Exception:
        print("CPU info not available")


def get_user():
    try:
        result = subprocess.run(
            ["whoami"],
            capture_output=True,
            text=True,
            check=True
        )

        print("Current User:")
        print(result.stdout.strip())
    except Exception:
        print("User info not available")


def get_load():
    try:
        result = subprocess.run(
            ["uptime"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()

        if "load average:" in output:
            load = output.split("load average:")[1].strip()
        else:
            load = "Load average not available"

        print("System Load Average:")
        print(load)
    except Exception:
        print("Load average not available")


def get_ip():
    try:
        result = subprocess.run(
            ["hostname", "-I"],
            capture_output=True,
            text=True,
            check=True
        )
        ip = result.stdout.strip().split()[0]

        print("IP Address:")
        print(ip)
    except Exception:
        print("IP address not available")


def main():
    parser = argparse.ArgumentParser(description="Script for showing system information")
    parser.add_argument("-d", action="store_true", help="Show distro info")
    parser.add_argument("-m", action="store_true", help="Show memory info (total, used, free)")
    parser.add_argument("-c", action="store_true", help="Show CPU info (model, core numbers, speed)")
    parser.add_argument("-u", action="store_true", help="Show current user")
    parser.add_argument("-l", action="store_true", help="Show system load average")
    parser.add_argument("-i", action="store_true", help="Show IP address")

    args = parser.parse_args()

    if not (args.d or args.m or args.c or args.u or args.l or args.i):
        parser.print_help()
        return

    if args.d:
        get_distro()
        print()

    if args.m:
        get_memory()
        print()

    if args.c:
        get_cpu()
        print()

    if args.u:
        get_user()
        print()

    if args.l:
        get_load()
        print()

    if args.i:
        get_ip()
        print()


if __name__ == "__main__":
    main()