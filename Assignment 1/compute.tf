# Startup script for web servers
locals {
  startup_script = templatefile("${path.module}/scripts/startup.sh", {
    health_check_port = var.health_check_port
  })
}

# Create Web Server Instances
resource "google_compute_instance" "web_servers" {
  count        = var.instance_count
  name         = "web-server-${count.index + 1}"
  machine_type = var.machine_type
  zone         = var.zone

  tags = var.network_tags

  boot_disk {
    initialize_params {
      image = var.instance_image
      size  = var.disk_size
    }
  }

  network_interface {
    network    = google_compute_network.vpc_network.id
    subnetwork = google_compute_subnetwork.subnet.id
    # No external IP - using NAT for internet access
  }

  metadata_startup_script = local.startup_script

  service_account {
    scopes = ["cloud-platform"]
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Create Instance Group
resource "google_compute_instance_group" "web_servers" {
  name = "${var.network_name}-web-servers-group"
  zone = var.zone

  instances = google_compute_instance.web_servers[*].id

  named_port {
    name = "http"
    port = var.health_check_port
  }

  depends_on = [google_compute_instance.web_servers]
}
