import subprocess
import os
import signal
import sys
import time


def run_backend():
    return subprocess.Popen(
        ["uvicorn", "dream100_api.main:app", "--reload"], preexec_fn=os.setsid
    )


def run_frontend():
    frontend_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dream100/frontend"
    )
    return subprocess.Popen(
        ["npm", "run", "dev"], cwd=frontend_dir, preexec_fn=os.setsid
    )


def terminate_process_group(process):
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except ProcessLookupError:
        pass  # Process has already terminated


def main():
    backend_process = run_backend()
    frontend_process = run_frontend()

    def signal_handler(sig, frame):
        print("\nShutting down...")
        terminate_process_group(backend_process)
        terminate_process_group(frontend_process)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        signal_handler(None, None)


if __name__ == "__main__":
    main()
