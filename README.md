# SamaritanWSServer - WebSocket Server-Client Communication

![Logo](Logo.png) <!-- Replace with the actual path to your logo image -->

This project implements a simple WebSocket server-client communication using Python that I will later use for Samaritan. The server and client scripts allow exchanging messages and sending images between them.

## Features
- Establishes a WebSocket connection between the server and client.
- Sends and receives text messages between the server and client.
- Sets a camera ID on the client side and sends it to the server.
- Sends image data from the client to the server.
- Performs image processing or prediction based on the camera ID on the server side.
- Saves sent and received messages to separate text files.
- Saves received images as base64 strings to files.
- Gracefully handles termination of the client and server.

## Requirements
- Python 3.6 or higher
- websockets package

## Usage
1. Start the WebSocket server by running `server.py`.
2. Run `client.py` to establish a WebSocket connection with the server.
3. Enter messages or image paths as prompted in the client console.
4. Messages and responses will be displayed in the console and saved to separate text files.
5. The server will process the received image data and send a response back to the client.

## File Descriptions
- `server.py`: Contains the WebSocket server code.
- `client.py`: Contains the WebSocket client code.
- `sent_messages.txt`: A text file that records all messages sent from the client.
- `received_messages.txt`: A text file that records all messages received by the server.
- `sent_responses.txt`: A text file that records all responses sent by the server.
- `received_responses.txt`: A text file that records all responses received by the client.

## Customize
Feel free to modify the code to suit your specific requirements. You can extend the functionality, handle additional events, or integrate with other systems.

## License
This project is licensed under the [MIT License](LICENSE).
