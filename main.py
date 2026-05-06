from typing import cast
from groq import Client, Groq
from groq.types.chat import ChatCompletion, ChatCompletionMessage, ChatCompletionMessageParam, ChatCompletionToolParam
from dotenv import load_dotenv
import json
import os
import streamlit as st

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {client}",
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

def sum_of_number(num1, num2):
	sum = num1+num2
	return{
			"num1":num1,
			"num2": num2,
			"sum": sum,
			}

messages : list[ChatCompletionMessageParam] =  [
		{"role": "system", "content": "You are a helpful assistant."},
		# {"role": "user", "content": "Add 5 and 10."}
		]

tools : list[ChatCompletionToolParam] = [
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
			},
		{
			"type": "function",
			"function": {
				"name": "sum_of_number",
				"description": "Calculate sum of two numbers",
				"parameters": {
					"type": "object",
					"properties": {
						"num1": {
							"type": "number",
							"description": "First number"
							},
						"num2": {
							"type": "number",
							"description": "Second number"
							}
						},
					"required": ["num1", "num2"]
					}
				}
			}
		]

available_functions = {
		"calculate_tax": calculate_tax,
		"sum_of_number": sum_of_number,
		}

def run_ai():
	response = client.chat.completions.create(
			model="llama-3.1-8b-instant",
			temperature=0.2,
			messages=messages,
			tools=tools,
			tool_choice="auto"
			)

	message = response.choices[0].message

	if message.tool_calls:
		messages.append(
				cast(ChatCompletionMessageParam, message.model_dump(exclude_none=True))
				)

		for tool_call in message.tool_calls:
			function_name = tool_call.function.name
			function_arg = json.loads(tool_call.function.arguments)

			result = available_functions[function_name](**function_arg)
			messages.append({
				"role": "tool",
				"tool_call_id": tool_call.id,
				"content": json.dumps(result)
				})

		final_response = client.chat.completions.create(
				model="llama-3.1-8b-instant",
				messages=messages
				)

		with st.chat_message(name="assistant"):
			st.write(st.write(final_response.choices[0].message.content))

	else:
		with st.chat_message(name="assistant"):
			st.write(message.content)
	return response
