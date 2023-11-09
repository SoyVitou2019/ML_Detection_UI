import gradio as gr
from assets.model import XG_boosting_prediction
from clients import send_request
import json
import ast
def save_non_abuse_class(top_classes):
    top_class_json = json.loads(json.dumps(top_classes['message']))
    top_class_json = ast.literal_eval(top_class_json)
    dic_predict = {
        "Non Abuse Image": 0,
        "Abuse Image": 0
    }
    temp_predict = []
    Non_abuse_doc = ["Nice emoji", "Non Abuse"]
    temp_predict.append(list(top_class_json.keys())[0])
    for k, v in top_class_json.items():
        if k in Non_abuse_doc:
            dic_predict["Non Abuse Image"] += v
        else:
            dic_predict["Abuse Image"] += v
    dic_predict = sorted(dic_predict.items(), key=lambda x: x[1], reverse=True)
    dic_predict = {k: v for k, v in dic_predict}
    return dic_predict
        
        
    
    
def prediction(img):
    # top_classes = XG_boosting_prediction(img)
    top_classes = send_request(img_input=img, url='http://18.139.116.122/')
    print(top_classes)
    save_class = save_non_abuse_class(top_classes)
    prediction_str = "\n".join([f"{index+1}. {property} : {round(value*100,2)}%" for index, (property, value) in enumerate(save_class.items())])
    return prediction_str

def clear_output():
    image_input.value = None
    prediction_output.value = None
    return None, None

with gr.Blocks(css="footer{display:none !important}") as demo:
    with gr.Row():
        image_input = gr.inputs.Image()
        prediction_output = gr.Textbox(placeholder="result", label="Prediction")
    image_button = gr.Button("Make prediction")
    clear_button = gr.Button("Clear")

    image_button.click(prediction, inputs=image_input, outputs=prediction_output)
    clear_button.click(clear_output, inputs=[], outputs=[image_input, prediction_output])

if __name__ == "__main__":
    demo.launch()