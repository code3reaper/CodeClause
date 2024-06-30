import asyncio
import websockets

connected_clients = set()

async def chat_handler(websocket, path):
    # Register client
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast incoming message to all connected clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    finally:
        # Unregister client
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(chat_handler, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
