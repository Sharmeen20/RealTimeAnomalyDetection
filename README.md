## Realtime Analysis of Transactions and Dynamic Anomaly Detection Using Generative AI Models

**Abstract**
This document outlines a solution for real-time analysis of transactions and dynamic 
anomaly detection using generative AI models such as OpenAI and Gemini. The proposed 
system leverages advanced AI capabilities to identify fraudulent activities and anomalies 
in transaction data with high accuracy and minimal latency. Experimental results 
demonstrate the system's effectiveness in various transaction environments, showcasing 
its potential to enhance transaction security and integrity.

**Project Overview:**

**Our dashboard is designed to:**
• Ingest transaction data in real-time from various sources.
• Analyze transactions using advanced machine learning models for anomaly detection.
• Provide real-time alerts for suspicious activities.
• Visualize transaction data and anomalies for easy interpretation.

**Key Features:**
• Transaction Data Simulation: The dashboard generates realistic transaction data to simulate real world scenarios.
• Anomaly Detection: A pre-trained machine learning model is employed to identify deviations from normal transaction patterns.
• Real-Time Alerts: Users are notified immediately when suspicious transactions are detected.
• Interactive Dashboard: The dashboard provides a user-friendly interface for visualizing transaction summaries, anomalies, and processed results.

**Technical Implementation:**
• Programming Languages: Python
• Libraries: Streamlit, Pandas, Matplotlib, Google GenerativeAI
• Machine Learning: Pre-trained anomaly detection models
• Data Storage: In-memory data structures

# Run the below commands
-Check python version: python --version

-Install all the dependencies: pip install -r requirements.txt

-Run streamlit app: python -m streamlit run streamlit_app.py
