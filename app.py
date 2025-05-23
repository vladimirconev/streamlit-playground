
def main():
    favicon = Image.open("images/smiley.png")
    st.set_page_config(
        page_title="My custom page title",
        page_icon=favicon,
        layout="centered"
    )

    STREAMLIT_SVG = "images/streamlit-logo-primary-colormark-darktext.svg"

    st.image(STREAMLIT_SVG, caption="Playground")

    st.header("GIT email config", divider="gray")

    process = subprocess.Popen(["git", "config", "--global", "user.email"], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    st.text("Current state: " + stdout)
    email = st.radio("Please select preferred git email:", ["vladimir.conev@scalefocus.com",
                                                            "conev.vladimir@gmail.com"])
    if st.button("Apply") and email:
        git_command = f"git config --global user.email {email}"
        print(git_command)
        os.system(git_command)
        st.rerun()

    st.header("Docker Desktop", divider="blue")

    st.image("images/docker_.png", caption=None)

    docker_status = os.system("docker desktop status")
    ## 1 not running
    ## 0 running
    print(docker_status)

    if st.button("Start", disabled=docker_status == 0):
        docker_start_cmd = "docker desktop start"
        output = os.system(docker_start_cmd)
        print(output)
        print(os.system("docker desktop status"))
        st.rerun()
    if st.button("Stop it", disabled=docker_status != 0):
        docker_stop_cmd = "docker desktop stop"
        os.system(docker_stop_cmd)
        st.rerun()

    st.header("OpenWeb UI", divider="green")

    if st.button("Spin it"):
        os.system("open-webui serve")

    st.header("Ollama", divider="red")

    st.image("images/Lama--Streamline-Ultimate.png", caption=None)

    if st.button("List"):
        process = subprocess.Popen(["ollama", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        st.text(stdout)

    model_to_pull = st.text_input("LLM model", "i.e. llama3.2-vision")
    if st.button("Pull"):
        os.system(f"ollama pull {model_to_pull}")
        st.badge("Success", icon=":material/check:", color="green")

    # ["jpg", "jpeg", "png"]
    uploaded_files = st.file_uploader(
        "Choose image", accept_multiple_files=True, type=["jpg", "jpeg", "png"]
    )
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        base64_encoded_bytes = base64.b64encode(bytes_data)
        # Decode the Base64 bytes to a string (UTF-8 by default)
        base64_encoded_string = base64_encoded_bytes.decode('utf-8')
        system_prompt = """You are Image AI assistant. 
            List all items you see on the image and define their category.
            Return items inside the JSON array in RFC8259 compliant JSON format."""
        response = ollama.chat(
            model='llama3.2-vision',
            messages=[{
                'role': 'assistant',
                'system': system_prompt,
                'temperature': 0,
                'content': 'Provide detected category and detected objects as RFC8259 compliant JSON. No further info on surroundings and background are required.',
                'images': [base64_encoded_string]
            }])
        st.text(response.message.content)
        st.json(response.message.content, expanded=True)


if __name__ == "__main__":
    import base64
    import streamlit as st
    import os
    import subprocess
    import ollama
    from PIL import Image
    main()