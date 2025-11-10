import subprocess
import time
import sys
import os

# config
SCRIPTS = ["extract.py", "visualise.py", "output.py"]

def start_process(script):
    """Start a subprocess for a given script."""
    print(f"Starting {script} ...")
    return subprocess.Popen([sys.executable, script])

def main():
    # ensure scripts exist
    for s in SCRIPTS:
        if not os.path.exists(s):
            print(f"Error: {s} not found in the current directory.")
            return

    # ensure output directory exists
    os.makedirs("out", exist_ok=True)

    # start all scripts
    processes = {s: start_process(s) for s in SCRIPTS}
    print("\nAll modules are running:")
    for s in SCRIPTS:
        print(f" - {s}")
    print("\nPress Ctrl+C to stop all services.\n")

    try:
        while True:
            # check if any process has exited; if so, restart it
            for s, p in list(processes.items()):
                ret = p.poll()
                if ret is not None:
                    print(f"{s} exited with code {ret}. Restarting...")
                    processes[s] = start_process(s)
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nStopping all processes...")
        for p in processes.values():
            p.terminate()
        for p in processes.values():
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()
        print("All processes stopped.")
    except Exception as e:
        print("Unexpected error:", e)
        for p in processes.values():
            p.terminate()

if __name__ == "__main__":
    main()
