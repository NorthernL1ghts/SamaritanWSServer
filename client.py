import asyncio
import websockets
import signal
import cv2
import base64

async def send_message():
    async with websockets.connect('ws://localhost:8765') as websocket:
        message = input("Enter a message to send: ")
        await websocket.send(message)
        print(f"Sent message to server: {message}")

        camera_id = int(input("Enter the camera_id you are looking at (or -1 if not set): "))
        await websocket.send(f"SET_CAMERA:{camera_id}")
        print(f"Sent camera_id to server: {camera_id}")

        # Save sent message to sent_messages.txt
        with open("sent_messages.txt", "a") as file:
            file.write(message + "\n")

        while True:
            message = input("Enter 'q' to quit or press Enter to send an image: ")
            if message == "q":
                await websocket.send("CLOSE")
                print("Closed connection.")
                break

            # Read image from file
            image_path = input("Enter the path of the image file: ")
            try:
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
            except FileNotFoundError:
                print("File not found. Please try again.")
                continue

            # Encode image data as base64 string
            image_base64 = base64.b64encode(image_data).decode("utf-8")

            await websocket.send(image_base64)
            print(f"Sent image to server")

            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                print(f"Received response from server: {response}")

                # Save received response to file
                with open("received_responses.txt", "a") as file:
                    file.write(response + "\n")

                with open("sent_responses.txt", "a") as file:
                    file.write(response + "\n")

            except asyncio.TimeoutError:
                print("Timeout: No response received from the server.")

async def start_client():
    await send_message()

def handle_exit(signal, frame):
    print("Exiting client...")
    exit(0)

# Register the signal handler for handling SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, handle_exit)

# Run the client
asyncio.run(start_client())
