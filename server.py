import asyncio
import websockets

connections = {}

async def handle_client(websocket, path):
    try:
        # Store the connection in the dictionary with default camera_id -1
        connections[websocket] = -1

        while True:
            message = await websocket.recv()
            print(f"Received message from client: {message}")

            if message.startswith("SET_CAMERA"):
                # Parse the camera_id from the message
                camera_id = int(message.split(":")[1])

                # Update the camera_id for the specific client connection
                connections[websocket] = camera_id
                print(f"Client {websocket.remote_address} set camera_id to {camera_id}")
            elif message == "CLOSE":
                # Remove the connection from the dictionary and close the WebSocket connection
                del connections[websocket]
                await websocket.close()
                print(f"Closed connection with client {websocket.remote_address}")
            else:
                # Process the received message (image data) and camera_id here
                camera_id = connections[websocket]
                if camera_id != -1:
                    # Perform image prediction/detection based on the camera_id
                    # ...

                    response = "Server processed the image"
                    await websocket.send(response)
                    print(f"Sent response to client {websocket.remote_address}: {response}")
                else:
                    print(f"Client {websocket.remote_address} has not set a camera_id")

    except websockets.exceptions.ConnectionClosedOK:
        print(f"Client connection closed: {websocket.remote_address}")
        # Remove the connection from the dictionary
        del connections[websocket]

async def start_server():
    server = await websockets.serve(handle_client, 'localhost', 8765)
    print("Server started.")
    await server.wait_closed()

asyncio.run(start_server())
