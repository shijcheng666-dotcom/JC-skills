@echo off
REM Local Agent Memory Audit - Windows CMD Launcher
REM Usage: run-audit.cmd [--memory-dir PATH] [--output PATH]
python "%~dp0memory_audit.py" %*
