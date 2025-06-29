from dotenv import load_dotenv
from schema import GraphState
from graph_builder import build_state_graph

load_dotenv()

def main():
    initial_state = {
        "turn": None,
        "current_iter": 0,
        "max_iter": 6,
        "history": []
    }

    graph = build_state_graph(GraphState)
    app = graph.compile()
    result = app.invoke(initial_state, config={"recursion_limit": 2000})
    print("Final State:", result)

if __name__ == "__main__":
    main()