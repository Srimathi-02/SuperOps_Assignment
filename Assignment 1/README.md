# GCP Load Balancer Infrastructure

This Terraform configuration creates a complete load-balanced web application infrastructure on Google Cloud Platform (GCP).

## Architecture

The infrastructure includes:
- VPC Network with custom subnet
- Cloud NAT for outbound internet access
- Two web server instances running nginx
- Global HTTP Load Balancer
- Health checks and firewall rules
- Instance Access Protocol (IAP) for SSH access

## File Structure

```
.
├── main.tf                    # Provider configuration and core networking
├── variables.tf               # Variable definitions
├── compute.tf                 # Compute instances and instance groups
├── security.tf                # Firewall rules
├── load_balancer.tf           # Load balancer configuration
├── outputs.tf                 # Output definitions
├── terraform.tfvars           # Variable values (your configuration)
├── terraform.tfvars.example   # Example variable values
├── scripts/
│   └── startup.sh            # Instance startup script
└── README.md                 # This file
```

## Prerequisites

1. [Terraform](https://www.terraform.io/downloads.html) installed (>= 1.0)
2. [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and configured
3. A GCP project with billing enabled
4. Required APIs enabled:
   - Compute Engine API
   - Cloud Resource Manager API

## Quick Start

1. **Clone or download the configuration files**

2. **Enable required APIs:**
   ```bash
   gcloud services enable compute.googleapis.com
   gcloud services enable cloudresourcemanager.googleapis.com
   ```

3. **Authenticate with GCP:**
   ```bash
   gcloud auth application-default login
   ```

4. **Configure variables:**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your project ID
   ```

5. **Initialize and apply:**
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

6. **Access the application:**
   - The load balancer IP will be displayed in the output
   - Visit `http://<load_balancer_ip>` to see the application

## Configuration

### Required Variables

- `project_id`: Your GCP Project ID

### Optional Variables

All other variables have sensible defaults but can be customized:

- `region`: GCP region (default: us-central1)
- `zone`: GCP zone (default: us-central1-a)
- `network_name`: VPC network name (default: lb-network)
- `subnet_cidr`: Subnet CIDR range (default: 10.0.1.0/24)
- `machine_type`: Instance type (default: e2-micro)
- `instance_count`: Number of web servers (default: 2)
- `health_check_port`: Port for health checks (default: 80)

## Security Features

- **No External IPs**: Instances use Cloud NAT for outbound access
- **Firewall Rules**: Restricted access with proper source ranges
- **IAP SSH**: Secure SSH access through Identity-Aware Proxy
- **Health Check Access**: Dedicated firewall rules for load balancer health checks

## Monitoring and Debugging

- Instance logs are available in `/var/log/startup-script.log`
- Use Cloud Console to monitor instance health
- SSH access via IAP: `gcloud compute ssh INSTANCE_NAME --zone=ZONE --tunnel-through-iap`

## Cleanup

To destroy the infrastructure:

```bash
terraform destroy
```
