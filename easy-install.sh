#!/bin/bash
# Face Recognition PWA - Easy Install Script
# Production ready deployment in 5 minutes

PROJECT=${1:-attendance_prod}
DOMAIN=${2:-attendance.yourdomain.com}
EMAIL=${3:-admin@yourdomain.com}

echo "🚀 Installing Face Recognition PWA..."
echo "📁 Project: $PROJECT"
echo "🌐 Domain: $DOMAIN"
echo "📧 Email: $EMAIL"
echo "=================================="

# Function to print colored output
print_success() {
    echo -e "\e[32m✅ $1\e[0m"
}

print_info() {
    echo -e "\e[34mℹ️  $1\e[0m"
}

print_error() {
    echo -e "\e[31m❌ $1\e[0m"
}

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    print_info "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    print_success "Docker installed"
else
    print_success "Docker already installed"
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    print_info "Installing Docker Compose..."
    sudo apt-get update
    sudo apt-get install -y docker-compose-plugin
    print_success "Docker Compose installed"
else
    print_success "Docker Compose already installed"
fi

# Create project directory
print_info "Creating project directory..."
mkdir -p ~/$PROJECT
cd ~/$PROJECT

# Clone repository
print_info "Cloning Face Recognition PWA..."
git clone https://github.com/ganeshchavan786/Face-Recognition-Attendance-PWA.git .

# Generate secrets
print_info "Generating secure keys..."
cd backend
if [ ! -f ".env" ]; then
    cp .env.example .env
    
    # Generate keys if script exists
    if [ -f "generate_keys.py" ]; then
        python3 generate_keys.py > keys.txt 2>/dev/null
        
        # Update .env with generated keys (if available)
        if [ -f "keys.txt" ]; then
            SECRET_KEY=$(grep "SECRET_KEY" keys.txt | cut -d'"' -f2)
            ENCRYPTION_KEY=$(grep "ENCRYPTION_KEY" keys.txt | cut -d'"' -f2)
            
            if [ ! -z "$SECRET_KEY" ]; then
                sed -i "s/your-secret-key-here/$SECRET_KEY/g" .env
            fi
            if [ ! -z "$ENCRYPTION_KEY" ]; then
                sed -i "s/your-encryption-key-here/$ENCRYPTION_KEY/g" .env
            fi
        fi
    fi
    
    # Update CORS origins
    sed -i "s|http://localhost:5173|http://$DOMAIN|g" .env
    sed -i "s|http://localhost:3000|http://$DOMAIN|g" .env
fi

cd ..

# Deploy with docker-compose
print_info "Starting services with Docker Compose..."
docker-compose up -d

# Wait for services to start
print_info "Waiting for services to start..."
sleep 10

# Check deployment status
print_info "Checking deployment status..."
if docker-compose ps | grep -q "Up"; then
    print_success "Deployment successful!"
    echo ""
    echo "🌐 Access your Face Recognition PWA:"
    echo "📱 Main App: http://$DOMAIN"
    echo "⚙️  Admin Panel: http://$DOMAIN:3000"
    echo "📚 API Documentation: http://$DOMAIN:8000/docs"
    echo ""
    echo "🔧 Management Commands:"
    echo "📋 View status: cd ~/$PROJECT && docker-compose ps"
    echo "📋 View logs: cd ~/$PROJECT && docker-compose logs -f"
    echo "🔄 Restart: cd ~/$PROJECT && docker-compose restart"
    echo "🛑 Stop: cd ~/$PROJECT && docker-compose down"
    echo ""
    print_success "Installation completed in 5 minutes! 🎉"
else
    print_error "Deployment failed! Check logs with: cd ~/$PROJECT && docker-compose logs"
    exit 1
fi
