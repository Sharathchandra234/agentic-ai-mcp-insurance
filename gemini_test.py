import os
from google import genai


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")


client = genai.Client(
    api_key=api_key,
    http_options={"api_version": "v1"}
)


interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Explain MCP in one simple sentence."
)


print(interaction.output_text)