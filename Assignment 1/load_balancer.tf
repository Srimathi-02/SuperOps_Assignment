# Create Health Check
resource "google_compute_health_check" "web_health_check" {
  name = "${var.network_name}-web-health-check"

  http_health_check {
    port         = var.health_check_port
    request_path = var.health_check_path
  }

  check_interval_sec  = 10
  timeout_sec         = 5
  healthy_threshold   = 2
  unhealthy_threshold = 3
}

# Create Backend Service
resource "google_compute_backend_service" "web_backend" {
  name        = "${var.network_name}-web-backend"
  protocol    = "HTTP"
  port_name   = "http"
  timeout_sec = 10

  backend {
    group = google_compute_instance_group.web_servers.id
  }

  health_checks = [google_compute_health_check.web_health_check.id]
}

# Create URL Map
resource "google_compute_url_map" "web_url_map" {
  name            = "${var.network_name}-web-url-map"
  default_service = google_compute_backend_service.web_backend.id
}

# Create HTTP Proxy
resource "google_compute_target_http_proxy" "web_proxy" {
  name    = "${var.network_name}-web-proxy"
  url_map = google_compute_url_map.web_url_map.id
}

# Create Global Forwarding Rule (Load Balancer)
resource "google_compute_global_forwarding_rule" "web_lb" {
  name       = "${var.network_name}-load-balancer"
  target     = google_compute_target_http_proxy.web_proxy.id
  port_range = tostring(var.health_check_port)
}
