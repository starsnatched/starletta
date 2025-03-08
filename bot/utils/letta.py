from letta_client import AsyncLetta, LlmConfig, EmbeddingConfig, MessageCreate
from decouple import config
from typing import List

class LettaClient:
    def __init__(self):
        self.client = AsyncLetta(base_url=config("LETTA_BASE_URL"))
        
    async def create_agent(self, name: str, user_id: int):
        return await self.client.agents.create(name=name, 
                                               llm_config=LlmConfig(model=config("LETTA_MODEL"), model_endpoint_type="ollama", context_window=config("LETTA_CONTEXT_WINDOW"), model_endpoint=config("OLLAMA_BASE_URL")),
                                               embedding_config=EmbeddingConfig(embedding_endpoint_type="ollama", embedding_model=config("LETTA_EMBEDDING_MODEL"), embedding_dim=config("LETTA_EMBEDDING_DIM"), embedding_endpoint=config("OLLAMA_BASE_URL")),
                                               project_id=str(user_id)
                                               )
        
    async def delete_agent(self, agent_id: str):
        return await self.client.agents.delete(agent_id)
        
    async def list_agents(self, user_id: int):
        return await self.client.agents.list(project_id=str(user_id))
    
    async def retrieve_agent(self, agent_id: str):
        return await self.client.agents.retrieve(agent_id)
    
    async def send_message(self, agent_id: str, messages: List[MessageCreate]):
        return await self.client.agents.messages.create(
            agent_id=agent_id,
            messages=messages
        )
        
    async def list_messages(self, agent_id: str):
        return await self.client.agents.messages.list(agent_id)
        
async def main():
    letta = LettaClient()
    agent = await letta.create_agent("test", 123)
    agent_list = await letta.list_agents(123)
    agent_id = agent_list[0].id
    print(agent_id)
    # await letta.delete_agent(agent.id)
    # print(await letta.list_agents(123))
    output = await letta.send_message(agent.id, [MessageCreate(role="user", content="Hello")])
    print(output.messages[0].reasoning)
    print(output.messages[1].content)
    
    # print(await letta.list_messages(agent.id))
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())