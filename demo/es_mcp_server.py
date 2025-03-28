from typing import List, Dict

from elasticsearch import Elasticsearch
from mcp.server.fastmcp import FastMCP

#创建一个mcp_server服务
mcp = FastMCP("FileWriter")
#es user=elastic code=mSlg_=OvoP0PCices5YS
es_client = Elasticsearch(
    hosts=["https://localhost:9200"],  # ES服务器地址
    basic_auth=("elastic", "mSlg_=OvoP0PCices5YS"),  # 用户名密码
    verify_certs=False  # 如是正式生产环境请改为True，并提供CA证书
)

# 测试连接是否成功
try:
    info = es_client.info()
    print("Elasticsearch connected:", info)
except Exception as e:
    print("连接失败:", e)

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



@mcp.tool()
def list_indices() -> List[str]:
    """列出所有 Elasticsearch 索引"""
    rs= [index["index"] for index in es_client.cat.indices(format="json")]

    return rs

@mcp.tool()
def get_index(index: str) -> dict:
    """获取特定 Elasticsearch 索引的详细信息"""
    return es_client.indices.get(index=index)


@mcp.resource("file://movies.csv")
def get_movies() -> str:
    """Return the contents of movies.csv file"""
    with open("movies.csv", "r") as f:
        return f.read()


@mcp.tool()
def write_documents(index: str, documents: List[Dict]) -> dict:
    """Write multiple documents to an Elasticsearch index using bulk API

    Args:
        index: Name of the index to write to
        documents: List of documents to write

    Returns:
        Bulk operation response from Elasticsearch
    """
    operations = []
    for doc in documents:
        # Add index operation
        operations.append({"index": {"_index": index}})
        # Add document
        operations.append(doc)

    return es_client.bulk(operations=operations, refresh=True)


if __name__ == "__main__":
    mcp.run(transport='stdio')  # 默认使用 stdio 传输