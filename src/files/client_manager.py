import platform
import subprocess
import time

from pathlib import Path

class ClientManager():
    def __init__(self, learn, log_dir, host):
        self.client_dir =  Path(__file__).resolve().parent.parent.parent / "FightingICE7.1"
        self.os = platform.system()
        self.learn = learn
        self.log_dir = log_dir
        self.host = host
        self.processes = {}
        self.log_files = {}

    def launch_clients(self, ports):
        for port in ports:    
            self._create_client(port)

        self._verify_clients(ports)

    def _create_client(self, port):
        join_sym = ""
        if self.os == "Windows":
            join_sym = ";"
        else:
            join_sym = ":"         

        classpath = join_sym.join([
            "FightingICE.jar",
            "./lib/*",
            "./lib/lwjgl/*",
            f"./lib/lwjgl/natives/{self.os.lower()}/amd64/*",
            "./lib/grpc/*",
        ])

        cmd = [
            "java", "-cp", classpath, "Main",
            "--limithp", "400", "400",
            "--grey-bg",
            "--pyftg-mode",
            "--port", str(port),
        ]

        if self.learn:
            cmd.append("--headless-mode")
            cmd.append("--input-sync")

        log = open(self._log_path(port), "w")
        self.log_files[port] = log
        self.processes[port] = subprocess.Popen(cmd, cwd=self.client_dir, stdout=log, stderr=subprocess.STDOUT)

    def _verify_clients(self, ports):
        for port in ports:
            log_path = self._log_path(port)
            timeout = time.time() + 10
            while time.time() < timeout:
                polled_val = self.processes[port].poll()
                if polled_val is not None:
                    raise RuntimeError(f"Game client crashed on port {port} with exit code {polled_val}. Check {log_path}")
                if f"listening on {port}" in log_path.read_text(errors="ignore"):
                    break
                time.sleep(0.5)
            else:
                raise TimeoutError(f"Client on {port} never started. Check {log_path}")

    def _log_path(self, port):
        return self.log_dir / f"client_{port}.log"

    def close_clients(self):
        for client in self.processes.values():
            if client.poll() is not None:
                continue

            if self.os == "Windows":
                subprocess.run(["taskkill", "/PID", str(client.pid), "/T", "/F"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                client.wait()

            else:
                client.terminate()
                try:
                    client.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    client.kill()
                    client.wait()

        for log in self.log_files.values():
            log.close()