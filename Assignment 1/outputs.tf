# Load Balancer Outputs
output "load_balancer_ip" {
  description = "External IP address of the load balancer"
  value       = google_compute_global_forwarding_rule.web_lb.ip_address
}

output "load_balancer_url" {
  description = "URL to access the load balancer"
  value       = "http://${google_compute_global_forwarding_rule.web_lb.ip_address}"
}

# Web Server Outputs
output "web_server_names" {
  description = "Names of the web server instances"
  value       = google_compute_instance.web_servers[*].name
}

output "web_server_internal_ips" {
  description = "Internal IP addresses of the web servers"
  value       = google_compute_instance.web_servers[*].network_interface.0.network_ip
}

# Network Infrastructure Outputs
output "vpc_network_name" {
  description = "Name of the VPC network"
  value       = google_compute_network.vpc_network.name
}

output "subnet_name" {
  description = "Name of the subnet"
  value       = google_compute_subnetwork.subnet.name
}

output "subnet_cidr" {
  description = "CIDR range of the subnet"
  value       = google_compute_subnetwork.subnet.ip_cidr_range
}

# NAT Gateway Outputs
output "nat_gateway_name" {
  description = "Name of the NAT gateway"
  value       = google_compute_router_nat.nat.name
}

output "nat_gateway_region" {
  description = "Region of the NAT gateway"
  value       = google_compute_router_nat.nat.region
}

output "router_name" {
  description = "Name of the Cloud Router"
  value       = google_compute_router.router.name
}

# Instance Group Output
output "instance_group_name" {
  description = "Name of the instance group"
  value       = google_compute_instance_group.web_servers.name
}

# Health Check Output
output "health_check_name" {
  description = "Name of the health check"
  value       = google_compute_health_check.web_health_check.name
}
