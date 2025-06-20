import getpass
import os

from dotenv import load_dotenv

# Load from .env file
load_dotenv()



if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY #getpass.getpass("Enter API key for Groq: ")



from langchain_groq import ChatGroq

llm = ChatGroq(model="llama3-8b-8192")





from langgraph.graph import MessageGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import MessageGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage

def start(messages=None):
    return HumanMessage(content="write a one-line tweet about a random topic.")

def generate(messages=None):
    if len(messages)==1:        
        all_msgs =messages[0].content #HumanMessage(content="write a one-line tweet about world war 2.")
        return AIMessage(content=llm.invoke([all_msgs]).content)

#     # all_msgs = messages
#     all_msgs = []
#     for i, msg in enumerate(messages):
        
#         # if i<2:
#         #     all_msgs.append(msg)
#         #     continue

            
            
#         if i%2==0:
#             all_msgs.append(HumanMessage(content=f"{msg.content}"))
#             continue
        
#         # if i%2==1:"
#         all_msgs.append(AIMessage(content=f"{msg.content}"))
        
#     print('-'*10)
#     print('all_msgs=', all_msgs)

#     response= llm.invoke(all_msgs)
#     # print('-'*10)
#     # print(all_msgs)
#     print('='*10)
    print('-'*10)
    
    # print(messages)
    print('='*10)
    
#     for msg in messages:
#         if isinstance(msg, HumanMessage):
       
#             print("(Hu) -->  ", msg.content)
#         else:
#             print('(AI) -->  ', msg.content)
#         
        

    response = llm.invoke(f'improve this tweet: {messages[-1].content}, and only give one-line tweet without explaining/mentioning what you changing')
    # if len(messages)%1==0:
        
    # return HumanMessage(content=f"how about this: {response.content}")
    # print('response.content=', response.content)
    return AIMessage(content=f"a better tweet is : {response.content}")

def reflect(messages):
    response = llm.invoke(f'improve this tweet: {messages[-1].content}, and only give one-line tweet without explaining/mentioning what you changing')
    return HumanMessage(content=f"{response.content}. Can you improve it more?")

def should_continue(msg):
    # print('msg[generate node]=',msg["generate_node"])
    print('len(msg)=', len(msg))
    if (len(msg)>6):
        return "to_final"
    return "to_continue"

def final(messages):
        print('='*10)
        for msg in messages:
            if isinstance(msg, HumanMessage):

                print("(Hu) -->  ", msg.content)
            else:
                print('(AI) -->  ', msg.content)
        print('='*10)
        response = llm.invoke(messages[:-1]) # technically the last must be a hummanMessage
        print('\n\nbased on all the corrections the final tweet would be:', response.content)
    
graph = MessageGraph()
# graph.add_edge(START, "generate")
graph.add_node("start", start)
graph.add_node("generate", generate)
graph.add_node("reflect", reflect)
graph.add_node("final", final)
graph.add_edge("start","generate")
graph.set_entry_point("start")

graph.add_conditional_edges("generate", 
                            should_continue,
                            
                          {    
        "to_continue": "reflect",  # Mapping function output to nodes
        "to_final": "final",
    },     
                           )
graph.add_edge("reflect", "generate")




# Compile the graph
app = graph.compile()

# # Run the graph with a dummy input
# graph.invoke([HumanMessage(content="Go!")])

app.invoke([])

# print('Done')