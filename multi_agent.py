import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool 
import openai
import wikipedia
print(os.getenv("OPENAI_API_KEY"))

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_MODEL = "gpt-4-32k"
OPENAI_MODEL = "gpt-3.5-turbo"
openai.api_key = OPENAI_API_KEY



st.set_page_config(page_title= "AI Reasearcher and Writing Tool", page_icon="🧠", layout="wide")
st.title("Advanced Multi-Agent AI Reasearcher & Writing Tool" )
st.write("Generate in-depth research papers and articles using Multiple AI Agents.")

topic = st.text_input("Enter the topic you want to research about:")
language = st.selectbox("Select the language you want to use:", ["english", "spanish", "french", "German", "italian", "Chinese", "japanese", "korian", "russian"])

reseach_depth = st.radio("Research Depth:",["Basic", "Detailed"])


if st.button("Run AI Research & Writing"):
    with st.spinner("Running AI Agent... Please wait..."):
        
        search_tool = SerperDevTool(api_key=SERPER_API_KEY)
        
        def wikipedia_search(query):
            try:
                summary = wikipedia.summary(query , sentences=3)
                return summary
              
            except wikipedia.exceptions.DisambiguationError as e:
                return f"Multiple results found:{e.options[:5]}"
            except wikipedia.exceptions.PageError:
                return "No Wikipedia article found for the given query."
            
        wiki_summary = wikipedia_search(topic)
        
        
# make the muilple agents writinf , search , reasearch and summarization
# reasearch agent make first: below code

        researcher = Agent(
            role="Senior Researcher",
            goal = f'Analyse and summarize the lastest developments in "{topic}"',
            verbose=True,
            memory=True,
            backstory="Ecpert in AI-Based reasearch and DATA analysis",
            tools=[search_tool],
            allow_delegation=True
            
        )
        
        
# Writing agent make second: below code

        writer = Agent(
            role="Senior Writer",
            goal = f'Write engaging content on {topic} in {language}',
            verbose=True,
            memory=True,
            backstory="Skilled in simplifying complex topics",
            tools=[search_tool],
            allow_delegation=False
        )

# editor agent make third: below code

        editor = Agent(
            role="Senior Editor",
            goal ="Refine and improve the article for better readability adn accuracy",
            verbose=True,
            memory=True,
            backstory="A meticulous editor ensuring top-quality content.",
            tools=[search_tool],
            allow_delegation=False
        )
        
# summarizer agent make fourth: below code

        # summarizer = Agent(
        #     role="Senior Summarizer",
        #     goal = f'Summarize the lastest developments in "{topic}"',
        #     verbose=True,
        #     memory=True,
        #     backstory="Ecpert in AI-Based reasearch and DATA analysis",
        #     tools=[search_tool],
        #     allow_delegation=False
        # )
        
        # crew = Crew(
        #     agents=[researcher, writer, editor, summarizer],
        #     verbose=True
        # )

        # if reseach_depth == "Basic":
        #     process = Process(
        #         crew=crew,
        #         tasks=[
        #             Task(agent=researcher, action="search", query=topic),
        #             Task(agent=writer, action="write", query=topic),
        #             Task(agent=editor, action="edit", query=topic),
        #             Task(agent=summarizer, action="summarize", query=topic)
        #         ]
        #     )
        # elif reseach_depth == "Detailed":
        #     process = Process(
        #         crew=crew,
        #         tasks=[
        #             Task(agent=researcher, action="search", query=topic),
        #             Task(agent=writer, action="write", query=topic),
        #             Task(agent=editor, action="edit", query=topic),
        #             Task(agent=summarizer, action="summarize", query=topic)
        #         ]
        #     )
        # else:
        #     process = Process(
        #         crew=crew,
        #         tasks=[
        #             Task(agent=researcher, action="search", query=topic),
        #             Task(agent=writer, action="write", query=topic),
        #             Task(agent=editor, action="edit", query=topic),
        #             Task(agent=summarizer, action="summarize", query=topic)
        #         ]
        #     )
        # process.run()
        # st.write(f"Research Summary: {researcher.memory}")
        # st.write(f"Article: {writer.memory}")
        # st.write(f"Edited Article: {editor.memory}")
        # st.write(f"Summary: {summarizer.memory}")
        # st.balloons()
        
        

        
        # define tasks for agents
        
        research_task = Task(
    description="Gather the latest research and provide a summary.",
    agent=researcher,
    expected_output="A well-researched summary of the topic in text format."
)

        
        write_task = Task(
    description = f"Create an in-depth article on {topic} in {language}, explaining its importance and future impact.",
    expected_output = "A well-formatted, informative article with expert analysis.",  # ✅ Correct spelling
    # tools = [search_tool],
    agent = writer
)

        edit_task = Task(
    description = f"Improve the readability, structure, and accuracy of the article on {topic}.",
    expected_output = "A polished, professional article ready for publishing.",  # ✅ Correct spelling
    # tools = [search_tool],
    agent = editor
)

        
        # summarizer_task = Task(
        #     description = f"Summarize the lastest developments in {topic}.",
        #     excepted_output = "A concise summary of the lastest developments in {topic}.",
        #     tools = [search_tool],
        #     agent = summarizer,
        # )
       
    #    reach in depth
    if reseach_depth == "Basic":
        crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task], process=Process.sequential)
    else:
        crew = Crew(agents=[researcher, writer, editor], tasks=[research_task, write_task, edit_task], process=Process.sequential)
        
    result = crew.kickoff(inputs={'topic': topic})
    st.success("AI Research and Writing Completed!")
    st.subheader("Generated Report:")
    st.write(result)
    
    
    summary_prompt = f"Summarize the following research on {topic} in a short, engaging paragraph:\n\n{result}"
    summary_response = openai.Completion.create(
        engine=OPENAI_MODEL,
        prompt=summary_prompt,
        max_tokens=150,
        temperature=0.7,
    )
    
    summary = summary_response.choices[0].text.strip()
    st.subheader("AI-Generated Summary:")
    st.write(summary)
    
    
    # download options
    
    st.download_button("Download as PDF", result, file_name=f"{topic}_report.pdf")
    st.download_button("Download as Markdown", result, file_name=f"{topic}_report.md")
    # st.download_button("Download as Text", result, file_name=f"{topic}_report.txt")
    
    # st.download_button("Download as PDF", summary, file_name=f"{topic}_summary.pdf")
    # st.download_button("Download as Markdown", summary, file_name=f"{topic}_summary.md")
    # st.download_button("Download as Text", summary, file_name=f"{topic}_summary.txt")
    
    # st.balloons()
       

    