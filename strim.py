from numpy import place
from scipy.sparse import data
import streamlit as st
import pandas as pd
import main
import json

res = []

ret = st.chat_input(
		placeholder="Enter your message",
		key="chat",
		max_chars=None,
		# accept_file="multiple",
		height="stretch",
		)

# ret is None when no message submitted, string when user sends message
if ret:
	with st.chat_message(name="user"):
		st.write(ret)
	main.messages.append({"role": "user", "content": ret})
	res = main.run_ai()
	st.write(res)
