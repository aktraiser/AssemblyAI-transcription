import streamlit as st  # Importing streamlit, a framework for creating web apps.
import requests  # Importing requests module for sending HTTP requests.
import time  # Importing time module for timing operations.

st.title('AssemblyAI transcription')  # Setting the title of the web app.

file_buffer = st.file_uploader("Télécharger le fichier audio")  # Creating a file uploader widget.
language = st.text_input('Entrer le code de langue:')  # Creating a text input widget for language code.

upload_endpoint = "https://api.assemblyai.com/v2/upload"  # The endpoint for uploading the file.
headers = {'authorization':'...'}  # The headers for the request.

# This function reads the content of the uploaded file.
def read_file(file_buffer):
    if file_buffer is not None:
        return file_buffer.read()

if st.button('Transcrire'):  # If the 'Transcribe' button is clicked.
    if file_buffer is None:
        st.write("Veuillez télécharger un fichier.")  # If no file is uploaded, display an error message.
    else:
        # Upload the file and get the response.
        upload_response = requests.post(upload_endpoint, headers=headers, data=read_file(file_buffer))
        st.write(upload_response.json()['upload_url'])  # Display the upload URL.

        transcription_endpoint = "https://api.assemblyai.com/v2/transcript"  # The endpoint for transcription.

        json = {"audio_url":upload_response.json()['upload_url'], 
                "language_code":language}  # The payload for the transcription request.

        # Send the transcription request and get the response.
        transcription_response = requests.post(transcription_endpoint, headers = headers, json=json)
        st.write(transcription_response.json())  # Display the transcription response.

        transcript_id = transcription_response.json()['id']  # Get the transcript id from the response.

        polling_endpoint = transcription_endpoint + "/" + transcript_id  # The endpoint for polling the status.

        # Keep checking the status until the transcription is completed or an error occurs.
        while True:
            polling_response = requests.get(polling_endpoint, headers=headers)  # Send the request for status.
            status = polling_response.json()['status']  # Get the status from the response.
            
            if status == "completed":
                st.write(polling_response.json()['text'])  # If completed, display the transcription text.
                break  # Break the loop.
            
            elif status == "error":
                st.write('La transcription a rencontré une erreur!')  # If an error occurred, display an error message.
            
            else:
                st.write(status)  # If still in progress, display the status.
                time.sleep(2)  # Wait for 2 seconds before checking the status again.
                continue
