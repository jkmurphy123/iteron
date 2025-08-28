# iteron
A simulated ASCII window application

retro_panels/
│── main.py
│── config.json
│── panels/
│    ├── __init__.py
│    └── panel.py


# 1) Create & activate a venv (example)
cd projects
python3 -m venv llm_env
source llm_env/bin/activate  
cd iteron

# 2) Install deps
pip install -r requirements.txt

# 3) Launch
python main.py