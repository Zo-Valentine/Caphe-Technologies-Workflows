# ☕ Caphè Technologies Workflows

**Enterprise Workflow Automation Platform**

Caphè Technologies Workflows is a comprehensive workflow automation ecosystem built on n8n, featuring production-ready templates, a powerful API server, and intuitive frontend interfaces for healthcare staffing and enterprise automation needs.

![Project Banner](./assets/n8n-screenshot.png)

## 🚀 Overview

This repository contains a complete workflow automation solution with:

- **400+ Production-Ready Workflows**: Categorized templates for healthcare, HR, marketing, finance, and more
- **Python API Server**: RESTful API for workflow management and integration
- **React Frontend Applications**: Modern UI for workflow browsing and management
- **Healthcare Focus**: Specialized workflows for staffing, compliance, and patient care
- **AI-Powered Automation**: LangChain integration for intelligent workflow processing

## 📦 Project Structure

```
Caphè-Technologies-Workflows/
├── workflows/              # Workflow templates organized by category
├── frameworks/
│   └── caphe-workflows/   # Python API server
├── caphe-workflows-ui/    # Primary React frontend
├── caphe-workflows-frontend/ # Alternative frontend interface
├── scripts/               # Deployment and integration scripts
└── packages/              # n8n core packages and extensions
```

## 🎯 Key Features

### Workflow Library
- **12 Industry Categories**: Marketing, Healthcare, Finance, HR, IT, and more
- **48+ Subcategories**: Specialized workflow collections
- **Production-Ready**: Tested and documented templates
- **Metadata-Driven**: Rich metadata for search and discovery

### API Server
- **RESTful API**: Full workflow CRUD operations
- **WebSocket Support**: Real-time workflow updates
- **Search & Filter**: Advanced workflow discovery
- **Category Management**: Organized workflow browsing

### Frontend Applications
- **Modern React UI**: Built with Vite for fast performance
- **Responsive Design**: Works on desktop and mobile
- **Workflow Preview**: Visual workflow representation
- **One-Click Import**: Easy workflow installation

## 🏥 Healthcare Workflows

Specialized workflows for healthcare staffing and operations:

- **Staffing & Recruitment**: Job applications, resume parsing, interview scheduling
- **Compliance**: License verification, background checks, credential management
- **Communication**: Patient notifications, candidate follow-ups, automated messaging
- **Operations**: Shift matching, availability tracking, employee referrals

## 🔧 Quick Start

### Prerequisites
- Node.js 18+ (for n8n and frontend)
- Python 3.9+ (for API server)
- Docker (optional, for containerized deployment)

### Running the API Server

```bash
# Navigate to the framework directory
cd frameworks/caphe-workflows

# Install dependencies
pip install -r requirements.txt

# Start the server
python3 run.py
```

The API server will be available at `http://localhost:8000`

### Running the Frontend

```bash
# Navigate to the UI directory
cd caphe-workflows-ui

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Using n8n

```bash
# Using npx
npx n8n

# Or with Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

Access n8n at `http://localhost:5678`

## 📚 Documentation

- **Workflow Library**: See [workflows/README.md](./workflows/README.md)
- **API Documentation**: See [frameworks/caphe-workflows/README.md](./frameworks/caphe-workflows/README.md)
- **Deployment Guide**: See [DEPLOYMENT_SUCCESS_REPORT.md](./DEPLOYMENT_SUCCESS_REPORT.md)
- **n8n Documentation**: [docs.n8n.io](https://docs.n8n.io)

## �️ Development

### Project Scripts

```bash
# Validate workflow metadata
python3 scripts/validate_metadata.py

# Fix metadata issues
python3 scripts/fix_metadata.py

# Deploy integration
python3 scripts/deploy_integration.py

# Generate workflow index
node scripts/generate-index.js
```

### Environment Setup

```bash
# Activate Python virtual environment
source activate_env.sh

# Or manually
source caphe.env/bin/activate
```

## 🏗️ Architecture

### Backend (Python)
- **Flask API**: RESTful endpoints for workflow management
- **WebSocket Server**: Real-time updates and communication
- **File-Based Storage**: JSON workflows with metadata
- **Search Engine**: Fast workflow discovery and filtering

### Frontend (React + TypeScript)
- **Vite**: Fast build tool and dev server
- **React 18**: Modern component architecture
- **TypeScript**: Type-safe development
- **Responsive Design**: Mobile-first approach

### Workflow Platform (n8n)
- **Node-Based Editor**: Visual workflow creation
- **400+ Integrations**: Connect to any service
- **AI Capabilities**: LangChain integration
- **Self-Hosted**: Full data control

## 📊 Workflow Categories

| Category | Workflows | Description |
|----------|-----------|-------------|
| Healthcare | 15+ | Staffing, compliance, patient care |
| Human Resources | 10+ | Recruitment, onboarding, management |
| Marketing & Sales | 12+ | Campaigns, lead generation, CRM |
| Finance & Accounting | 8+ | Invoicing, payments, reporting |
| Customer Service | 10+ | Support, ticketing, communication |
| IT & Development | 12+ | DevOps, monitoring, deployment |
| Data Analytics | 8+ | Collection, reporting, BI |
| Content & Media | 6+ | Publishing, processing, management |
| E-commerce | 8+ | Orders, inventory, fulfillment |
| Operations | 10+ | Logistics, supply chain, inventory |
| Education | 6+ | Enrollment, grading, communication |
| General Utilities | 15+ | Tools, scheduling, notifications |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](./CONTRIBUTING.md) for details.

## 📝 License

This project builds upon n8n, which is [fair-code](https://faircode.io) distributed under the [Sustainable Use License](./LICENSE.md).

Caphè Technologies Workflows additions and customizations are proprietary to Caphè Technologies.

## 🔗 Resources

- **Caphè Technologies**: [Coming Soon]
- **n8n Platform**: [n8n.io](https://n8n.io)
- **Documentation**: [docs.n8n.io](https://docs.n8n.io)
- **Community**: [community.n8n.io](https://community.n8n.io)

## 📧 Support

For support and inquiries:
- **GitHub Issues**: [Report bugs or request features](https://github.com/Zo-Valentine/Caph-Technologies-Workflows/issues)
- **Email**: Contact Caphè Technologies for enterprise support

## 🌟 Acknowledgments

Built on the powerful [n8n](https://n8n.io) workflow automation platform. Special thanks to the n8n community for their excellent foundation.

---

**Last Updated**: November 22, 2025  
**Version**: 1.0.0  
**Repository**: [Caphè-Technologies-Workflows](https://github.com/Zo-Valentine/Caph-Technologies-Workflows)
