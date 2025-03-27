from openai import OpenAI

# Ollama 不验证 API key，但字段不能省略
client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")

def ask_qwen(question):
    response = client.chat.completions.create(
        model="qwen2.5:7b",  # 此处为你实际在Ollama启动的模型ID
        messages=[
            {"role": "system", "content": "你是一个专业的滑雪高手。"},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


# 测试调用
if __name__ == "__main__":
    question = "什么是刻滑，如何练习？"
    answer = ask_qwen(question)
    print("Qwen2的回答：")
    print(answer)