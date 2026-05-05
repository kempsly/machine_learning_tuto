import requests  # used to send HTTP requests (to call your local model API)
import json      # used to convert Python objects <-> JSON format
import gradio as gr  # used to build a simple web UI

url = "http://localhost:11434/api/generate"  
# endpoint of your local model (e.g., Ollama running on port 11434)

headers = {
    'Content-Type': 'application/json'  
    # tells the server we are sending JSON data
}

history = []  
# list to store all previous prompts (for conversation memory)

def generate_response(prompt):  
    # function called every time user submits input in UI
    
    history.append(prompt)  
    # add current user prompt to history
    
    final_prompt = "\n".join(history)  
    # combine all previous prompts into one string (multi-turn context)

    data = {
        "model": "codeguru",  
        # name of the model you are calling (must exist in your local setup)

        "prompt": final_prompt,  
        # full conversation sent to model

        "stream": False  
        # disable streaming (we want full response at once)
    }

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(data)  
        # convert Python dict to JSON string before sending
    )

    if response.status_code == 200:  
        # check if request was successful
        
        response = response.text  
        # get response as raw text
        
        data = json.loads(response)  
        # convert JSON string back to Python dictionary
        
        actual_response = data['response']  
        # extract the model's generated text
        
        return actual_response  
        # return response to display in UI
    
    else:
        print("error:", response.text)  
        # print error message if request failed


interface = gr.Interface(
    fn=generate_response,  
    # function to call when user submits input

    inputs=gr.Textbox(lines=4, placeholder="Enter your Prompt"),  
    # input box (4 lines, with placeholder text)

    outputs="text"  
    # output will be displayed as plain text
)

interface.launch()  
# start the Gradio web app (opens in browser)