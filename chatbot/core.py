from rag.mongo_client import MongoClient

class Chatbot:
    def __init__(self,
        llm,
        mongodbUri: str,
        db_name: str,
        dbChatHistoryCollection: str,
        semanticCacheCollection: str,
    ):
        self.client = MongoClient().get_mongo_client(mongodbUri)
        self.db = self.client[db_name] 
        self.history_collection = self.db[dbChatHistoryCollection]
        self.semantic_cache_collection = self.db[semanticCacheCollection]
        self.llm = llm
    def __call__(self, session_id: str, query: str, enhanced_message: str, cache_response: bool = False, query_embedding: list[float]=[]):
        if query != enhanced_message:
            data=[
                {"role":"system","content":"You are a real-time chatbot assistant with the ability to perform Google searches. Your task is to help users find the most accurate and relevant information for their queries. DO NOT provide unrelated or off-topic responses."},
                {"role":"user","content":enhanced_message }
            ]

        else :
            data=[
                {"role":"system","content":"You are a helpful AI assistant. Answer user questions fully and confidently. If you don't know the answer, simply say you don't know. DO NOT provide unrelated or off-topic responses."},
                {"role":"user","content":query}
            ]
        response = self.llm.generate_content(data)
        response_content = response.choices[0].message.content

        self.history_collection.insert_one({
           "SessionId": session_id,
            "History": {
                "type": "user",
                "data":  {
                    "type": "user",
                    "content": query,
                }
            }
        })

        self.history_collection.insert_one({
           "SessionId": session_id,
            "History": {
                "type": "assistant",
                "data":  {
                    "type": "assistant",
                    "content": response_content,
                }
            }
        })
        if cache_response:
            embedding = query_embedding
            self.semantic_cache_collection.insert_one({
                "embedding": embedding,
                "text": [
                    {
                        "type": "human",
                        "content": query,
                        "enhanced_content": enhanced_message,
                    }
                ],
                "llm_string": {
                    "model_name": response.model,
                    "name": "ChatOpenAI"
                },
                "return_val": [
                    {
                        "type": "assistant",
                        "content": response_content,
                        "enhanced_content": None,
                        "id": response.id,
                        "usage_metadata": {
                            "input_tokens": response.usage.prompt_tokens,
                            "output_tokens": response.usage.completion_tokens,
                            "total_tokens": response.usage.total_tokens
                        },
                        "response_metadata": {
                            "usage": response.usage.to_json(),
                            "model_name": response.model,
                            "finish_reason": response.choices[0].finish_reason,
                            "logprobs": response.choices[0].logprobs
                        },
                    }
                ]
            })
        return response_content