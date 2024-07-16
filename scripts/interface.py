import gradio as gr
import sys
sys.path.append('../sd-drive')
from uploader import uploader

def create_interface():
    with gr.Blocks() as interface:
        gr.Markdown("# Upload Files to Google Drive")
        with gr.Row():
            with gr.Column():
                input_dir = gr.Textbox(label="Input Directory", placeholder="/kaggle/working/x1101/outputs")
                gr.Markdown("Enter the full path of the directory containing the images.")
            with gr.Column():
                output = gr.Textbox(label="Output", placeholder="Status messages will appear here.")
        
        submit_button = gr.Button("Upload")
        submit_button.click(fn=uploader, inputs=[input_dir], outputs=[output])

    interface.launch()

if __name__ == "__main__":
    create_interface()
