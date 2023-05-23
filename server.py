import asyncio
import websockets

connections = {}

async def handle_client(websocket, path):
    try:
        # Store the connection in the dictionary
        connections[id(websocket)] = websocket

        while True:
            message = await websocket.recv()
            print(f"Received message from client: {message}")

            # Process the received message here
            # ...

            response = "Server processed the message"
            await websocket.send(response)
            print(f"Sent response to client: {response}")

            # Write the received message and response to files
            with open("received_messages.txt", "a") as received_file:
                received_file.write(message + "\n")
            with open("sent_responses.txt", "a") as response_file:
                response_file.write(response + "\n")

    except websockets.exceptions.ConnectionClosedOK:
        print("Client connection closed.")
        # Remove the connection from the dictionary
        del connections[id(websocket)]

async def start_server():
    server = await websockets.serve(handle_client, 'localhost', 8765)
    print("Server started.")
    await server.wait_closed()

asyncio.run(start_server())
