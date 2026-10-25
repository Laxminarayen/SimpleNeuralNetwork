# Salary Predictor — a simple neural network served with Flask

A tiny PyTorch neural network that predicts salary from years of experience,
served as a web app and deployable to a GCP Compute Engine VM.

```
train.ipynb   ->  trains the network, saves salary_net.pth
model.py      ->  the network definition (shared by notebook + app)
app.py        ->  Flask web app that loads the model and predicts
deploy/       ->  files to run it on a GCP VM
```

## Run it on your own computer

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

jupyter notebook train.ipynb      # run all cells -> creates salary_net.pth
python app.py                     # open http://localhost:8080
```

## API

```bash
curl -X POST http://localhost:8080/api/predict \
     -H 'Content-Type: application/json' \
     -d '{"experience": 5}'
# -> {"experience": 5, "salary": 65000}
```

## Deploy to a GCP Compute Engine VM

1. Create an **e2-small** VM (Debian/Ubuntu) and allow HTTP traffic.
2. Add a firewall rule allowing **TCP 8080** (or put it behind a load balancer).
3. SSH into the VM, clone this repo from GitHub, and run the setup script:

```bash
sudo apt-get update && sudo apt-get install -y git
git clone https://github.com/Laxminarayen/SimpleNeuralNetwork.git
cd SimpleNeuralNetwork
sudo bash deploy/startup.sh
```

To update later: `cd SimpleNeuralNetwork && git pull && sudo bash deploy/startup.sh`

The app runs as a **systemd service** (`salarynet`) via **gunicorn**, so it
restarts automatically if it crashes or the VM reboots.

```bash
sudo systemctl status salarynet    # check it
sudo journalctl -u salarynet -f    # watch logs
```

Visit `http://YOUR_VM_EXTERNAL_IP:8080`.

See **SalaryNet_Teaching_Guide.pdf** for the full classroom walkthrough.
