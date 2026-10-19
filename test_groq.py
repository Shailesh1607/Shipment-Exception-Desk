
from llm import llm

try:
    response = llm.invoke(
        "Reply with exactly: Groq LLM is working!"
    )

    print("LLM connection successful!")
    print("Model response:", response.content)

except Exception as e:
    print("LLM test failed.")
    print("Error:", e)
