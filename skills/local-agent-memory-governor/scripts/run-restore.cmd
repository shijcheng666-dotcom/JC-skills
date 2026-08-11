@echo off
REM Local Agent Memory Restore - Windows CMD Launcher
REM Usage: run-restore.cmd --backup-dir PATH [--memory-dir PATH] [--dry-run] [--list]
python "%~dp0memory_restore.py" %*
