
import requests
import google.generativeai as genai


GOOGLE_API_KEY="AIzaSyBFmrbl7suBQNN7RekAEsWBkXIlizAS7f0"

def analyze_transaction(transaction):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name='gemini-pro')
    prompt = f"""You are an expert checking the transactions are legit or not. Your have to identify the transaction and provide response in single word 'True' or 'False' in below format. Where true stands for legit and false stands for fraudulent transaction {transaction}"""
    response = model.generate_content(prompt)
    print(response)
    return response.text


def get_fraud_reason(transaction):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name='gemini-pro')
    prompt = f"""You are an expert in identifying fraudulent transactions. For the transaction {transaction},
        provide a reason why it is considered fraudulent by replacing put_reason_here.
        Reason: <put_reason_here>"""
    response = model.generate_content(prompt)
    print(response)   
    return response.text


def send_status_to_third_party(transaction_id, status):
    # Example function to send status to third-party application
    # requests.post('https://third-party-app.com/status', json={'transaction_id': transaction_id, 'status': status})
    return status
    

