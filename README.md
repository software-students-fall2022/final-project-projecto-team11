[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9574936&assignment_repo_type=AssignmentRepo)


![Web App Workflow](https://github.com/software-students-fall2022/final-project-projecto-team11/actions/workflows/web-app-workflow.yml/badge.svg)

![Translator Service Worflow](https://github.com/software-students-fall2022/final-project-projecto-team11/actions/workflows/translator-service-workflow.yml/badge.svg)

# Final Project

## Description
Our app provides real-time translation of speech for users. Simply speak into the microphone and the app will transcribe your words into text, translate them, and display the translation through the web app. Additionally, users have the option to create an account to access their translation history.

Please run the below commands in a terminal on your system to install and run these programs. Before you begin, please [ensure Docker is installed on your system](https://docs.docker.com/engine/install/). Also, please [ensure ffmpeg is installed on your system](https://ffmpeg.org/download.html).

## Instructions to Install and run

### Step 1: Clone Repository
First, clone this repository onto your system:
```
git clone https://github.com/software-students-fall2022/final-project-projecto-team11.git
```
### Step 2: Start Docker Containers
In a seperate terminal window, in the root directory of the project, start the docker containers for the web app and MongoDB database by using:
```
docker compose up
```
If you receive permissions errors, use `sudo` in front of the above command if on Mac or Linux, or use an elevated PowerShell terminal to run the command if on Windows.

Now, navigate to <http://localhost:5001>.

## Hosts

[DigitalOcean Deployment](https://web-app-oyfrn.ondigitalocean.app/)

[Dockerhub Repo for Both Containers](https://hub.docker.com/repository/docker/chiaos/se_final_project_repo)

## Instructions for Use

### Sign in or sign up
Click on "Register" on the top left of the screen if you don't have an account, or "Sign in" on the top right if you have an account. After entering your information, submit it. That will take you to the recording page, where you can actually record what you want to translate.

### Translate recording
Select the language that you want to translate to from the dropdown menu. Then, press hold the "record" button to start speaking what you want to translate. When the button is released, the translation request will be processed and the result displayed.

### View translation history
If you are signed in, click the "Translation History" button on the top left and you will see a list of all translations you requested in the past.

### Logout
To logout from your account, click the "Logout" button on the top right corner.

## Members of Team 11
[Michael Ma](https://github.com/mma01us)

[David Adler](https://github.com/dov212)

[Harrison Douglass](https://github.com/hpdouglass)

[Sneheel Sarangi](https://github.com/Xarangi)

[Bruce Wu](https://github.com/bxw201)

[Brandon Chao](https:/github.com/Sciao)

[Khalifa AlFalasi](https:/github.com/Khalifa-AlFalasi)

### NOTE ON TRANSLATOR SERVICE DEPLOYMENT
Our translator-service container component uses multi-processing, which we have discovered to not be compatible with certain OSes. As a result, deployment to digital ocean was not possible in the scope of the project.
