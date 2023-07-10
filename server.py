import asyncio
import websockets
import signal
import os

# Mapping of WebSocket connections to camera IDs
connections = {}

# Mapping of camera IDs to WebSocket connections (for grouping related data)
camera_mapping = {}

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

                # Update the mapping with the camera_id and the WebSocket connection
                if camera_id in camera_mapping:
                    camera_mapping[camera_id].add(websocket)
                else:
                    camera_mapping[camera_id] = {websocket}

            elif message == "CLOSE":
                await close_connection(websocket)
                break

            else:
                # Process the received message (image data) and camera_id here
                camera_id = connections.get(websocket, -1)
                if camera_id != -1:
                    # Save the received image as a base64 string to a file
                    filename = f"image_{camera_id}.txt"  # Example filename
                    folder_path = "received_images"

                    # Create the folder if it doesn't exist
                    os.makedirs(folder_path, exist_ok=True)

                    file_path = os.path.join(folder_path, filename)

                    with open(file_path, "w") as file:
                        file.write(message)

                    # Send a confirmation response to the client
                    response = f"Received image '{filename}'"
                    await websocket.send(response)
                    print(f"Sent response to client {websocket.remote_address}: {response}")
                else:
                    print(f"Client {websocket.remote_address} has not set a camera_id")

    except websockets.exceptions.ConnectionClosedOK:
        print(f"Client connection closed: {websocket.remote_address}")
        await close_connection(websocket)

async def close_connection(websocket):
    # Remove the connection from the dictionary and close the WebSocket connection
    if websocket in connections:
        del connections[websocket]

    # Remove the connection from the mapping
    camera_id = connections.get(websocket, -1)
    if camera_id in camera_mapping:
        camera_mapping[camera_id].discard(websocket)
        if len(camera_mapping[camera_id]) == 0:
            del camera_mapping[camera_id]

    await websocket.close()
    print(f"Closed connection with client {websocket.remote_address}")

async def start_server():
    server = await websockets.serve(handle_client, 'localhost', 8765)
    print("Server started.")
    await server.wait_closed()

def handle_exit(signal, frame):
    print("Exiting server...")
    exit(0)

signal.signal(signal.SIGINT, handle_exit)
asyncio.run(start_server())
