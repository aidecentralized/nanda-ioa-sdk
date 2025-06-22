# NANDA SDK

A Python SDK for setting up Internet of Agents servers. This tool automates the process of configuring user-space agent services with SSL certificates and required software.

## Prerequisites

### Server Requirements:
- Linux server (Ubuntu/Debian recommended)  
- Python 3.6 or higher with venv support
- Git (for cloning repositories)
- Internet connectivity

### Optional System Dependencies:
If you don't have `python3-venv` or `git`, install them once:
```bash
sudo apt update && sudo apt install python3-venv git
```

**Note**: NANDA SDK now runs in **user-space** without requiring root privileges for operation!

## Installation

Pre-requisite commands (run as regular user):

```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
pipx ensurepath

# Restart terminal or reload shell
source ~/.bashrc  # or ~/.zshrc

# Install nanda-sdk
pipx install nanda-sdk
```

## Quick Setup Guide

### 1. Basic Setup
```bash
nanda-sdk --anthropic-key <your_anthropic_api_key> --domain <myapp.example.com> 
```

### 2. Advanced Setup Options
The setup requires two mandatory parameters:
- `--anthropic-key`: Your Anthropic API key
- `--domain`: Your complete domain name (e.g., myapp.example.com)

Optional parameters:
- `--smithery-key`: Your Smithery API key for connecting to MCP servers
- `--agent-id`: A specific agent ID (if not provided, a random 6-digit number will be generated)
- `--num-agents`: Number of agents to set up (defaults to 1 if not specified)
- `--registry-url`: Custom registry URL (defaults to https://chat.nanda-registry.com)

Example commands:
```bash
# Basic setup with random agent ID
nanda-sdk --anthropic-key <your_anthropic_api_key> --domain <myapp.example.com> 

# Setup with specific agent ID and multiple agents
nanda-sdk --anthropic-key <your_anthropic_api_key> --domain <myapp.example.com> --agent-id 123456 --num-agents 3

# Setup with custom smithery key
nanda-sdk --anthropic-key <your_anthropic_api_key> --domain <myapp.example.com> --smithery-key <your_smithery_api_key>
```

### 3. Verify Installation
After setup completes, verify your agent is running:

```bash
# Check user service status
systemctl --user status internet_of_agents

# View logs
journalctl --user -u internet_of_agents -f

# List running processes 
ps aux | grep python | grep agents
```

Your agent will be:
- Running as a user systemd service
- Accessible on ports 8080 (HTTP) and 8443 (HTTPS) 
- Using self-signed SSL certificates
- Located in `~/internet_of_agents/`

## What the Setup Does

The SDK automatically:
1. Generates a random 6-digit agent ID (if not specified)
2. Creates user directories in your home folder:
   - `~/internet_of_agents/` - Main application
   - `~/.local/ssl/` - SSL certificates  
   - `~/.config/systemd/user/` - User service
3. Clones the agent repository
4. Sets up Python virtual environment
5. Generates self-signed SSL certificates
6. Configures user-level systemd service
7. Runs on non-privileged ports (8080/8443)

## Service Management

All commands run as your regular user (no sudo needed):

```bash
# Start the service
systemctl --user start internet_of_agents

# Stop the service  
systemctl --user stop internet_of_agents

# Restart the service
systemctl --user restart internet_of_agents

# Check status
systemctl --user status internet_of_agents

# View logs
journalctl --user -u internet_of_agents -f

# Enable/disable auto-start
systemctl --user enable internet_of_agents
systemctl --user disable internet_of_agents
```

## Port Information

Your agents will run on:
- **HTTP**: Port 8080 (http://yourdomain.com:8080)
- **HTTPS**: Port 8443 (https://yourdomain.com:8443) 

⚠️ **Note**: Self-signed certificates will show browser warnings. This is normal for development setups.

## File Locations

- **Application**: `~/internet_of_agents/`
- **SSL Certificates**: `~/.local/ssl/`
- **Configuration**: `~/.config/internet_of_agents.env`
- **Service**: `~/.config/systemd/user/internet_of_agents.service`
- **Logs**: `journalctl --user -u internet_of_agents`

## Troubleshooting

### Common Issues:

1. **"python3-venv not found"**:
   ```bash
   sudo apt install python3-venv
   ```

2. **"git not found"**:
   ```bash
   sudo apt install git
   ```

3. **Service won't start**:
   ```bash
   systemctl --user status internet_of_agents
   journalctl --user -u internet_of_agents -f
   ```

4. **Port already in use**:
   The setup uses ports 8080/8443. Make sure these aren't used by other services.

## Requirements

- Python 3.6 or higher
- python3-venv package
- Git
- Linux server (tested on Ubuntu)
- Anthropic API key

## Support

For issues or questions, please check the logs first:
```bash
journalctl --user -u internet_of_agents -f
```

## License

MIT License 
