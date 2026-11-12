import os
import sys
import tempfile
from PySide6.QtCore import QObject, QProcess, Signal, QProcessEnvironment


class ScriptRunner(QObject):
    """Asynchronous script execution runner using QProcess."""

    stdout_received = Signal(str)
    stderr_received = Signal(str)
    system_received = Signal(str)
    finished = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.process: QProcess = QProcess(self)
        self.process.readyReadStandardOutput.connect(self._on_stdout)
        self.process.readyReadStandardError.connect(self._on_stderr)
        self.process.finished.connect(self._on_finished)
        self.temp_file_path: str = ""

    def run_script(self, code: str):
        if self.process.state() != QProcess.NotRunning:
            self.process.kill()
            self.process.waitForFinished(1000)

        # Save script code to a temporary JPS file
        with tempfile.NamedTemporaryFile("w", suffix=".jps", delete=False, encoding="utf-8") as temp_f:
            temp_f.write(code)
            self.temp_file_path = temp_f.name

        self.system_received.emit("────────────────────────────────────────────────────────────")
        self.system_received.emit(f"[JPS IDE] Running script...")

        python_exe = sys.executable
        args = ["-m", "jps.runner", self.temp_file_path]

        # Ensure PYTHONPATH includes current working directory
        env = QProcessEnvironment.systemEnvironment()
        current_pythonpath = env.value("PYTHONPATH", "")
        env.insert("PYTHONPATH", os.getcwd() + os.pathsep + current_pythonpath)
        self.process.setProcessEnvironment(env)

        self.process.start(python_exe, args)

    def _on_stdout(self):
        data = self.process.readAllStandardOutput().data().decode("utf-8", errors="replace")
        for line in data.splitlines():
            self.stdout_received.emit(line)

    def _on_stderr(self):
        data = self.process.readAllStandardError().data().decode("utf-8", errors="replace")
        for line in data.splitlines():
            self.stderr_received.emit(line)

    def _on_finished(self, exit_code, exit_status):
        if exit_code == 0:
            self.system_received.emit("[JPS IDE] Program executed successfully.")
        else:
            self.system_received.emit(f"[JPS IDE] Program finished with exit code {exit_code}.")

        # Cleanup temp file
        if self.temp_file_path and os.path.exists(self.temp_file_path):
            try:
                os.remove(self.temp_file_path)
            except Exception:
                pass

        self.finished.emit(exit_code)
