# Robots.txt: Grad Project (Allyson Lee)

## Description
Robots.txt is an interactive experience that visualises the Dead Internet Theory. This project illustrates the discrepancy between humans and bots, and the lasting negative impact bots — and artificial intelligence as a whole — is having on the internet. <br>
It utilises Python to create the visual interface and ArduinoIDE to control the thermal printers.

## Getting Started
### Prerequisites
1. **Install Ollama Program** <br>

    First you will need to install Ollama onto your computer. Instructions for your operating system can be found on [this website](https://medium.com/@jonigl/getting-started-with-ollama-run-llms-on-your-computer-915ba084918c). 
    
    <br>

2. **Install requirements.txt**
    ```
    pip install -r requirements.txt
    ```

    <br>

3. **Install Ollama Model**
    ```
    ollama pull llama3.2:1b
    ```

<br>

### Arduino–Thermal Printer Aspect
For this project, the thermal printers used are manufactured by Adafruit. Therefore, the code is written for their specific printers. <br>
The Adafruit Thermal Printer library install and circuit is detail on the [Adafruit website](https://learn.adafruit.com/mini-thermal-receipt-printer/microcontroller). <br>

This project requires two separate Arduino–Thermal Printer circuits to be set up. Additionally, the Arduino serial port will need to be changed to your personal Arduinos' port in both human.py and bot.py.


### Launching the Project
To launch the project, run launcher.py in your respective command line.
```
python3 launcher.py
```
**Note:** If you would like to run the program without the Arduino–thermal printer aspect, please comment out lines: 62–65, 126 in human.py & 44–47, 194 in bot.py.