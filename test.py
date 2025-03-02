import openai

# Load API key securely (Use environment variable or a config file)
api_key = "OPENAI_API_KEY"  # Replace with your actual key

openai.api_key = api_key

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print("API Key is working ✅")
    print("Response:", response["choices"][0]["message"]["content"])
except openai.OpenAIError as e:
    print(f"Error: {e}")
