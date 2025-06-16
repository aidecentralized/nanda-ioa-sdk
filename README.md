# NANDA SDK

A Python SDK for setting up Internet of Agents servers. This tool automates the process of configuring servers with DNS records, SSL certificates, and required software.

## Installation

Pre-requistie commands 

ssh into the servers

```bash
sudo apt update  && sudo apt install python3 python3-pip

```

```bash
pip install nanda-sdk
```

```bash
nanda-sdk --anthropic-key <your_anthropic_api_key> --domain <myapp.example.com> 
```

## Quick Setup Guide

### 1. Install the SDK
```bash
pip install nanda-sdk
```

### 2. Run the Setup
The setup requires two mandatory parameters:
- `--anthropic-key`: Your Anthropic API key
- `--domain`: Your complete domain name (e.g., myapp.example.com)

Optional parameters:
- `--smithery-key`: Your Smithery API key for connecting to MCP servers. A default key will be provided by application for connectivitiy
- `--agent-id`: A specific agent ID (if not provided, a random 6-digit number will be generated)
- `--num-agents`: Number of agents to set up (defaults to 1 if not specified)
- `--registry-url`: If the registry url needs to be changed. Default to https://chat.nanda-registry.com. We just need to pass 
the domain. Expected port for registry to run in 6900
Example commands:
```bash
# Basic setup with random agent ID
nanda-sdk --anthropic-key <your_anthropic_api_key> --domain <myapp.example.com> 

# Setup with specific agent ID
nanda-sdk --anthropic-key <your_anthropic_api_key> --domain <myapp.example.com> --agent-id 123456

# Setup with multiple agents
nanda-sdk --anthropic-key <your_anthropic_api_key> --domain <myapp.example.com> --num-agents 3

# Setup with your own smithery key
nanda-sdk --anthropic-key <your_anthropic_api_key> --domain <myapp.example.com> --smithery-key <your_smithery_api_key>

# Setup with your own registry
nanda-sdk --anthropic-key <your_anthropic_api_key> --domain <myapp.example.com> --registry-url <https://your-domain.com>
```

### 3. Verify Installation
After setup completes, verify your agent is running:

```bash
# Check service status
systemctl status internet_of_agents

# View logs
journalctl -u internet_of_agents -f

# list of servers 
ps aux | grep run_ui_agent_https
```

Your agent will be:
- Running as a systemd service
- Accessible at your specified domain
- Automatically starting on server reboot

## What the Setup Does

The SDK automatically:
1. Generates a random 6-digit agent ID (if not specified)
2. Gets your server's public IP
3. Creates a DNS record (e.g., chat123456.nanda-registry.com)
4. Installs required packages:
   - Python and pip
   - Git
   - Certbot for SSL
   - Nginx
5. Sets up SSL certificates
6. Clones the repository
7. Sets up Python virtual environment
8. Configures the systemd service

## Troubleshooting

If you encounter any issues:

1. Check the service status:
```bash
systemctl status internet_of_agents
```

2. View detailed logs:
```bash
journalctl -u internet_of_agents -f
```

3. For Route53 DNS issues, contact the IOA support team.

## Requirements

- Python 3.6 or higher
- Linux server (tested on Ubuntu)
- Anthropic API key

## Support

If you encounter any issues with Route53 DNS setup, please contact the IOA support team.

## License

MIT License 