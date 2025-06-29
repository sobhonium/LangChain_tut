from config import llm
from langchain.prompts import ChatPromptTemplate
from schema import ArbiterQuestion


def first_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are the first speaker, and the second speaker is also your teammate. you and the second speaker stole something from the shopping last night. you should avoid the attention from yourself and also point to show the thrid speaker guitly of the rubbery. "),
        ("human", "Here is the conversation so far:\n\n{history}\n\n say something to help your teammate and fool the arbiter that the third speaker is a theif? just give one sentence without mentioning anything else.")
    ])
    first_node_chain = prompt | llm

    return first_node_chain

def second_chain():
    prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are the second speaker, and the firsts speaker is also your teammate. you  stole something from the shopping with the frist speaker."),
            ("human", "Here is the conversation so far:\n\n{history}\n\nsay something to help your teammate and fool the arbiter that the third speaker is a theif? just give one sentence without mentioning anything else.")
        ])
    second_node_chain = prompt | llm

    return second_node_chain


def third_chain():
    prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are the third speaker, the first and second speaker are blaming you that you stole from the shopping but you are not."),
            ("human", "Here is the conversation so far:\n\n{history}\n\nsay something to protect yourself and convince the arbiter that you are not a theif. just give one sentence without mentioning anything else.")
        ])
    third_node_chain = prompt | llm

    return third_node_chain


# The chain for the last verdict when it reaches out to the point
# it's needed to draw the conclusion and say the verdict outloud.
def arbiter_verdict_chain():
    prompt = ChatPromptTemplate.from_messages([
    ("system", f"You are the arbiter, the first and second and the third speakers are mentioning the stories and reasons. you should ask follow up questions to find the thief or theives."),
    ("human", "Here is the conversation so far:\n\n{history}\n\n as an arbiter who do you think is the theif. justify your verdict.")
    ])
    arbiter_verdict_chain = prompt | llm
    return arbiter_verdict_chain

# During the court session the arbiter should mange the turns for
# speakers and ask them follow up questions about the statm
def arbiter_ruling_chain():
    from langchain.output_parsers import PydanticOutputParser
    # from langchain.prompts import ChatPromptTemplate
    # from langchain.prompts import ChatPromptTemplate
    parser = PydanticOutputParser(pydantic_object=ArbiterQuestion)

    prompt = ChatPromptTemplate.from_messages([
        ("system", 
        f"You are the arbiter in a theft investigation. The first, second, and third speakers have provided their stories. "
        "Your job is to ask one of them a follow-up question to clarify their statement. Your output must follow this JSON schema:\n{format_instructions}"),

        ("human", 
        "Here is the conversation so far:\n\n{history}\n\n"
        "Ask a single follow-up question based on their previous statements. "
        "Choose **one** speaker only, and do not refer to yourself or repeat the background. "
        "Output must include the speaker you're targeting and the question.")
    ])

    prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    arbiter_rule_chain = prompt | llm | parser
    return arbiter_rule_chain

