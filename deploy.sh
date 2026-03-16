#!/bin/bash
# Deployment script for Social Mimic Agent to EC2

set -e

EC2_IP="54.227.176.142"
EC2_USER="ec2-user"
KEY_PATH="$HOME/.ssh/arxiv-assistant-key.pem"
APP_DIR="social_mimic_agent"

echo "=== Deploying Social Mimic Agent to EC2 ==="

# Create EC2 setup script
cat > /tmp/ec2_setup_social.sh << 'SETUP_EOF'
#!/bin/bash
set -e

echo "=== Setting up Social Mimic Agent ==="

cd ~/$APP_DIR

# Install Python dependencies
pip3 install --user -r requirements.txt

echo ""
echo "=== Setup complete ==="
echo "To run the app:"
echo "  cd ~/$APP_DIR && python3 main.py"
SETUP_EOF

# Replace APP_DIR variable in setup script
sed -i.bak "s/\$APP_DIR/$APP_DIR/g" /tmp/ec2_setup_social.sh

echo "Creating app directory on EC2..."
ssh -i $KEY_PATH -o StrictHostKeyChecking=no $EC2_USER@$EC2_IP "mkdir -p ~/$APP_DIR"

echo "Copying files to EC2..."
# Copy all project files (excluding venv, __pycache__, .git)
rsync -avz -e "ssh -i $KEY_PATH -o StrictHostKeyChecking=no" \
    --exclude 'venv' \
    --exclude '__pycache__' \
    --exclude '.git' \
    --exclude '*.pyc' \
    --exclude '.env' \
    --exclude 'logs' \
    ./ $EC2_USER@$EC2_IP:~/$APP_DIR/

# Copy setup script
scp -i $KEY_PATH /tmp/ec2_setup_social.sh $EC2_USER@$EC2_IP:/tmp/

# Run setup script on EC2
echo "Running setup on EC2..."
ssh -i $KEY_PATH $EC2_USER@$EC2_IP "chmod +x /tmp/ec2_setup_social.sh && /tmp/ec2_setup_social.sh"

echo ""
echo "=== Deployment complete! ==="
echo ""
echo "To run the app, SSH into EC2 and set environment variables:"
echo ""
echo "  ssh -i $KEY_PATH $EC2_USER@$EC2_IP"
echo ""
echo "  # Set API keys (required)"
echo "  export GEMINI_API_KEY=your-gemini-key"
echo "  export OPENAI_API_KEY=your-openai-key"
echo ""
echo "  # Run the app"
echo "  cd ~/$APP_DIR && python3 main.py"
echo ""
