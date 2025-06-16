#!/usr/bin/env python3
import os
import sys
import logging
import subprocess
import requests
import random
import yaml
import argparse
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nanda_sdk')



class NandaSdk:
    def __init__(self, 
                 domain: str,
                 num_agents: int,
                 registry_url: str = "https://chat.nanda-registry.com",
                 agent_id: Optional[int] = None):
        """
        Initialize NANDA SDK
        
        Args:
            domain: Complete domain name provided by user (e.g., 'myapp.example.com')
            num_agents: Number of agents to set up
            registry_url: URL of the NANDA registry (default: https://chat.nanda-registry.com)
            agent_id: Agent ID number (if None, a random 6-digit number will be generated)
        """
        self.domain = domain
        self.agent_id = agent_id if agent_id is not None else self._generate_agent_id()
        self.num_agents = num_agents
        self.registry_url = registry_url
        logger.info(f"Using agent ID: {self.agent_id}")
        logger.info(f"Using domain: {self.domain}")
        logger.info(f"Using num_agents: {self.num_agents}")
        logger.info(f"Using registry URL: {self.registry_url}")

    def _generate_agent_id(self) -> int:
        """Generate a random 6-digit agent ID"""
        return random.randint(100000, 999999)

    def get_public_ip(self) -> str:
        """Get the server's public IP address"""
        try:
            # Try multiple IP detection services in case one fails
            ip_services = [
                "https://api.ipify.org",
                "https://ifconfig.me/ip",
                "https://icanhazip.com"
            ]
            
            for service in ip_services:
                try:
                    response = requests.get(service, timeout=5)
                    if response.status_code == 200:
                        ip = response.text.strip()
                        logger.info(f"Successfully detected public IP: {ip}")
                        return ip
                except Exception as e:
                    logger.warning(f"Failed to get IP from {service}: {str(e)}")
                    continue
            
            raise Exception("Failed to detect public IP from any service")
        except Exception as e:
            logger.error(f"Failed to get public IP: {str(e)}")
            raise

    def create_ansible_inventory(self) -> str:
        """Create Ansible inventory file"""
        # Get server's public IP
        server_ip = self.get_public_ip()
        
        inventory_content = f"""[servers]
server ansible_host={server_ip}

[all:vars]
ansible_user=root
ansible_connection=local
ansible_python_interpreter=/usr/bin/python3
domain_name={self.domain}
agent_id_prefix={self.agent_id}
github_repo=https://github.com/aidecentralized/nanda-agent.git
registry_url={self.registry_url}
"""
        inventory_path = "/tmp/ioa_inventory.ini"
        with open(inventory_path, "w") as f:
            f.write(inventory_content)
        return inventory_path

    def setup_server(self, anthropic_api_key: str, smithery_api_key: str, verbose: bool = False) -> bool:
        """Set up the server using Ansible"""
        inventory_path = None
        group_vars_dir = None
        try:
            # Create Ansible inventory
            inventory_path = self.create_ansible_inventory()
            logger.info(f"Created inventory file at {inventory_path}")
            
            # Create group_vars directory and file
            group_vars_dir = "/tmp/group_vars"
            os.makedirs(group_vars_dir, exist_ok=True)
            logger.info(f"Created group_vars directory at {group_vars_dir}")
            
            # Create group_vars/all.yml
            group_vars_content = {
                'anthropic_api_key': anthropic_api_key,
                'smithery_api_key': smithery_api_key,
                'domain_name': self.domain,
                'agent_id_prefix': self.agent_id,
                'github_repo': 'https://github.com/aidecentralized/nanda-agent.git',
                'num_agents': self.num_agents,
                'registry_url': self.registry_url
            }
            
            with open(f"{group_vars_dir}/all.yml", "w") as f:
                yaml.dump(group_vars_content, f)
            
            # Get the path to the local Ansible playbook
            current_dir = os.path.dirname(os.path.abspath(__file__))
            playbook_path = os.path.join(current_dir, "ansible", "playbook.yml")
            logger.info(f"Using playbook at: {playbook_path}")
            
            # Run Ansible playbook with optional verbose output
            verbose_flag = "-vvv" if verbose else ""
            cmd = f"ansible-playbook -i {inventory_path} {playbook_path} {verbose_flag}"
            logger.info(f"Running command: {cmd}")
            stdout, stderr = self.execute_command(cmd)
            
            if stdout:
                logger.info(f"Ansible playbook output: {stdout}")
            if stderr:
                logger.error(f"Ansible playbook error: {stderr}")
                return False

            # Check if the playbook failed by looking for "failed=1" in the output
            if "failed=1" in stdout:
                logger.error("Ansible playbook failed with errors")
                return False
                
            logger.info("Server setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup server: {str(e)}")
            return False
        finally:
            # Clean up temporary files
            if os.path.exists(inventory_path):
                os.remove(inventory_path)
            if os.path.exists(f"{group_vars_dir}/all.yml"):
                os.remove(f"{group_vars_dir}/all.yml")
            if os.path.exists(group_vars_dir):
                os.rmdir(group_vars_dir)

    def execute_command(self, command: str) -> tuple:
        """Execute a command on the server"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout, result.stderr
        except Exception as e:
            logger.error(f"Failed to execute command: {str(e)}")
            return "", str(e)

    def setup(self, anthropic_api_key: str, smithery_api_key: str, verbose: bool = False) -> bool:
        """Complete setup process"""
        if not self.setup_server(anthropic_api_key, smithery_api_key, verbose):
            return False
            
        logger.info("Setup completed successfully")
        return True

def main():
    parser = argparse.ArgumentParser(description='Setup Internet of Agents server')
    parser.add_argument('--anthropic-key', 
                       required=True,
                       help='Anthropic API key for the agent')
    parser.add_argument('--domain',
                       required=True,
                       help='Complete domain name (e.g., myapp.example.com)')
    parser.add_argument('--smithery-key', 
                       help='OptionalSmithery API key for the MCP connections')
    parser.add_argument('--agent-id',
                       type=int,
                       help='Optional agent ID (if not provided, will generate one)')
    parser.add_argument('--num-agents',
                       type=int,
                       default=1,
                       help='Optional num of agents(if not provided, will default to one)')
    parser.add_argument('--verbose',
                       action='store_true',
                       help='Enable verbose output for Ansible playbook')
    parser.add_argument('--registry-url',
                       default="https://chat.nanda-registry.com",
                       help='URL of the NANDA registry (default: https://chat.nanda-registry.com)')

    args = parser.parse_args()

    if not args.anthropic_key:
        print("Error: Anthropic API key must be provided")
        sys.exit(1)
        
    if not args.domain:
        print("Error: Domain must be provided")
        sys.exit(1)

    if args.smithery_key:
        smithery_key = args.smithery_key
    else:
        #Hardcoding the SMITHERY_API_KEY here as this is not chargable and we dont want users to provide this 
        smithery_key = "b4e92d35-0034-43f0-beff-042466777ada"
        
    setup = NandaSdk(
        domain=args.domain, 
        agent_id=args.agent_id, 
        num_agents=args.num_agents,
        registry_url=args.registry_url
    )
    
    if not setup.setup(args.anthropic_key, smithery_key, verbose=args.verbose):
        print("Setup failed")
        sys.exit(1)
    print("Setup completed successfully")

if __name__ == "__main__":
    main() 