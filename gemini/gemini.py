# Import packages
import google.generativeai as genai
from typing import List, Tuple
import gradio as gr
import json

# Set up Gemini API key
## TODO: Fill in your Gemini API in the ""
GOOGLE_API_KEY=""
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Check if you have set your Gemini API successfully
# You should see "Set Gemini API sucessfully!!" if nothing goes wrong.
try:
    model.generate_content(
      "test",
    )
    print("Set Gemini API sucessfully!!")
except:
    print("There seems to be something wrong with your Gemini API. Please follow our demonstration in the slide to get a correct one.")


## TODO: Input the prompt in the ""
prompt_for_summarization = "Summarize the following article:"

# function to clear the conversation
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
    response = model.generate_content(
      input,
      generation_config=genai.types.GenerationConfig(temperature=temp),
      safety_settings=[
          {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE",},
          {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE",},
          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE",},
          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE",},
          ]
    )

    return [(input, response.text)]

# function to export the whole conversation log
def export_summarization(chatbot: List[Tuple[str, str]], article: str) -> None:
    '''
    * Arguments

      - chatbot: the model itself, the conversation is stored in list of tuples

      - article: the article to be summarized

    '''
    target = {"chatbot": chatbot, "article": article}
    with open("part1.json", "w") as file:
        json.dump(target, file)


# This part constructs the Gradio UI interface
with gr.Blocks() as demo:
    gr.Markdown("# Summarization\nFill in any article you like and let the chatbot summarize it for you!!")
    chatbot = gr.Chatbot()
    prompt_textbox = gr.Textbox(label="Prompt", value=prompt_for_summarization, visible=False)
    article_textbox = gr.Textbox(label="Article", interactive = True, value = "")
    with gr.Column():
        gr.Markdown("#  Temperature\n Temperature is used to control the output of the chatbot. The higher the temperature is, the more creative response you will get.")
        temperature_slider = gr.Slider(0.0, 1.0, 0.7, step = 0.1, label="Temperature")
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