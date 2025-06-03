# Project Configuration Variables
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP Zone"
  type        = string
  default     = "us-central1-a"
}

# Network Configuration Variables
variable "network_name" {
  description = "Name of the VPC network"
  type        = string
  default     = "lb-network"
}

variable "subnet_name" {
  description = "Name of the subnet"
  type        = string
  default     = "lb-subnet"
}

variable "subnet_cidr" {
  description = "CIDR range for the subnet"
  type        = string
  default     = "10.0.1.0/24"
}

# Compute Instance Variables
variable "machine_type" {
  description = "Machine type for web servers"
  type        = string
  default     = "e2-micro"
}

variable "instance_image" {
  description = "OS image for instances"
  type        = string
  default     = "ubuntu-os-cloud/ubuntu-2004-lts"
}

variable "disk_size" {
  description = "Boot disk size in GB"
  type        = number
  default     = 10
}

variable "instance_count" {
  description = "Number of web server instances"
  type        = number
  default     = 2
}

# Load Balancer Variables
variable "health_check_path" {
  description = "Path for health check"
  type        = string
  default     = "/"
}

variable "health_check_port" {
  description = "Port for health check"
  type        = number
  default     = 80
}

# Firewall Variables
variable "allowed_source_ranges" {
  description = "Allowed source IP ranges for HTTP access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# Tags
variable "network_tags" {
  description = "Network tags for instances"
  type        = list(string)
  default     = ["web-server"]
}
