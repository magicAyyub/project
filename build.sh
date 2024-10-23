cd backend && \
# if docker and docker-compose are not installed, install them
if ! [ -x "$(command -v docker)" ]; then
    sudo apt-get update && \
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && \
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    sudo apt-get update && \
    sudo apt-get install -y docker-ce && \
    sudo usermod -aG docker ${USER} && \
    sudo systemctl enable docker && \
    sudo systemctl start docker
fi && \
sudo docker-compose up --build -d && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
cd .. && \
cd frontend && \
npm install && \
npm run build && \
cd .. && \