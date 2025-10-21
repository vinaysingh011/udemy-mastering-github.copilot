# udemy-mastering-github.copilot
repo for udemy course-mastering github copilot for devops

# Uptime script

Print system uptime by reading `/proc/uptime`. Intended for Linux systems (this workspace runs on Ubuntu 24.04).

Usage
- Make executable (optional):
  chmod +x copilot_test.py

- Run with Python:
  python3 copilot_test.py

- Or run directly:
  ./copilot_test.py

Options
- --seconds     Print raw uptime seconds (useful for scripts)
- --path PATH   Read uptime from PATH instead of `/proc/uptime`
- --debug       Enable debug logging to stderr

Examples
- Formatted H:M:S (default):
  python3 copilot_test.py

- Raw seconds:
  python3 copilot_test.py --seconds

- Use alternate uptime file:
  python3 copilot_test.py --path /tmp/fake_uptime

Exit codes
- 0: success
- 2: not running on Linux
- 3: uptime file not found
- 4: permission denied reading uptime file
- 5: invalid uptime file contents
- 10: unexpected error

Notes
- The script expects a Linux-style `/proc/uptime`. When used in scripts, prefer `--seconds` for stable numeric output.
- In this dev container you can run the commands shown above directly.
