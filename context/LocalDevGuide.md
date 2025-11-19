# Local Development Guide: HiveInvestor

This guide provides instructions for setting up your local development environment for the HiveInvestor project. We will be using VirtualBox for virtual machines, Python (FastAPI) for the backend, and Node.js (Vue.js with Tailwind CSS) for the frontend. This guide assumes a macOS host environment.

## 1. Prerequisites

Before you begin, ensure you have the following installed on your macOS host:

*   **Homebrew:** A package manager for macOS. If not installed, follow the instructions on [Homebrew's official website](https://brew.sh/).
*   **VirtualBox:** A powerful x86 and AMD64/Intel64 virtualization product. Download and install from [VirtualBox Downloads](https://www.virtualbox.org/wiki/Downloads).
*   **Vagrant:** A tool for building and managing virtual machine environments. Install via Homebrew:
    ```bash
    brew install vagrant
    ```
*   **Git:** For version control. Install via Homebrew:
    ```bash
    brew install git
    ```
*   **VS Code (Recommended IDE):** Download from [Visual Studio Code](https://code.visualstudio.com/).

## 2. Virtual Machine Setup (Ubuntu Server)

We will use Vagrant to provision an Ubuntu Server VM for our development environment.

### 2.1. Create a Project Directory and Vagrantfile

1.  Navigate to your project root directory:
    ```bash
    cd /Users/cwserna/code/gemini-demo
    ```
2.  Create a `Vagrantfile` in the root of your project. This file defines your VM configuration.
    ```bash
    vagrant init ubuntu/focal64
    ```
    This will create a basic `Vagrantfile`. Open it and modify it to include port forwarding and a synced folder.

    **Example `Vagrantfile` content:**
    ```ruby
    Vagrant.configure("2") do |config|
      config.vm.box = "ubuntu/focal64"
      config.vm.network "forwarded_port", guest: 8000, host: 8000 # FastAPI
      config.vm.network "forwarded_port", guest: 8080, host: 8080 # Vue.js Dev Server
      config.vm.synced_folder ".", "/vagrant" # Syncs your project folder to /vagrant in the VM
    end
    ```

### 2.2. Start and SSH into the VM

1.  From your project root directory, start the VM:
    ```bash
    vagrant up
    ```
    This may take some time as it downloads the Ubuntu image.
2.  Once the VM is running, connect to it via SSH:
    ```bash
    vagrant ssh
    ```

## 3. Inside the Virtual Machine: Environment Setup

Once you are SSHed into your Ubuntu VM, follow these steps to set up the development environment.

### 3.1. Update and Install Basic Tools

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git
```

### 3.2. Python (Backend - FastAPI)

1.  **Install pyenv (Recommended for Python Version Management):**
    ```bash
    curl https://pyenv.run | bash
    ```
    Follow the on-screen instructions to add `pyenv` to your shell's PATH. You'll typically need to add lines like these to your `~/.bashrc` or `~/.profile`:
    ```bash
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
    source ~/.bashrc
    ```
2.  **Install Python:**
    ```bash
    pyenv install 3.9.18 # Or your preferred Python 3.x version
    pyenv global 3.9.18
    ```
3.  **Create a Virtual Environment:**
    Navigate to your synced project directory (where your backend code will reside).
    ```bash
    cd /vagrant/backend # Assuming your backend code is in a 'backend' folder
    python -m venv venv
    source venv/bin/activate
    ```
4.  **Install FastAPI and Uvicorn:**
    ```bash
    pip install fastapi uvicorn[standard]
    ```
5.  **Install Google Cloud Client Library for Firestore:**
    ```bash
    pip install google-cloud-firestore
    ```

### 3.3. Node.js (Frontend - Vue.js with Tailwind CSS)

1.  **Install NVM (Node Version Manager):**
    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
    ```
    Close and reopen your SSH session, or run `source ~/.bashrc` (or `~/.profile`) to load NVM.
2.  **Install Node.js:**
    ```bash
    nvm install --lts
    nvm use --lts
    ```
3.  **Install Vue CLI (if needed, or use Vite):**
    For new projects, Vite is often preferred. If you need Vue CLI:
    ```bash
    npm install -g @vue/cli
    ```
4.  **Create a Vue.js Project (if not already created):**
    Navigate to your synced project directory.
    ```bash
    cd /vagrant/frontend # Assuming your frontend code is in a 'frontend' folder
    # If using Vite:
    npm create vue@latest
    # Follow prompts, select Vue, JavaScript/TypeScript, Router, Pinia, etc.
    # Then:
    cd <your-vue-project-name>
    npm install
    npm install -D tailwindcss postcss autoprefixer
    npx tailwindcss init -p
    ```
    Configure `tailwind.config.js` and `postcss.config.js` as per Tailwind CSS documentation for Vue.js.

## 4. Running the Application

### 4.1. Backend (FastAPI)

1.  SSH into your VM: `vagrant ssh`
2.  Navigate to your backend project directory: `cd /vagrant/backend`
3.  Activate your Python virtual environment: `source venv/bin/activate`
4.  Run the FastAPI application:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
    Your backend will be accessible from your host machine at `http://localhost:8000`.

### 4.2. Frontend (Vue.js)

1.  SSH into your VM (if not already in a separate session): `vagrant ssh`
2.  Navigate to your frontend project directory: `cd /vagrant/frontend/<your-vue-project-name>`
3.  Run the Vue.js development server:
    ```bash
    npm run dev -- --host 0.0.0.0 --port 8080
    ```
    Your frontend will be accessible from your host machine at `http://localhost:8080`.

## 5. Google Cloud SDK (Optional, for local GCP interaction)

If you need to interact with GCP services directly from your VM (e.g., for local Firestore emulation), install the Google Cloud SDK.

1.  Add the Cloud SDK distribution URI as a package source:
    ```bash
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    sudo apt install apt-transport-https ca-certificates gnupg -y
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
    sudo apt update && sudo apt install google-cloud-sdk -y
    ```
2.  Initialize the SDK:
    ```bash
    gcloud init
    ```
    Follow the prompts to log in with your Google account and configure your project.

## 6. Shutting Down the VM

When you are done developing, you can shut down the VM from your host machine:

*   **Suspend (saves state):** `vagrant suspend`
*   **Halt (clean shutdown):** `vagrant halt`
*   **Destroy (deletes VM):** `vagrant destroy` (Use with caution, this removes all VM data)

This completes the local development environment setup.
