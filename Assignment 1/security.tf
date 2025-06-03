# Create Firewall Rule for HTTP (External Access)
resource "google_compute_firewall" "allow_http" {
  name    = "${var.network_name}-allow-http"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = [tostring(var.health_check_port)]
  }

  source_ranges = var.allowed_source_ranges
  target_tags   = var.network_tags
  direction     = "INGRESS"
  priority      = 1000
}

# Create Firewall Rule for Health Check (Global Load Balancer)
resource "google_compute_firewall" "allow_health_check" {
  name    = "${var.network_name}-allow-health-check"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = [tostring(var.health_check_port)]
  }

  # Google Cloud health check IP ranges
  source_ranges = ["130.211.0.0/22", "35.191.0.0/16"]
  target_tags   = var.network_tags
  direction     = "INGRESS"
  priority      = 1000
}

# Create Firewall Rule for IAP SSH
resource "google_compute_firewall" "allow_iap_ssh" {
  name    = "${var.network_name}-allow-iap-ssh"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  # IAP SSH IP range
  source_ranges = ["35.235.240.0/20"]
  target_tags   = var.network_tags
  direction     = "INGRESS"
  priority      = 1000
}
