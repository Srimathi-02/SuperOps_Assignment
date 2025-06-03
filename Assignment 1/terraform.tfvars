# GCP Project Configuration
project_id = "vernal-signal-461417-t8"
region     = "us-central1"
zone       = "us-central1-a"

# Network Configuration
network_name  = "lb-network"
subnet_name   = "lb-subnet"
subnet_cidr   = "10.0.1.0/24"

# Compute Configuration
machine_type     = "e2-micro"
instance_image   = "ubuntu-os-cloud/ubuntu-2004-lts"
disk_size        = 10
instance_count   = 2

# Load Balancer Configuration
health_check_path = "/"
health_check_port = 80

# Security Configuration
allowed_source_ranges = ["0.0.0.0/0"]
network_tags         = ["web-server"]
