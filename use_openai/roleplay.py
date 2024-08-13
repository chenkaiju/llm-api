import openai
import gradio as gr
import json

def init():
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

    return client



client = init()
character_for_chatbot = "You are a senior software engineer. You are good in python"
prompt_for_roleplay = "Answer any questions regarding to python"


# function to clear the conversation
def reset() -> list:
    return []


# function to call the model to generate
def interact_roleplay(
    chatbot: list[tuple[str, str]], user_input: str, temp=1.0
) -> list[tuple[str, str]]:
    """
    * Arguments

      - user_input: the user input of each round of conversation

      - temp: the temperature parameter of this model. Temperature is used to control the output of the chatbot.
              The higher the temperature is, the more creative response you will get.

    """
    try:
        messages = []
        for input_text, response_text in chatbot:
            messages.append({"role": "user", "content": input_text})
            messages.append({"role": "assistant", "content": response_text})

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temp,
            max_tokens=200,
        )
        chatbot.append((user_input, response.choices[0].message.content))

    except Exception as e:
        print(f"Error occurred: {e}")
        chatbot.append((user_input, f"Sorry, an error occurred: {e}"))
    return chatbot


# function to export the whole conversation log
def export_roleplay(chatbot: list[tuple[str, str]], description: str) -> None:
    """
    * Arguments

      - chatbot: the model itself, the conversation is stored in list of tuples

      - description: the description of this task

    """
    target = {"chatbot": chatbot, "description": description}
    with open("part2.json", "w") as file:
        json.dump(target, file)


first_dialogue = interact_roleplay([], prompt_for_roleplay)

# this part constructs the Gradio UI interface
with gr.Blocks() as demo:
    gr.Markdown(
        f"# Part2: Role Play\nThe chatbot wants to play a role game with you, try interacting with it!!"
    )
    chatbot = gr.Chatbot(value=first_dialogue)
    description_textbox = gr.Textbox(
        label=f"The character the bot is playing",
        interactive=False,
        value=f"{character_for_chatbot}",
    )
    input_textbox = gr.Textbox(label="Input", value="")
    with gr.Column():
        gr.Markdown(
            "#  Temperature\n Temperature is used to control the output of the chatbot. The higher the temperature is, the more creative response you will get."
        )
        temperature_slider = gr.Slider(0.0, 2.0, 1.0, step=0.1, label="Temperature")
    with gr.Row():
        sent_button = gr.Button(value="Send")
        reset_button = gr.Button(value="Reset")
    with gr.Column():
        gr.Markdown(
            "#  Save your Result.\n After you get a satisfied result. Click the export button to recode it."
        )
        export_button = gr.Button(value="Export")
    sent_button.click(
        interact_roleplay,
        inputs=[chatbot, input_textbox, temperature_slider],
        outputs=[chatbot],
    )
    reset_button.click(reset, outputs=[chatbot])
    export_button.click(export_roleplay, inputs=[chatbot, description_textbox])


demo.launch(debug=True)
