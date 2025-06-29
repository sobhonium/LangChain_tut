
from langgraph.graph import START, END
from langgraph.graph import StateGraph
# from langchain.prompts import ChatPromptTemplate

# from config import llm

def build_state_graph(state_schema=None):


    graph = StateGraph(state_schema)



    # def start(state=None):
    #     print('start node entered')
    #     return "starrrrrrt"#HumanMessage(content="5")



    def first(state):
        print('frist node entered')
        from chains import first_chain
        # first_chain

        chain = first_chain()

        history_str = "\n".join([m for m in state["history"]])
        response = chain.invoke({
                # "topic": state["topic"],
                "history": history_str
            })
            
        state['history'].append('first speaker:'+ response.content)
        print('first node ended')
        print(state["current_iter"])
        return state
        
    def second(state):
        print('second node entered')
        from chains import second_chain
        chain = second_chain()

        
        history_str = "\n".join([m for m in state["history"]])
        response = chain.invoke({
                # "topic": state["topic"],
                "history": history_str
            })
            
        state['history'].append('second speaker:'+ response.content)
        print('second node ended')
        return state

    def third(state):
        print('thrid node entered')
        from chains import third_chain

        chain = third_chain()

        history_str = "\n".join([m for m in state["history"]])
        response = chain.invoke({
                # "topic": state["topic"],
                "history": history_str
            })
            
        state['history'].append('third speaker:'+ response.content)
        print('thrid node ended')
        # state["current_iter"]+=1
        if (state["current_iter"]>state["max_iter"]):
            dialogue = state['history']
            
    #         from collections import defaultdict

    #         # Collect all lines under their respective speakers
    #         grouped = defaultdict(list)

            # Format and print while preserving order
            for line in dialogue:
                if ':' in line:
                    speaker, msg = line.split(':', 1)
                    speaker = speaker.strip()
                    msg = msg.strip()
                    print(f"{speaker}):")
                    print(f"  {msg}")
                    print()
            
        print('='*20)
        return state

    def arbitar(state):
        if (state["current_iter"]>=state["max_iter"]):

            from chains import arbiter_verdict_chain    
            chain = arbiter_verdict_chain()
            history_str = "\n".join([m for m in state["history"]])
            response = chain.invoke({
            # "topic": state["topic"],
            "history": history_str
            })
            state["current_iter"]+=1
            
            state['history'].append('arbiter:'+ response.content)
            print('='*10)
            print('final verdict=',response.content)
            print('='*10)
            return state
            
        state["current_iter"]+=1
        
        if (state["history"]==[]):
            print(f'state is={state["history"]}')
            state['history'].append('arbiter: Alright, you guys are called as suspects here, after a rubbery in a shopping last night. I love to here your points and stories. Go on.')

            state['turn']='1st'
            return state
        # the number of nodes are 3 and we want at the first time, all nodes speak
        elif (state["current_iter"]<4):   
            if (state['turn']=='1st'):
                state['turn']='2nd'
                return state
            elif (state['turn']=='2nd'):
                state['turn']='3rd'
                return state
            elif (state['turn']=='3rd'):
                state['turn']='1st'
                return state
        else:
            from chains import arbiter_ruling_chain
            chain = arbiter_ruling_chain()
            
            history_str = "\n".join(state["history"])

            response = chain.invoke({
                "history": history_str
            })

            # Append formatted question to history
            state['history'].append(f"arbiter can you ({response.target_speaker}) answer this: {response.question}")
            
            if (response.target_speaker=='first speaker'):
                state['turn']='1st'
                return state
            elif (response.target_speaker=='second speaker'):
                state['turn']='2nd'
                return state
            elif (response.target_speaker=='third speaker'):
                state['turn']='3rd'
                return state
            return state      


    graph.add_node(first)
    graph.add_node(second)
    graph.add_node(third)
    graph.add_node(arbitar)


    def next_node(state):
        # print('msg[generate node]=',msg["generate_node"])
        if (state["current_iter"]>state["max_iter"]):
        #     print('---------Whole debate:-----------')
        #     for idx, msg in enumerate(state['history']):
        #         if idx%3==0:
        #             print('(first):', msg)
        #         if idx%3==1:
        #             print('(second):', msg)
        #         if idx%3==2:
        #             print('(thrid):', msg)                
            return "to_end"
        # print('len(msg)=', len(msg))
        if (state['turn']=='1st'):
            return "to_first"
        if (state['turn']=='2nd'):
            return "to_second"
        if (state['turn']=='3rd'):
            return "to_third"

        

        
    graph.add_edge(START, "arbitar")

    graph.add_conditional_edges("arbitar", 
                                next_node,
                                
                            {    
            "to_first": "first",  # Mapping function output to nodes
            "to_second": "second",  # Mapping function output to nodes
            "to_third": "third",  # Mapping function output to nodes
            "to_end":END,                      
            # "to_thrid": "trh",
        },  
                            )


    graph.add_edge("first", "arbitar")
    graph.add_edge( "second", "arbitar")
    graph.add_edge("third", "arbitar")

    return graph