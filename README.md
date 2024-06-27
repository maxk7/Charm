# Charm

Local, customized [Hydra Visualizer](https://hydra.ojack.xyz/?sketch_id=celeste_2) for reactive art and live music visualization

#### Security Warnings

This project is currently under active development. During this phase, the client application **executes JavaScript code received from the local backend server without strict validation.** This practice, while expedient for development, introduces significant security risks. Users are strongly advised to run Charm only if they are fully aware of and accept the inherent security vulnerabilities associated with this temporary design. Proceed with caution and ensure appropriate safeguards are in place.

# Application Design

Charm is an Electron-based application designed to render and interact with Hydra code in real-time via a unique Python-Textual user interface. The communication bridge between the Electron front-end and the user interface is efficiently managed through a Python-Flask backend server, ensuring seamless integration and performance. The application design will be broken down into the following sections:

- Server (Python-Flask)
- Client
  - Visualizer (Electron)
  - GUI (Python-Textual)
    - modules

## Server

The Python-Flask server self-contained within `/server/main.py` and listens to post requests from the client gui on the `/run-js` URL. Incoming messages include hydra code and other javascript commands and are sent to the client visualizer through socket emit. 

## Client

### Visualizer

### GUI

#### Modules
