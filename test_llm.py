from utils.llm import get_llm

llm = get_llm()
print("Invoking LLM...")
res = llm.invoke("Hello, what is 2+2?")
print("Response:", res.content)
