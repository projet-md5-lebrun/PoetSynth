from huggingface_hub import InferenceClient
import gradio as gr

client = InferenceClient("mistralai/Mixtral-8x7B-Instruct-v0.1")

def format_prompt(theme, syl, message):
    prompt = f"Crée un poeme en francais sur le theme {theme} de preference en {syl}. <s> [INST] {message} [/INST]"
    return prompt

def generate(
    text,
    theme,
    syl,
    temperature=0.9,
    max_new_tokens=256,
    top_p=0.95,
    repetition_penalty=1.0,
):
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=42,
    )

    formatted_prompt = format_prompt(theme, syl, text)
    stream = client.text_generation(
        formatted_prompt,
        **generate_kwargs,
        stream=True,
        details=True,
        return_full_text=False
    )

    output = ""
    for response in stream:
        output += response.token.text

    return output

iface = gr.Interface(
    fn=generate,
    inputs=[
        gr.Textbox(label="Enter a message"),
        gr.Radio(["Nature", "Chiens", "Other"], label="Choose a theme"),
        gr.Radio(["5", "7", "10"], label="Choose syllable count"),
    ],
    outputs="text",
   # live=True
)

iface.launch()
