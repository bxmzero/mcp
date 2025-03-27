from mcp.server.fastmcp import FastMCP

mcp = FastMCP("FileWriter")


@mcp.tool()
def write_to_txt(filename: str, content: str) -> str:
    """
    将指定内容写入文本文件并且保存到本地。
    参数:
      filename: 文件名（例如 "output.txt"）
      content: 要写入的文本内容
    返回:
      写入成功或失败的提示信息
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"成功写入文件 {filename}。"
    except Exception as e:
        return f"写入文件失败：{e}"


if __name__ == "__main__":
    mcp.run(transport='stdio')  # 默认使用 stdio 传输