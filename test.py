import gradio as gr
with gr.Column():
    file_obj = gr.File(label="Input File")
    input= file_obj
    output = gr.Textbox(label="Output")
iface = gr.Interface( fn = None, inputs=input, outputs=output)
iface.launch()
