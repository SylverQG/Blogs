# [LLM](https://github.com/SylverQG/Blogs/issues/10)

快速入门RAG
========
来源：王海文


## 0.安装依赖库
```python
%pip install -U langchain_community tiktoken langchain_openai chromadb langchain langchain_core
%pip install sentence_transformers
%pip install huggingface_hub
%pip install ipywidgets
%pip install unstructured
%pip install sentencepiece bs4
```



## 1.加载文档


```python
from langchain_community.document_loaders import WebBaseLoader

url = "https://techdiylife.github.io/blog/202401/240327-ollama-20question.html"
loader = WebBaseLoader(
    web_paths=[url],
    requests_kwargs={
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
    }
)
docs = loader.load()
```

## 2.文本切分


```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
split_text = text_splitter.split_documents(docs)
```

## 3.向量化(Embedding)并存储


```python
%pip install langchain_ollama socksio httpcore[socks]
```



```python
from langchain_community.embeddings import OllamaEmbeddings
# from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# ollama下载embedding模型：https://ollama.ai/ 
# ollama pull mofanke/acge_text_embedding
# ollama pull qwen3-embedding:4b

embedding_model = OllamaEmbeddings(model="qwen3-embedding:4b")  # 参数名应为 model 而不是 model_name
vectorstore = Chroma.from_documents(documents=split_text, embedding=embedding_model)
retriever = vectorstore.as_retriever()
print("向量数据库构建完成")
```

    向量数据库构建完成


```bash
/tmp/ipykernel_1796418/1638132037.py:8: LangChainDeprecationWarning: The class `OllamaEmbeddings` was deprecated in LangChain 0.3.1 and will be removed in 1.0.0. An updated version of the class exists in the `langchain-ollama package and should be used instead. To use it run `pip install -U `langchain-ollama` and import as `from `langchain_ollama import OllamaEmbeddings``.
  embedding_model = OllamaEmbeddings(model="qwen3-embedding:4b")  # 参数名应为 model 而不是 model_name
向量数据库构建完成
```

## 4.构建prompt模板


```python
from langchain_core.prompts import ChatPromptTemplate

template = """你是一个回答问题的助手。请使用以下检索到的信息来回答问题。如果没有相关的信息，请回答"没有找到相关的信息。"。请用最多三句话来保持回答的简洁性

问题: {question}

背景: {context}

答案:
"""
prompt = ChatPromptTemplate.from_template(template) 


# 也可以从hub中加载
# from langchain import hub
# prompt = hub.load("tongshi/prompt_template_ragopenai")
```

## 5.初始化LLM


```python
# 在线api
# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI

# load_dotenv() # loads contents of the .env file

# llm = ChatOpenAI(
#     openai_api_base="https://api.openai.com/v1",
#     openai_api_version="2020-11-07",
#     openai_api_key=os.getenv("OPENAI_API_KEY")
#     model="gpt-3.5-turbo",
# )
# ==============================================

# 本地ollama
from langchain_community.llms import Ollama
llm = Ollama(model="deepseek-r1:7b")
# from langchain_ollama import OllamaLLM
# llm = OllamaLLM(model="deepseek-r1:7b")
```

```bash

/tmp/ipykernel_1796418/3311084766.py:18: LangChainDeprecationWarning: The class `Ollama` was deprecated in LangChain 0.3.1 and will be removed in 1.0.0. An updated version of the class exists in the `langchain-ollama package and should be used instead. To use it run `pip install -U `langchain-ollama` and import as `from `langchain_ollama import OllamaLLM``.
  llm = Ollama(model="deepseek-r1:7b")
```

## 6.构建 RAG Chain


```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def format_docs(docs):
    return "\n\n".join([f"{d.page_content}\n\n" for d in docs])

rag_chain = (
    {"context":retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# RunnablePassthrough():将原始输入传送给下一个节点
```

## 7.执行查询


```python
result = rag_chain.invoke("ollama支持哪些模型?")
print(result)
```

    ollama支持的模型包括70b、8b等版本，具体取决于下载和配置。instruct标签通常指代中文生成模型，text标签则指代中文推理模型，默认为text-3.5-turbo-instruct。官方支持的详细信息可参考https://ollama.com/library。


## 8.批量测试


```python
test_questions = [
    "ollama支持那些模型?",
    "Linux系统上,模型下载之后,模型存放在哪里?",
    "Windows系统上,如何修改默认下载位置?",
    "Modelfile是什么?",
    "如何导入safetensors格式的模型?",
    "有什么webui可用吗?",
]

for i,q in enumerate(test_questions[:3],start=1):
    print(f"问题 {i} : {q}")
    print(f"答案 {i} : {rag_chain.invoke(q)}\n")
```

    问题 1 : ollama支持那些模型?
    答案 1 : Ollama模型库中，70b和8b分别对应Qwen-7B和Qwen-8B模型；instruct是Instruct系列指令模型，text是专门的文本生成模型。
    
    问题 2 : Linux系统上,模型下载之后,模型存放在哪里?
    答案 2 : 在 Linux 系统上，默认情况下，下载好的模型会被存放在 `/home/<username>/.ollama/models` 的位置。
    
    问题 3 : Windows系统上,如何修改默认下载位置?
    答案 3 : 如何修改下载模型的默认存放目录？  
    在 Windows 系统中，可以进入 Documentary 或 Document folder 设置，默认存储位置为 C:\Users\<username>\.ollama\models。打开系统属性，选择“文档”或“更多文件夹”，找到 ollama_models 文件夹并修改其路径。
    


# 关键技术点

## 1.通过Ollama使用Embeddinng模型


```python
%ollama pull mxbai-embed-large
# 或
%ollama pull mofanke/acge_text_embedding
# 或
%ollama pull qwen3-embedding:4b
from langchain_community.embeddings import OllamaEmbeddings
# from langchain_ollama import OllamaEmbeddings
embedding_model = OllamaEmbeddings(model="qwen3-embedding:4b")
```

## 2.如何通过Ollama使用LLM


```python
# 本地ollama
from langchain_community.llms import Ollama
llm = Ollama(model="deepseek-r1:7b")
# llm = Ollama(model="qwen3")
```

>支持流式输出：
>```
>for chunk in llm.stream("讲个笑话"):
>    print(chunk,end="",flush=True)
>```

## 3.将Prompt提示词改为中文


```python
prompt = hub.pull("rlm/rag-prompt")
prompt.message[0].prompt.template = """你是一个回答问题的助手。请使用以下检索到的信息来回答问题。如果没有相关的信息，请回答"没有找到相关的信息。"。请用最多三句话来保持回答的简洁性

问题: {question}

背景: {context}

答案: """
```

或者直接用`ChatPromptTemplate.from_template()`自定义

## 4.RAG是如何进行检索的
1. 向量化：使用Embedding模型将文本转换为向量（如 mxbai-embed-large）
2. 相似度计算：使用余弦相似度 (cosine similarity) 向量数据库中查找最接近的文档
3. 返回Top-K：返回最相关的K个文档的上下文

`retriever = vectorstore.as_retriever(search_kwargs={"k":3}) # 返回前三个结果`

## 5.RAG是如何生成答案的
1. 将用户问题+检索到的上下文 -> 拼接成Prompt
2. 输入给LLM进行推理
3. LLM仅基于上下文作答，避免进行幻觉

>你是一个回答问题的助手。请使用以下检索到的信息来回答问题……
>
>问题: {question}
>
>背景: {context}
>
>答案: """

## 6.Runnable 接口

`Runnable` 是LangChain的抽象接口，它定义了如何运行一个任务，支持统一调用各种组件(LLM， Prompt, Chain, Agent, Parser等)

### 核心方法:
- `.invoke(inputs)`: 运行一个任务，返回结果
- `.batch(inputs, batch_size=1)`: 批量运行任务，返回结果
- `.stream(inputs)`: 运行一个任务，返回结果，支持流式输出
- `.bind(**kwargs)`: 绑定参数，返回一个新的Runnable对象
- `.ainvoke(inputs)`: 异步运行一个任务，返回结果
- `.abatch(inputs, batch_size=1)`: 异步批量运行任务，返回结果
### 组合方式(LCEL)：
```python
chain = prompt | llm | StrOutputParser()
chain.invoke({"topic": "bears"})
```
## 7.修改为读取本地文档


```python
# TXT文件
from langchain.document_loaders import TextLoader
loader = TextLoader('data/guide.txt')
docs = loader.load()

# HTML文件
from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader("example.html")
docs = loader.load()

# PDF文件（需要安装pypdf2）
from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("example.pdf")
docs = loader.load()

```

## 8.如何使用HuggingFace的Embedding模型


```python
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

model_name = "sentence-transformers/all-MiniLM-L6-v2"
model_kwargs = {"device": "gpu"}
ecode_kwargs = {"normalize_embeddings": False}
hf_embeddings = HuggingFaceEmbeddings(
    model_name=model_name, 
    model_kwargs=model_kwargs, 
    encode_kwargs=ecode_kwargs)
vector_store = Chorma.from_documents(splits, embedding=hf_embeddings)
```

## 9.使用HuggingFace的LLM
### 方法一：使用`transformers`+`pipeline`


```python
from transformers import AutoModelForCausalLm, AutoTokenizer, pipeline
from langchain.llms import HuggingFacePipeline

model_id = "THUDM/chatglm3-6b"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLm.from_pretrained(model_id, trust_remote_code=True, device_map="auto")
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, new_max_length=512)
llm = HuggingFacePipeline(pipeline=pipe)
```

### 方法二：使用from_model_id


```python
from langchain_huggingface import HuggingFacePipeLine

llm = HuggingFacePipeLine.from_model_id(
    model_id="google/gemma2-7b",
    task="text-generation",
    device_map="auto",
    model_kwargs={"temperature": 0.7, "max_length": 512,"trust_remote_code": True}
)
```

# RAG优化


|方向|描述|
|---|----|
|模型升级|使用更大更强的模型|
|Embedding优化|使用更高效的Embedding模型|
|文本切分|调整chunk_size (256~512)、overlap (50~100)|
|检索策略|修改K 值 (1~5)、尝试similarity_threshold (0.7~0.9)；过滤低分结果|
|Prompt工程|明确指令、限制输出格式、添加示例（few-shot）|
|引入Rerank|使用bge-rerank对检索结果重排序|