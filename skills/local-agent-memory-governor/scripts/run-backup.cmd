@echo off
REM Local Agent Memory Backup - Windows CMD Launcher
REM Usage: run-backup.cmd [--memory-dir PATH] [--backup-dir PATH]
python "%~dp0memory_backup.py" %*
