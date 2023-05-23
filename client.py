import asyncio
import websockets

async def send_message():
    async with websockets.connect('ws://localhost:8765/') as websocket:
        camera_id = int(input("Enter the camera_id you are looking at (or -1 if not set): "))
        await websocket.send(f"SET_CAMERA:{camera_id}")
        print(f"Sent camera_id to server: {camera_id}")

        while True:
            message = input("Enter 'q' to quit or press Enter to send an image: ")
            if message == "q":
                await websocket.send("CLOSE")
                print("Closed connection.")
                break

            # Replace this part with your actual image capture code
            image_data = "Image data"
            await websocket.send(image_data)
            print(f"Sent image to server")

            response = await websocket.recv()
            print(f"Received response from server: {response}")

async def start_client():
    await send_message()

asyncio.run(start_client())
