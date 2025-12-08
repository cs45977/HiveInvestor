#!/bin/bash

# A script to start the local development environment for HiveInvestor.
# This script executes the 'scripts/vm_start.sh' script inside the Vagrant VM.

echo "🚀 Starting HiveInvestor local development environment..."

# Ensure the helper script is executable
chmod +x scripts/vm_start.sh

# Execute the helper script inside the VM
# We use 'bash' explicitly to run it.
vagrant ssh -c "bash /vagrant/scripts/vm_start.sh"

echo "🛑 Development environment script finished."
