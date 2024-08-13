import openai
import gradio as gr
import json

with open('key.json') as f:
    config = json.load(f)
    
OPENAI_API_KEY = config['OPENAI_API_KEY']
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
except:
    print("There seems to be something wrong with your ChatGPT API. Please follow our demonstration in the slide to get a correct one.")
    
# TODO: Fill in the below two lines: chatbot_task and chatbot_task
# The first is for you to tell the user that the chatbot can perform certain task
# The second one is the prompt that make the chatbot able to do certain task
chatbot_task = "FILL_IN_THE_TASK"
prompt_for_task = "FILL_IN_THE_PROMPT"

# function to clear the conversation
def reset() -> list:
    return []

# function to call the model to generate
def interact_customize(chatbot: list[tuple[str, str]], prompt: str ,user_input: str, temperature = 1.0) -> list[tuple[str, str]]:
    '''
    * Arguments

      - chatbot: the model itself, the conversation is stored in list of tuples

      - prompt: the prompt for your desginated task

      - user_input: the user input of each round of conversation

      - temp: the temperature parameter of this model. Temperature is used to control the output of the chatbot.
              The higher the temperature is, the more creative response you will get.

    '''
    try:
        messages = []
        messages.append({'role': 'user', 'content': prompt})
        for input_text, response_text in chatbot:
            messages.append({'role': 'user', 'content': input_text})
            messages.append({'role': 'assistant', 'content': response_text})

        messages.append({'role': 'user', 'content': user_input})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = messages,
            temperature = temperature,
            max_tokens=200,
        )

        chatbot.append((user_input, response.choices[0].message.content))

    except Exception as e:
        print(f"Error occurred: {e}")
        chatbot.append((user_input, f"Sorry, an error occurred: {e}"))
    return chatbot

def export_customized(chatbot: list[tuple[str, str]], description: str) -> None:
    '''
    * Arguments

      - chatbot: the model itself, the conversation is stored in list of tuples

      - description: the description of this task

    '''
    target = {"chatbot": chatbot, "description": description}
    with open("part3.json", "w") as file:
        json.dump(target, file)

# this part is to construct the Gradio UI interface
with gr.Blocks() as demo:
    gr.Markdown("# Part3: Customized task\nThe chatbot is able to perform a certain task. Try to interact with it!!")
    chatbot = gr.Chatbot()
    desc_textbox = gr.Textbox(label="Description of the task", value=chatbot_task, interactive=False)
    prompt_textbox = gr.Textbox(label="Prompt", value=prompt_for_task, visible=False)
    input_textbox = gr.Textbox(label="Input")
    with gr.Column():
        gr.Markdown("#  Temperature\n Temperature is used to control the output of the chatbot. The higher the temperature is, the more creative response you will get.")
        temperature_slider = gr.Slider(0.0, 1.0, 0.7, step = 0.1, label="Temperature")
    with gr.Row():
        sent_button = gr.Button(value="Send")
        reset_button = gr.Button(value="Reset")
    with gr.Column():
        gr.Markdown("#  Save your Result.\n After you get a satisfied result. Click the export button to recode it.")
        export_button = gr.Button(value="Export")
    sent_button.click(interact_customize, inputs=[chatbot, prompt_textbox, input_textbox, temperature_slider], outputs=[chatbot])
    reset_button.click(reset, outputs=[chatbot])
    export_button.click(export_customized, inputs=[chatbot, desc_textbox])

demo.launch(debug = True)