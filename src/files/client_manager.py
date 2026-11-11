import platform
import socket
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

        
        game = subprocess.Popen(cmd, cwd=self.client_dir, stdout=open(self.log_dir / "client.log", "w"), stderr=subprocess.STDOUT)

    def _verify_clients(self, ports):
        for port in ports:
            timeout = time.time() + 10
            while time.time() < timeout:
                try:
                    with socket.create_connection((self.host, port), timeout=1):
                        break
                except OSError:
                    time.sleep(0.5)
            else:
                raise TimeoutError(f"Port {port} never opened")