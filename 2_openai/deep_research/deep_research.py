import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)


# callback that gets called
# With these callbacks, you just return a result, the chat function that we've worked on in the past,
# that's an example of a callback. Chat just returns the result, but you can also, instead of doing that, have your callback functions
# be generators that Gradio needs to needs to iterate over and they will yield back results.
# And if you do that, then Gradio will show that incrementally in the user interface, so that you don't
# have to sit there and wait for a long time and suddenly see an output.
# You can see interim results as well.

async def run(query: str):
    async for chunk in ResearchManager().run(query):
        yield chunk


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")
    
    # inputs to the callback, contents of the query textbox
    # outputs what ever from the callback, to hook that up gradio hook it up to report markdown
    # run button
    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    # enter key
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True)

