# Textbook-QnA-RAG

This repository contains an implementation of **Retrieval-Augmented Generation (RAG)** for a textbook question-answering application. RAG combines generative models with retrieval mechanisms to provide more informed and contextually relevant outputs, enabling large language models (LLMs) to access updated information from specified documents or databases.

## What is RAG?

**Retrieval-Augmented Generation (RAG)** is a powerful technique that enhances LLMs by integrating external data retrieval into the response generation process. This allows models to utilize real-time or domain-specific knowledge, significantly improving the accuracy and relevance of their responses.

## Implementation Details

This implementation uses the **Ollama Framework** alongside **Mistral** for retrieval generation and **Nomic's embedding tools** for creating embeddings of text data.



## Getting Started

### Prerequisites

To run this application, ensure you have the following installed:

- Python 3.8>
- Ollama Framework- Install Ollama From Your Local Browser And Pull the LLM you need
- Mistral (for retrieval generation)
- Nomic's embedding tools (for text embedding)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/athrvakulkarni11/Textbook-QnA-RAG.git
   cd Textbook-QnA-RAG
   python withoutapp.py
