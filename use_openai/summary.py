import openai
import gradio as gr
import json
from typing import List, Dict, Tuple

## TODO: Fill in your OpenAI api in the "" part
OPENAI_API_KEY = ""
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Check if you have set your ChatGPT API successfully
# You should see "Set ChatGPT API sucessfully!!" if nothing goes wrong.
try:
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = [{'role':'user','content': "test"}],
            max_tokens=1,
    )
    print("Set ChatGPT API sucessfully!!")
except Exception as e:
    print(e)
    print("There seems to be something wrong with your ChatGPT API. Please follow our demonstration in the slide to get a correct one.")


prompt_for_summarization = "Please summarize the following article"

# function to reset the conversation
def reset() -> List:
    return []

# function to call the model to generate
def interact_summarization(prompt: str, article: str, temp = 1.0) -> List[Tuple[str, str]]:
    '''
    * Arguments

      - prompt: the prompt that we use in this section

      - article: the article to be summarized

      - temp: the temperature parameter of this model. Temperature is used to control the output of the chatbot.
              The higher the temperature is, the more creative response you will get.

    '''
    input = f"{prompt}\n{article}"
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = [{'role':'user','content': input}],
            temperature = temp,
            max_tokens=200,
    )

    return [(input, response.choices[0].message.content)]

# function to export the whole conversation
def export_summarization(chatbot: List[Tuple[str, str]], article: str) -> None:
    '''
    * Arguments

      - chatbot: the model itself, the conversation is stored in list of tuples

      - article: the article to be summarized

    '''
    target = {"chatbot": chatbot, "article": article}
    with open("part1.json", "w") as file:
        json.dump(target, file)

# this part generates the Gradio UI interface
with gr.Blocks() as demo:
    gr.Markdown("# Summarization\nFill in any article you like and let the chatbot summarize it for you!!")
    chatbot = gr.Chatbot()
    prompt_textbox = gr.Textbox(label="Prompt", value=prompt_for_summarization, visible=False)
    article_textbox = gr.Textbox(label="Article", interactive = True, value = "")
    with gr.Column():
        gr.Markdown("#  Temperature\n Temperature is used to control the output of the chatbot. The higher the temperature is, the more creative response you will get.")
        temperature_slider = gr.Slider(0.0, 2.0, 1.0, step = 0.1, label="Temperature")
    with gr.Row():
        sent_button = gr.Button(value="Send")
        reset_button = gr.Button(value="Reset")

    # with gr.Column():
    #     gr.Markdown("#  Save your Result.\n After you get a satisfied result. Click the export button to recode it.")
    #     export_button = gr.Button(value="Export")
    sent_button.click(interact_summarization, inputs=[prompt_textbox, article_textbox, temperature_slider], outputs=[chatbot])
    reset_button.click(reset, outputs=[chatbot])
    # export_button.click(export_summarization, inputs=[chatbot, article_textbox])


demo.launch(debug = True)