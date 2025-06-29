# 💬 QuantumChat – Lightning-Fast AI with GROQ & RAG

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)
![Groq](https://img.shields.io/badge/Groq-API-green.svg)
![RAG](https://img.shields.io/badge/RAG-Powered-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Overview

QuantumChat is a conversational AI application that combines GROQ's fast inference capabilities with Retrieval-Augmented Generation (RAG) technology. Built with Streamlit, it provides a user-friendly interface for chatting with AI models while leveraging external documents for enhanced responses.

### Key Features

- ⚡ **Lightning-Fast Responses**: Powered by GROQ's high-speed inference engine
- 🧠 **RAG Integration**: Upload documents and ask questions based on their content
- 💬 **Session Management**: Multiple chat sessions with persistent history
- 📚 **Multi-Format Support**: PDF, DOCX, TXT, MD, and HTML document processing
- 🎯 **Vector Search**: Qdrant-powered semantic search for relevant context
- 🌐 **Clean UI**: Intuitive Streamlit-based web interface

## 📋 Table of Contents

- [Installation](https://github.com/Vigneshmaradiya/quantumchat-groq-rag/blob/main/README.md#-installation)
- [Configuration](https://github.com/Vigneshmaradiya/quantumchat-groq-rag/edit/main/README.md#%EF%B8%8F-configuration)
- [Usage](https://github.com/Vigneshmaradiya/quantumchat-groq-rag/edit/main/README.md#-usage)
- [Project Structure](https://github.com/Vigneshmaradiya/quantumchat-groq-rag/edit/main/README.md#-project-structure)
- [Supported Models](https://github.com/Vigneshmaradiya/quantumchat-groq-rag/edit/main/README.md#-supported-models)
- [Upcoming Features](#-upcoming-features)
- [Contributing](https://github.com/Vigneshmaradiya/quantumchat-groq-rag/edit/main/README.md#-contributing)
- [License](https://github.com/Vigneshmaradiya/quantumchat-groq-rag/blob/main/LICENSE)

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- Conda package manager
- GROQ API key
- Qdrant Cloud account (for vector database)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Vigneshmaradiya/quantumchat-groq-rag.git
cd quantumchat-groq-rag
```

### Step 2: Create Conda Environment

```bash
# Create a new conda environment
conda create -n quantumchat python=3.10

# Activate the environment
conda activate quantumchat
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### Step 4: Environment Setup

Create a `.env` file in the root directory:

```env
# GROQ API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Qdrant Vector Database Configuration
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_URL=your_qdrant_cluster_url_here
```

### Step 5: Run the Application

```bash
# Activate conda environment
conda activate chatbot-app

# Run Streamlit app with proper path
PYTHONPATH=. streamlit run app/main.py
```

## ⚙️ Configuration

### GROQ API Key Setup

1. Visit [GROQ Console](https://console.groq.com/)
2. Create an account or sign in
3. Navigate to API Keys section
4. Generate a new API key
5. Add the key to your `.env` file

### Qdrant Setup

1. Visit [Qdrant Cloud](https://cloud.qdrant.io/)
2. Create a free account
3. Create a new cluster
4. Get your API key and cluster URL
5. Add them to your `.env` file

## 🎯 Usage

### Running the Application

```bash
# Activate conda environment
conda activate chatbot-app

# Run the Streamlit application
PYTHONPATH=. streamlit run app/main.py
```

### Accessing the Application

Open your web browser and navigate to: `http://localhost:8501`

### Basic Usage

1. **Start Chatting**: Select a model and start asking questions
2. **Upload Documents**: Use the sidebar to upload PDF, DOCX, TXT, MD, or HTML files
3. **Ask About Documents**: Once uploaded, ask questions about the document content
4. **Manage Sessions**: Create new sessions or switch between existing ones
5. **Download History**: Export chat history as JSON files

## 📁 Project Structure

```
quantumchat-groq-rag/
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   ├── llm_router.py          # GROQ API integration
│   ├── main.py                # Streamlit application
│   ├── rag_engine.py          # RAG functionality
│   └── session_memory.py      # Session management
└── utils/
    ├── __init__.py
    └── token_utils.py          # Token counting utilities
```

### Core Components

- **`app/config.py`**: Configuration management for API keys, models, and settings
- **`app/llm_router.py`**: GROQ API client with streaming support
- **`app/main.py`**: Main Streamlit application with UI components
- **`app/rag_engine.py`**: Document processing, embedding, and retrieval logic
- **`app/session_memory.py`**: Chat session persistence and management
- **`utils/token_utils.py`**: Token counting for usage tracking

## 🤖 Supported Models

The application supports multiple GROQ models:

| Model | Description | Max Tokens |
|-------|-------------|------------|
| `llama-3.1-8b-instant` | Fast, efficient model (Default) | 131,072 |
| `llama3-3.3-70b-versatile` | High-quality responses | 32,768 |
| `gemma2-9b-it` | Balanced performance | 8,192 |

## 🔧 Key Features Explained

### RAG (Retrieval-Augmented Generation)

The application uses a sophisticated RAG pipeline:

1. **Document Processing**: Splits uploaded documents into chunks
2. **Embedding Generation**: Uses HuggingFace embeddings (`all-MiniLM-L6-v2`)
3. **Vector Storage**: Stores embeddings in Qdrant vector database
4. **Semantic Search**: Retrieves relevant chunks based on user queries
5. **Context Integration**: Combines retrieved context with user questions

### Session Management

- **Persistent Sessions**: Chat history saved locally in JSON format
- **Session Isolation**: Each session has its own document context
- **Export Functionality**: Download chat history for backup or analysis

### Document Support

Supported file formats:
- **PDF**: Using PyPDFLoader
- **DOCX**: Using Docx2txtLoader  
- **TXT/MD/HTML**: Using UnstructuredFileLoader

## 🚧 Upcoming Features

We're actively working on exciting new features for the next version! Here's what's coming soon:

### 🧠 Advanced Memory & Persistence
- **Cross-Session Storage**: Persistent session storage across refreshes and deployments
- **Auto-Save & Resume**: Chat history automatically saved with seamless resume support
- **Cloud Backup**: Optional cloud synchronization for session data

### 📁 Enhanced Multi-File RAG Support
- **Batch Document Upload**: Upload and embed multiple documents simultaneously
- **Dynamic Source Management**: View, organize, and manage uploaded sources in real-time
- **Document Versioning**: Track and manage different versions of uploaded files
- **Cross-Document Queries**: Ask questions that span across multiple uploaded documents

### 💬 Next-Generation Chat UI
- **Source Transparency**: Toggle view of retrieved RAG context and sources used for each response
- **Rich Content Rendering**: Enhanced markdown support with tables, code blocks, links, and media
- **Customizable Sessions**: Editable session names (e.g., "Job Search Q&A", "Resume Analysis", "Research Notes")
- **Message Threading**: Organize conversations with threaded replies and topics

### 📊 Comprehensive Analytics & Tracking
- **Real-Time Metrics**: Live token usage display with visual indicators
- **Cost Estimation**: Accurate cost calculator for each interaction and session
- **Usage Visualization**: Interactive charts showing token consumption patterns
- **Performance Insights**: Response time analytics and model performance metrics

### 🔐 Enterprise-Ready Authentication
- **Secure Login System**: Optional user authentication for personal session access
- **Privacy Controls**: Session-based privacy settings and chat history protection
- **Team Collaboration**: Shared workspaces for team-based document analysis
- **Role-Based Access**: Different permission levels for various user types

### 📤 Advanced Export & Integration
- **Multi-Format Export**: Export complete chat sessions as PDF, Markdown, Word, or JSON
- **Source Linking**: Download RAG source documents with associated chat context
- **API Integration**: RESTful API for integrating with external systems
- **Webhook Support**: Real-time notifications and integrations with other tools

### 🎨 Customization & Themes
- **UI Themes**: Dark/light mode with custom color schemes
- **Layout Options**: Flexible interface layouts for different use cases
- **Custom Branding**: White-label options for enterprise deployments

### 🔍 Advanced Search & Discovery
- **Global Search**: Search across all sessions and documents
- **Smart Suggestions**: AI-powered query suggestions based on uploaded content
- **Bookmark System**: Save and organize important conversations and insights

**🎯 Timeline**: These features are planned for release in Q3-Q4 2025. Follow our repository for updates!

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone and setup
git clone https://github.com/Vigneshmaradiya/quantumchat-groq-rag.git
cd quantumchat-groq-rag

# Create development environment
conda create -n quantumchat-dev python=3.10
conda activate quantumchat-dev
pip install -r requirements.txt
```

### Running in Development Mode

```bash
# Run with auto-reload
PYTHONPATH=. streamlit run app/main.py --server.runOnSave true
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Implement your feature or fix
4. **Commit Changes**: `git commit -m "Add amazing feature"`
5. **Push to Branch**: `git push origin feature/amazing-feature`
6. **Open Pull Request**

## 🔍 Troubleshooting

### Common Issues

**GROQ API Key Error**:
```bash
# Check your .env file format
GROQ_API_KEY=gsk_your_actual_api_key_here
```

**Port Already in Use**:
```bash
# Use different port
PYTHONPATH=. streamlit run app/main.py --server.port 8502
```

**Qdrant Connection Issues**:
- Verify your Qdrant cluster is running
- Check API key and URL in `.env` file
- Ensure firewall allows connections

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GROQ Team**: For the lightning-fast inference engine
- **Streamlit**: For the excellent web framework
- **LangChain**: For RAG implementation components
- **Qdrant**: For vector database capabilities
- **HuggingFace**: For embedding models

## 📞 Contact

**Vignesh Maradiya**
- GitHub: [@Vigneshmaradiya](https://github.com/Vigneshmaradiya)
- Email: maradiyavignesh2004@gmail.com

---

⭐ If you found this project helpful, please consider giving it a star on GitHub!
