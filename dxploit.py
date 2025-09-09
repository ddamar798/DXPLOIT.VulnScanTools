#!/usr/bin/env python3
"""
Entry script for DXPLOIT.VulnScan — safe wrapper that imports package dxploit_vulnscan
Run with: python3 dxploit.py  OR python3 -m dxploit_vulnscan
"""
from dxploit_vulnscan.cli import run_cli

if __name__ == "__main__":
    run_cli()
