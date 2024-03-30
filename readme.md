Chatbot MySQL Python com GPT-4 e Mistral AI
Bem-vindo ao repositório GitHub de um chatbot utilizando SQL em linguagem natural com o GPT-4! desenvolvimento de um chatbot que pode interpretar consultas em linguagem natural, gerar consultas SQL e obter resultados de um banco de dados SQL, tudo de em um chat localhost gerado na inicialização do projeto. Integrado com uma GUI do Streamlit para uma experiência de interação aprimorada.

Recursos
Processamento de Linguagem Natural: Usa o GPT-4 para interpretar e responder a consultas de usuários em linguagem natural.
Geração de Consulta SQL: Gera dinamicamente consultas SQL com base na entrada em linguagem natural do usuário.
Interação com o Banco de Dados: Conecta-se a um banco de dados SQL para recuperar os resultados das consultas, demonstrando interação prática com banco de dados.
GUI do Streamlit: Apresenta uma interface amigável ao usuário construída com Streamlit, tornando fácil para usuários de todos os níveis de habilidade.
Baseado em Python: Totalmente codificado em Python, demonstrando boas práticas em desenvolvimento de software com tecnologias modernas.
Breve Explicação de Como o Chatbot Funciona
O chatbot funciona pegando uma consulta em linguagem natural do usuário, convertendo-a em uma consulta SQL usando o GPT-4, executando a consulta em um banco de dados SQL e depois apresentando os resultados de volta ao usuário em linguagem natural. Este processo envolve várias etapas de processamento de dados e interação com a API da OpenAI e um banco de dados SQL, tudo integrado de forma transparente em um aplicativo Streamlit.

Considere o seguinte diagrama para entender como as diferentes cadeias e componentes são construídos:

Arquitetura do Chatbot

Instalação
Certifique-se de ter o Python instalado em seu PC e o Anaconda para criar seu ambiente virtual. Em seguida, clone este repositório:

Para configurar a chave da API do OpenAI, siga estas etapas:

1. Acesse [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).
2. Copie sua chave da API do OpenAI
3. No seu projeto, crie um arquivo na raiz chamado `.env`
4. Dentro do arquivo `.env`, adicione a seguinte linha e substitua `SEU_OPENAI_API_KEY` pela sua chave da API do OpenAI:

    ```
    OPENAI_API_KEY=SEU_OPENAI_API_KEY
    ```

Para configurar a chave da API do GROQ, siga estas etapas:

1. Acesse [https://console.groq.com/playground](https://console.groq.com/playground).
2. Copie sua chave da API do GROQ.
3. No seu projeto, abra o arquivo `.env` que você criou anteriormente.
4. Adicione a seguinte linha e substitua `SEU_GROQ_API_KEY` pela sua chave da API do GROQ:

    ```
    GROQ_API_KEY=SEU_GROQ_API_KEY
    ```

<br>
```
git clone [link-do-repositório]
cd [diretório-do-repositório]
Instale os pacotes necessários:
```
<br>
Instale os requerimentos:
```
pip install -r requirements.txt
```
<br>
Para iniciar o aplicativo Streamlit e interagir com o chatbot:
```
streamlit run app.py
```

Licença
Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter detalhes.

Observação: Este projeto destina-se a fins educacionais e de pesquisa. Certifique-se de estar em conformidade com os termos de uso e diretrizes de quaisquer APIs ou serviços utilizados.

Feliz Codificação! 🚀👨‍💻🤖

Se você achar este projeto útil, considere dar a ele uma estrela!
