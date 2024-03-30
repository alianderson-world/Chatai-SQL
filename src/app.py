from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import streamlit as st

def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    uri_bd = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(uri_bd)

def get_sql_chain(bd):
    template = """
    Você é um analista de dados em uma empresa. Você está interagindo com um usuário que está fazendo perguntas sobre o banco de dados da empresa.
    Com base no esquema da tabela abaixo, escreva uma consulta SQL que responderia à pergunta do usuário. Leve em consideração o histórico da conversa.
    
    <ESQUEMA>{schema}</ESQUEMA>
    
    Histórico da Conversa: {chat_history}
    
    Escreva apenas a consulta SQL e mais nada. Não envolva a consulta SQL em nenhum outro texto, nem mesmo crases.
    
    Por exemplo:
    Pergunta: quais 3 artistas têm mais faixas?
    Consulta SQL: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    Pergunta: Nomeie 10 artistas
    Consulta SQL: SELECT Name FROM Artist LIMIT 10;
    
    Sua vez:
    
    Pergunta: {question}
    Consulta SQL:
    """
    
    prompt = ChatPromptTemplate.from_template(template)
  
    # llm = ChatOpenAI(model="gpt-4-0125-preview")
    llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
  
    def get_schema(_):
        return bd.get_table_info()
  
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )
    
def get_response(user_query: str, bd: SQLDatabase, chat_history: list):
    sql_chain = get_sql_chain(bd)
  
    template = """
    Você é um analista de dados em uma empresa. Você está interagindo com um usuário que está fazendo perguntas sobre o banco de dados da empresa.
    Com base no esquema da tabela abaixo, na pergunta, na consulta SQL e na resposta SQL, escreva uma resposta em linguagem natural.
    <ESQUEMA>{schema}</ESQUEMA>

    Histórico da Conversa: {chat_history}
    Consulta SQL: <SQL>{query}</SQL>
    Pergunta do usuário: {question}
    Resposta SQL: {response}"""
  
    prompt = ChatPromptTemplate.from_template(template)
  
    # llm = ChatOpenAI(model="gpt-4-0125-preview")
    llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
  
    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: bd.get_table_info(),
            response=lambda vars: bd.run(vars["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )
  
    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
    })
    
  
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Olá! Sou um assistente de SQL. Me pergunte qualquer coisa sobre o seu banco de dados."),
    ]

load_dotenv()

st.set_page_config(page_title="Conversa com MySQL", page_icon=":speech_balloon:")

st.title("Conversa com MySQL")

with st.sidebar:
    st.subheader("Configurações")
    st.write("Este é um aplicativo de chat simples usando MySQL. Conecte-se ao banco de dados e comece a conversar.")
    
    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Porta", value="3306", key="Port")
    st.text_input("Usuário", value="root", key="User")
    st.text_input("Senha", type="password", value="root", key="Password")
    st.text_input("Banco de Dados", value="worldb", key="Database")
    
    if st.button("Conectar"):
        with st.spinner("Conectando ao banco de dados..."):
            bd = init_database(
                st.session_state["User"],
                st.session_state["Password"],
                st.session_state["Host"],
                st.session_state["Port"],
                st.session_state["Database"]
            )
            st.session_state.bd = bd
            st.success("Conectado ao banco de dados!")
    
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("IA"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Humano"):
            st.markdown(message.content)

consulta_usuario = st.chat_input("Digite uma mensagem...")
if consulta_usuario is not None and consulta_usuario.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=consulta_usuario))
    
    with st.chat_message("Humano"):
        st.markdown(consulta_usuario)
        
    with st.chat_message("IA"):
        resposta = get_response(consulta_usuario, st.session_state.bd, st.session_state.chat_history)
        st.markdown(resposta)
        
    st.session_state.chat_history.append(AIMessage(content=resposta))
