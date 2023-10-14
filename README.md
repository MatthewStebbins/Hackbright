<div align='center'>

<img src=https://github.com/MatthewStebbins/Hackbright/blob/socket/static/img/Main%20image.png alt="logo" width=854 height=480 />

<h1>Welcome to The Siren </h1>
<p>Welcome to The Siren is a multiple player web game where players take turns adding cards to the the Ship deck or choosing a piece of equipment. If a player does not think they can beat the ship they can pass. Whoever wins twice before losings twice wins overall.</p>

<h4> <span> · </span> <a href="https://github.com/MatthewStebbins/Hackbright/blob/master/README.md"> Documentation </a> <span> · </span> <a href="https://github.com/MatthewStebbins/Hackbright/issues"> Report Bug </a> <span> · </span> <a href="https://github.com/MatthewStebbins/Hackbright/issues"> Request Feature </a> </h4>


</div>

# :notebook_with_decorative_cover: Table of Contents

- [About the Project](#star2-about-the-project)
- [Acknowledgements](#gem-acknowledgements)


## :star2: About the Project
### :space_invader: Tech Stack
<details> <summary>Client</summary> <ul>
<li><a href="https://react.dev/">React</a></li>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/javascript">Javascript</a></li>
<li><a href="https://socket.io/">SocketIO</a></li>
<li><a href="https://jinja.palletsprojects.com/en/3.1.x/">Jinja</a></li>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/HTML">HTML </a></li>
<li><a href="https://developer.mozilla.org/en-US/docs/Web/CSS">CSS</a></li>
</ul> </details>
<details> <summary>Server</summary> <ul>
<li><a href="https://flask-socketio.readthedocs.io/en/latest/">Flask-SocketIO</a></li>
<li><a href="https://flask.palletsprojects.com/en/3.0.x/">Flask </a></li>
<li><a href="https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/">Flask-SQLAlchemy</a></li>
<li><a href="https://www.python.org/">Python</a></li>
</ul> </details>
<details> <summary>Database</summary> <ul>
<li><a href="https://www.postgresql.org/">PostgreSQL</a></li>
</ul> </details>

### :dart: Features
- Kanban of intended features: https://trello.com/b/NgxyOInN/the-siren

### :art: Color Reference
| Color | Hex |
| --------------- | ---------------------------------------------------------------- |
| Primary Color | ![#062c43](https://via.placeholder.com/10/062c43?text=+) #062c43 |
| Secondary Color | ![#5591a9](https://via.placeholder.com/10/5591a9?text=+) #5591a9 |
| Accent Color | ![#ffd700](https://via.placeholder.com/10/ffd700?text=+) #ffd700 |
| Text Color | ![#ced7e0](https://via.placeholder.com/10/ced7e0?text=+) #ced7e0 |

## :toolbox: Getting Started

### :bangbang: Prerequisites

- Run PowerShell as an Administrator
- Install WSL
```bash
wsl --install
```
- Launch Ubuntu from start
- In the Ubuntu program, type the following update and upgrade packages
```bash
sudo apt update && sudo apt upgrade
```
- Using WSL 2
```bash
sudo apt install -y build-essential software-properties-common python3-pip python3-venv python3-dev
```
- Upgrade Python
```bash
sudo apt install -y
```

```bash
sudo add-apt-repository -y ppa:deadsnakes/ppa
```

```bash
sudo apt update
```

```bash
sudo apt install -y python3.9 python3.9-dev python3.9-distutils
```
- Install Python development tools: virtualenv
```bash
python3.9 -m pip install virtualenv ipython
```

```bash
ln -s $(which python3.9) ~/.local/bin/python3
```
- Install Node.js
```bash
sudo apt install -y nodejs
```
- Install PostgreSQL
```bash
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
```

```bash
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
```

```bash
sudo apt update
```

```bash
sudo apt install -y postgresql-13 postgresql-client-13 postgresql-server-dev-13 libpq-dev
```
- Set up PostgreSQL
```bash
sudo pg_ctlcluster 13 main start
```

```bash
sudo -u postgres psql --command "CREATE USER $(whoami) WITH SUPERUSER;"
```

```bash
createdb $(whoami)
```
- Clone or download repository from GitHub
```bash
gh repo clone MatthewStebbins/Hackbright
```


## :gem: Acknowledgements

Use this section to mention useful resources and libraries that you have used in your projects.

- [Thank you to Hackbright for starting this project](https://hackbrightacademy.com/)