# Make executable
chmod +x bin/tron

# Install dependencies
pip install -r requirements.txt

# Install package
pip install .

# Create default config directory
mkdir -p ~/.tron
cp config/default_rules.yaml ~/.tron/config.yaml

# Test installation
tron detect --verbose