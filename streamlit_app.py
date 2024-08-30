import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from data_generator import generate_transactions, store_transaction
from gemini_api import analyze_transaction, send_status_to_third_party, get_fraud_reason
 
color = ''
message = ''
reason = ''
 
# Function to load summary state from file
def load_summary_state():
    try:
        with open('summary_state.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'total_transactions': 0,
            'anomalies': 0,
            'fraudulent_transactions': [],
            'transaction_counts': {'bank': 0, 'ecommerce': 0, 'payment_gateway': 0},
            'anomaly_counts': {'bank': 0, 'ecommerce': 0, 'payment_gateway': 0}
        }
 
# Function to save summary state to file
def save_summary_state(state):
    with open('summary_state.json', 'w') as f:
        json.dump(state, f)
 
# Function to save summary state to CSV file
def save_summary_to_csv(state):
    summary_data = {
        'Metric': ['Total Transactions', 'Total Anomalies', 'Bank Transactions', 'E-commerce Transactions', 'Payment Gateway Transactions', 'Bank Anomalies', 'E-commerce Anomalies', 'Payment Gateway Anomalies'],
        'Count': [state['total_transactions'], state['anomalies'], state['transaction_counts']['bank'], state['transaction_counts']['ecommerce'], state['transaction_counts']['payment_gateway'], state['anomaly_counts']['bank'], state['anomaly_counts']['ecommerce'], state['anomaly_counts']['payment_gateway']]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv('summary_state.csv', index=False)
 
# Load summary state from file
summary_state = load_summary_state()
 
# Initialize session state with loaded summary state
if 'total_transactions' not in st.session_state:
    st.session_state.total_transactions = summary_state['total_transactions']
if 'anomalies' not in st.session_state:
    st.session_state.anomalies = summary_state['anomalies']
if 'fraudulent_transactions' not in st.session_state:
    st.session_state.fraudulent_transactions = summary_state['fraudulent_transactions']
if 'transaction_counts' not in st.session_state:
    st.session_state.transaction_counts = summary_state['transaction_counts']
if 'anomaly_counts' not in st.session_state:
    st.session_state.anomaly_counts = summary_state['anomaly_counts']
 
st.set_page_config(page_title='Real-Time Transaction Analysis Dashboard', page_icon="bar_chart", layout="wide")
 
# Sidebar for transaction type selection
st.sidebar.title('Transaction Settings')
transaction_type = st.sidebar.selectbox('Select Transaction Type', ['bank', 'ecommerce', 'payment_gateway'])
 
# Button to process transactions
if st.sidebar.button('Validate'):
    transaction_generator = generate_transactions(transaction_type)
    transaction = next(transaction_generator)  # Get only the first transaction
    st.session_state.total_transactions += 1
    st.session_state.transaction_counts[transaction['transaction_type']] += 1
    st.sidebar.write(transaction)
   
   
    # Send transaction to Gemini API for anomaly detection
    response = analyze_transaction(transaction)
    is_anomoly = 0
    if response == "False":
        is_anomoly = 1
        st.session_state.anomalies += 1
        st.session_state.anomaly_counts[transaction['transaction_type']] += 1
        reason = get_fraud_reason(transaction)
        color = "red"
        message = f"Transaction {transaction['transaction_id']} failed due to anomaly."
        # st.error(f"Transaction {transaction['transaction_id']} failed due to anomaly.")
        # Send status to third-party application
        send_status_to_third_party(transaction['transaction_id'], 'failed')
        # Store fraudulent transaction
        st.session_state.fraudulent_transactions.append(transaction)
    else:
        is_anomoly = 0
        color = "green"
        message = f"Transaction {transaction['transaction_id']} is successful."
        # st.success(f"Transaction {transaction['transaction_id']} is successful.")
        send_status_to_third_party(transaction['transaction_id'], 'successful')
   
    # Generate Excel file for fraudulent transactions
    if st.session_state.fraudulent_transactions:
        df = pd.DataFrame(st.session_state.fraudulent_transactions)
        df.to_excel('fraud_transactions.xlsx', index=False)
   
    # Save updated summary state to file and CSV
    updated_summary_state = {
        'total_transactions': st.session_state.total_transactions,
        'anomalies': st.session_state.anomalies,
        'fraudulent_transactions': st.session_state.fraudulent_transactions,
        'transaction_counts': st.session_state.transaction_counts,
        'anomaly_counts': st.session_state.anomaly_counts
    }
    save_summary_state(updated_summary_state)
    save_summary_to_csv(updated_summary_state)
    store_transaction(transaction_type, transaction, is_anomoly)
   
    # Display JSON data
    # st.json(transaction)
 
# CSS to fix the bottom container and make the main section scrollable
st.markdown(
    """
    <style>
    .main-container {
        width: 100%;
        height: 70vh;
        overflow-y: scroll;
    }
    .fixed-container {
        position: fixed;
        bottom: 0;
        width: 70%;
        padding: 20px;
        height: 30vh;
        background-color: rgb(240, 242, 246);  
    }
    </style>
    <style>
        .st-emotion-cache-ue6h4q {display: none}
        .st-emotion-cache-1jicfl2 {padding: 1rem 1rem 10rem;}
        footer {visibility: hidden;}
    </style>
 
    """,
    unsafe_allow_html=True
)
 
# Main dashboard
st.title('Real-Time Transaction Analysis Dashboard')
st.subheader('Summary')
 
# Layout for dashboard and processed transaction results
dashboard_container = st.container()
results_container = st.container()
 
with dashboard_container:
    # Display summary metrics in a horizontal table without index
    summary_data = {
        'Metric': ['Total Transactions', 'Total Anomalies', 'Bank Transactions', 'E-commerce Transactions', 'Payment Gateway Transactions', 'Bank Anomalies', 'E-commerce Anomalies', 'Payment Gateway Anomalies'],
        'Count': [st.session_state.total_transactions, st.session_state.anomalies, st.session_state.transaction_counts['bank'], st.session_state.transaction_counts['ecommerce'], st.session_state.transaction_counts['payment_gateway'], st.session_state.anomaly_counts['bank'], st.session_state.anomaly_counts['ecommerce'], st.session_state.anomaly_counts['payment_gateway']]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df_transposed = summary_df.set_index('Metric').T  # Transpose the DataFrame
    st.table(summary_df_transposed)  # Display the DataFrame as a table
 
    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots(figsize=(5, 5))
        transaction_counts = [st.session_state.transaction_counts['bank'], st.session_state.transaction_counts['ecommerce'], st.session_state.transaction_counts['payment_gateway']]
        transaction_counts = [0 if pd.isna(x) else x for x in transaction_counts]  # Replace NaN with 0
        ax1.pie(transaction_counts, labels=['Bank', 'E-commerce', 'Payment Gateway'], autopct='%1.1f%%')
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig1)
    with col2:
        fig2, ax2 = plt.subplots(figsize=(5, 5))
        anomaly_counts = [st.session_state.anomaly_counts['bank'], st.session_state.anomaly_counts['ecommerce'], st.session_state.anomaly_counts['payment_gateway']]
        anomaly_counts = [0 if pd.isna(x) else x for x in anomaly_counts]  # Replace NaN with 0
        ax2.bar(['Bank', 'E-commerce', 'Payment Gateway'], anomaly_counts)
        ax2.set_ylabel('Number of Anomalies')
        ax2.set_title('Anomalies by Transaction Type')
        st.pyplot(fig2)
 
with results_container:
    st.markdown(f'''<div class="fixed-container">
                <h3>Processed Transaction Results</h3>
                <span style="color: {color}; font-size:25px; border: 1px solid">{message}</span><br>
                <span style="color: {color}; font-size:20px;">{reason}</span></div>''', unsafe_allow_html=True)
   