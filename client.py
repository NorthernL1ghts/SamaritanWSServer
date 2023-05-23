import asyncio
import websockets

async def send_message():
    async with websockets.connect('ws://localhost:8765/') as websocket:
        while True:
            message = input("Enter a message to send (or 'q' to quit): ")
            if message == "q":
                break
            await websocket.send(message)
            print(f"Sent message to server: {message}")

            response = await websocket.recv()
            print(f"Received response from server: {response}")

            # Write the sent message and received response to files
            with open("sent_messages.txt", "a") as sent_file:
                sent_file.write(message + "\n")
            with open("received_responses.txt", "a") as response_file:
                response_file.write(response + "\n")

async def start_client():
    await send_message()

asyncio.run(start_client())
