#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Starting distributed systems..."
docker compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 10  # Wait for minimum initialization

echo "🧪 Running unit tests..."

# Check test dependencies without trying to install via apt
# This avoids permission issues
check_dependencies() {
  if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python before running."
    exit 1
  fi
  
  # Check if requests module is installed using Python
  if ! python3 -c "import requests" &> /dev/null; then
    echo "⚠️ Python module 'requests' not found."
    echo "⚠️ To install manually: pip install requests"
    echo "⚠️ Running tests without automatic module installation."
  fi
}

# Check dependencies
check_dependencies

# Run unit tests
python3 -m unitary_tests.tests

# If tests pass (exit code 0), continue with initialization
if [ $? -eq 0 ]; then
    echo
    echo "✅ Tests completed successfully! System ready for use."
    echo
    echo "🌐 Nginx LB → http://localhost/"
    echo "🐇 RabbitMQ UI → http://localhost:25673 (admin/admin)"
    echo "🐓 Cockroach UI → http://localhost:8080"
    echo "📘 Swagger → http://localhost/docs"
    echo "📊 Prometheus → http://localhost:9091"
    echo "📈 Grafana → http://localhost:3000 (admin/admin)"
    echo "🔍 Health API → http://localhost/health"
    echo
    echo "System started and running! 🚀"
else
    echo "❌ Unit tests failed! Check logs for more details."
    echo "ℹ️ The system is running but may not be functioning correctly."
fi
