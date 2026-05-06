import os
import json
import requests
GROQ_API_KEY = "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"
headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {GROQ_API_KEY}",
		}
def calculate_tax(price, tax_rate):
	tax = price * tax_rate / 100
	total = price + tax
	return {
			"price": price,
			"tax_rate": tax_rate,
			"tax": tax,
			"total": total
			}
messages = [
		{"role": "system", "content": "You are a helpful assistant."},
		{"role": "user", "content": "Calculate 15% tax on 200 dollars."}
		]
tools = [
		{
			"type": "function",
			"function": {
				"name": "calculate_tax",
				"description": "Calculate tax and total price",
				"parameters": {
					"type": "object",
					"properties": {
						"price": {
							"type": "number",
							"description": "Original price before tax"
							},
						"tax_rate": {
							"type": "number",
							"description": "Tax rate percentage"
							}
						},
					"required": ["price", "tax_rate"]
					}
				}
			}
		]
body = {
		"model": "llama-3.1-8b-instant",
		"temperature": 0.2,
		"messages": messages,
		"tools": tools,
		"tool_choice": "auto"
		}
response = requests.post(
		"https://api.groq.com/openai/v1/chat/completions",
		headers=headers,
		json=body,
		)
data = response.json()
message = data["choices"][0]["message"]

print(message)
