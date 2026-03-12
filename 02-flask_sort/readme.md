# Higher or Lower - Flask Game

A simple web game built with Flask where the player has to guess a random number between 0 and 9.

## How it works

When the server starts, a random number is generated.  
The player guesses the number by typing it in the URL.

Example:
![Game Demo](static/gifs/how_to_play.gif)

- **Too high** → if the guess is greater than the number
- **Too low** → if the guess is smaller than the number
- **You got it!** → if the guess is correct

Each response shows a colored message and a GIF.

## Technologies

- Python
- Flask

## Project structure
```
higher-lower/
│
├── server.py
├── static/
│   └── gifs/
│       └── how_to_play.gif
└── README.md
```

## Running the project

1. Install Flask

pip install flask

2. Run the server

python server.py

3. Open your browser

http://127.0.0.1:5000

## Learning purpose

This project was created to practice:

- Flask routing
- Dynamic URLs
- Basic HTML responses
- Static files in Flask