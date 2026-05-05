
#  Machine Learning & AI — Complete Reference Repository

> A comprehensive, production-oriented machine learning repository covering the full AI/ML spectrum — from classical algorithms to Large Language Models, GenAI, and MLOps. Built as a personal reference combining multiple courses, projects, and real-world implementations.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Topics Covered](#topics-covered)
  - [Supervised Learning](#supervised-learning)
  - [Unsupervised Learning](#unsupervised-learning)
  - [Reinforcement Learning](#reinforcement-learning)
  - [Deep Learning — TensorFlow](#deep-learning--tensorflow)
  - [Deep Learning — PyTorch](#deep-learning--pytorch)
  - [Classical ML & Scikit-Learn](#classical-ml--scikit-learn)
  - [Other ML Libraries](#other-ml-libraries)
  - [Generative AI & LLMs](#generative-ai--llms)
  - [LangChain & LangGraph](#langchain--langgraph)
  - [LLMOps](#llmops)
  - [MLOps](#mlops)
  - [Model Building & Deployment](#model-building--deployment)
  - [Packages & Utilities](#packages--utilities)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Author](#author)

---

## Overview

This repository is a **massive personal ML reference** built by combining knowledge from multiple courses, tutorials, and real-world projects. It is structured to serve as a go-to reference for data scientists and ML engineers working across the full pipeline — from raw data to production deployment.

It covers:
- Classical and modern machine learning algorithms
- Deep learning with TensorFlow and PyTorch
- Generative AI, LLMs, RAG pipelines, and multi-agent systems
- MLOps and LLMOps for production-grade deployments
- End-to-end model building, serving, and monitoring

---

## Repository Structure

```
machine_learning_tuto/
│
├── supervised_learning/          ← regression, classification, ensemble methods
├── unsupervised_learning/        ← clustering, dimensionality reduction, anomaly detection
├── reinforcement_learning/       ← Q-learning, policy gradient, environments
├── deep_learning_tensorflow/     ← CNNs, RNNs, Transformers with TF/Keras
├── deep_learning_pytorch/        ← neural networks, CV, NLP with PyTorch
├── classical_ml/                 ← decision trees, SVM, Naive Bayes, KNN
├── scikit_learn/                 ← sklearn pipelines, preprocessing, model selection
├── other_ml_libraries/           ← XGBoost, LightGBM, CatBoost, statsmodels
├── generative_ai/                ← LLMs, prompting, RAG, agents, GenAI projects
├── langchain_langgraph/          ← LangChain chains, agents, LangGraph workflows
├── llmops/                       ← LLM evaluation, monitoring, fine-tuning, deployment
├── mlops/                        ← MLflow, Docker, CI/CD, model registry
├── model_building_deployment/    ← FastAPI, Streamlit, serving, containerization
└── packages/                     ← reusable utilities, helpers, custom modules
```

---

## Topics Covered

### Supervised Learning

Classical and modern supervised learning algorithms for regression and classification tasks.

| Topic | Description |
|---|---|
| Linear Regression | Simple, multiple, ridge, lasso, ElasticNet |
| Logistic Regression | Binary and multiclass classification |
| Decision Trees | CART, pruning, feature importance |
| Support Vector Machines | SVM, SVR, kernel tricks |
| K-Nearest Neighbors | KNN classification and regression |
| Ensemble Methods | Random Forest, Gradient Boosting, AdaBoost, Stacking |
| XGBoost | Full tutorial with SHAP, Optuna tuning, production pipeline |
| Evaluation | Cross-validation, metrics, bias-variance analysis |

---

### Unsupervised Learning

Algorithms for discovering hidden patterns without labeled data.

| Topic | Description |
|---|---|
| K-Means Clustering | Elbow method, silhouette score |
| DBSCAN | Density-based clustering, outlier detection |
| Hierarchical Clustering | Dendrograms, linkage methods |
| PCA | Principal Component Analysis, dimensionality reduction |
| t-SNE / UMAP | Non-linear dimensionality reduction, visualization |
| Autoencoders | Representation learning, anomaly detection |
| Anomaly Detection | Isolation Forest, LOF, statistical methods |

---

### Reinforcement Learning

Agents learning to make decisions through interaction with environments.

| Topic | Description |
|---|---|
| Q-Learning | Tabular Q-learning, exploration vs exploitation |
| Deep Q-Network | DQN with neural network function approximation |
| Policy Gradient | REINFORCE, actor-critic methods |
| OpenAI Gym | Environment setup, custom environments |
| PPO / A2C | Proximal Policy Optimization, Advantage Actor-Critic |

---

### Deep Learning — TensorFlow

Neural network implementations using TensorFlow and Keras.

| Topic | Description |
|---|---|
| Neural Network Fundamentals | Layers, activations, backpropagation |
| CNNs | Image classification, object detection |
| RNNs & LSTMs | Sequence modeling, time series |
| Transformers | Attention mechanism, BERT, fine-tuning |
| Transfer Learning | Pre-trained models, feature extraction |
| Custom Training Loops | tf.GradientTape, custom layers, callbacks |
| TF Data Pipeline | tf.data, data augmentation, performance optimization |

---

### Deep Learning — PyTorch

Neural network implementations using PyTorch.

| Topic | Description |
|---|---|
| Tensors & Autograd | PyTorch fundamentals, computational graphs |
| Neural Networks | nn.Module, custom architectures |
| CNNs in PyTorch | Image classification, feature maps |
| RNNs in PyTorch | LSTM, GRU, sequence tasks |
| Transformers | Attention, positional encoding, HuggingFace integration |
| Training Utilities | DataLoader, optimizers, schedulers, mixed precision |
| Model Saving | state_dict, checkpointing, ONNX export |

---

### Classical ML & Scikit-Learn

Core scikit-learn workflows for production-ready pipelines.

| Topic | Description |
|---|---|
| Preprocessing | Imputation, scaling, encoding, feature engineering |
| Pipelines | sklearn Pipeline, ColumnTransformer, FeatureUnion |
| Model Selection | GridSearchCV, RandomizedSearchCV, cross-validation |
| Feature Selection | RFE, SelectFromModel, importance-based selection |
| Imbalanced Data | SMOTE, class weights, resampling strategies |
| Evaluation | ROC AUC, confusion matrix, classification report |

---

### Other ML Libraries

Specialized libraries for high-performance ML.

| Library | Topics |
|---|---|
| **XGBoost** | Full tutorial, early stopping, SHAP, Optuna, production pipeline |
| **LightGBM** | Histogram boosting, categorical features, fast training |
| **CatBoost** | Native categorical handling, ordered boosting |
| **Statsmodels** | Statistical modeling, time series, hypothesis testing |
| **Optuna** | Bayesian hyperparameter optimization |
| **SHAP** | Model explainability, waterfall plots, feature importance |
| **imbalanced-learn** | SMOTE, ADASYN, undersampling techniques |

---

### Generative AI & LLMs

Large Language Models, prompting strategies, RAG pipelines, and multi-agent systems.

| Topic | Description |
|---|---|
| LLM Fundamentals | Transformer architecture, tokenization, inference |
| Prompt Engineering | Zero-shot, few-shot, chain-of-thought, system prompts |
| RAG Pipelines | Document loading, chunking, embedding, retrieval, generation |
| Hybrid Search | BM25 + semantic search, Reciprocal Rank Fusion |
| Vector Stores | FAISS, ChromaDB, AstraDB — setup and querying |
| Embeddings | HuggingFace embeddings, OpenAI embeddings, sentence-transformers |
| Multi-Agent Systems | Agent architectures, tool use, supervisor patterns |
| Document Intelligence | PDF, Word, PowerPoint, email, CSV processing for AI pipelines |
| GenAI Projects | End-to-end GenAI applications |

---

### LangChain & LangGraph

Full framework coverage for building LLM-powered applications.

| Topic | Description |
|---|---|
| LangChain Chains | LLMChain, SequentialChain, summarization chains |
| LangChain Agents | ReAct agents, tool use, AgentExecutor |
| LangChain Tools | DuckDuckGo, Python REPL, custom tools with @tool |
| LangChain Memory | ConversationBufferMemory, SummaryMemory |
| LangChain Retrievers | BM25, FAISS, EnsembleRetriever |
| LangGraph Basics | StateGraph, nodes, edges, conditional routing |
| LangGraph Multi-Agent | Supervisor pattern, parallel execution, shared state |
| LangGraph + RAG | Hybrid search nodes, memory-enabled RAG pipelines |
| CrewAI | Role-based agent crews, task delegation, sequential/parallel execution |
| LangSmith | Tracing, debugging, observability for LLM apps |

---

### LLMOps

Production operations for Large Language Model systems.

| Topic | Description |
|---|---|
| LLM Evaluation | RAGAS, faithfulness, relevance, groundedness metrics |
| Prompt Management | Versioning prompts, A/B testing, prompt registries |
| Fine-tuning | LoRA, QLoRA, instruction tuning, PEFT |
| Model Monitoring | Drift detection, hallucination monitoring, cost tracking |
| LangSmith | Tracing, evaluation, dataset management |
| Guardrails | Input/output validation, safety filters, NeMo Guardrails |
| Cost Optimization | Token budgeting, caching, model routing |

---

### MLOps

Infrastructure and practices for deploying ML models to production.

| Topic | Description |
|---|---|
| MLflow | Experiment tracking, model registry, artifact storage |
| Docker | Containerizing ML models and pipelines |
| CI/CD | GitHub Actions for automated testing and deployment |
| Data Versioning | DVC — tracking datasets and model artifacts |
| Model Registry | Staging, production, archiving models |
| Experiment Tracking | Logging parameters, metrics, artifacts |
| Pipeline Orchestration | End-to-end ML pipeline automation |

---

### Model Building & Deployment

End-to-end model serving and application development.

| Topic | Description |
|---|---|
| FastAPI | Complete REST API tutorial, endpoints, dependencies, middleware |
| Streamlit | Interactive ML dashboards and demo applications |
| Model Serving | REST API with FastAPI + XGBoost/sklearn/LLM |
| Containerization | Docker + Docker Compose for ML services |
| Cloud Deployment | AWS Lambda with Mangum, serverless ML endpoints |
| Gradio | Quick ML demo interfaces |

---

### Packages & Utilities

Reusable modules and helper functions.

| Module | Description |
|---|---|
| Data processors | PDF, Word, PowerPoint, email, CSV processors |
| Evaluation utils | Metric computation, reporting, visualization helpers |
| Pipeline templates | Reusable sklearn and LangChain pipeline components |
| Config management | Environment variables, settings, configuration loaders |

---

## Tech Stack

### Core ML
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-2.x-red)
![LightGBM](https://img.shields.io/badge/LightGBM-4.x-green)

### Deep Learning
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow)

### GenAI & LLMs
![LangChain](https://img.shields.io/badge/LangChain-0.3-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-latest-purple)
![FAISS](https://img.shields.io/badge/FAISS-vector--store-lightgrey)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector--store-green)

### Deployment
![FastAPI](https://img.shields.io/badge/FastAPI-0.11x-teal)
![Docker](https://img.shields.io/badge/Docker-containerization-blue)
![MLflow](https://img.shields.io/badge/MLflow-tracking-blue)

### LLM Providers
![Groq](https://img.shields.io/badge/Groq-LPU-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-black)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Inference-yellow)

---

## Getting Started

### Prerequisites

```bash
Python 3.10+
pip or conda
```

### Clone the repository

```bash
git clone https://github.com/kempsly/machine_learning_tuto.git
cd machine_learning_tuto
```

### Create a virtual environment

```bash
# using venv
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# using conda
conda create -n ml_env python=3.10
conda activate ml_env
```

### Install dependencies

Each folder contains its own `requirements.txt`. Install dependencies for the section you want to explore:

```bash
# example — install for GenAI / LangChain section
pip install -r langchain_langgraph/requirements.txt

# example — install for classical ML section
pip install -r classical_ml/requirements.txt

# install everything (may take a while)
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the root (never commit this):

```bash
# .env
OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
LANGSMITH_API_KEY=your_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=ml_tuto
HF_TOKEN=your_huggingface_token
```

---

## Navigation Guide

| You want to... | Go to |
|---|---|
| Build a classification model end-to-end | `supervised_learning/` + `scikit_learn/` |
| Learn XGBoost with SHAP and Optuna | `other_ml_libraries/xgboost/` |
| Build a RAG pipeline | `generative_ai/rag/` + `langchain_langgraph/` |
| Build multi-agent systems | `langchain_langgraph/langgraph/` |
| Deploy a model as REST API | `model_building_deployment/fastapi/` |
| Track ML experiments | `mlops/mlflow/` |
| Process financial documents with AI | `generative_ai/document_intelligence/` |
| Learn ensemble methods | `supervised_learning/ensemble/` + `other_ml_libraries/` |

---

## Author

**Kempsly Silencieux**

AI Engineer / Data Scientist

[![GitHub](https://img.shields.io/badge/GitHub-kempsly-black)](https://github.com/kempsly)

---

> *"The best way to learn machine learning is to build things, break things, and document everything."*

---

⭐ If you find this repository useful, feel free to star it.
