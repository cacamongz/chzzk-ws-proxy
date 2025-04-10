import asyncio
import websockets
import os

PORT = int(os.environ.get("PORT", 10000))  # Render가 포트를 환경변수로 넘겨줌
TARGET_WS = "wss://kr-ss.chzzk.naver.com"

async def handler(client_ws, _):
    async with websockets.connect(TARGET_WS) as server_ws:
        async def relay(src, dst):
            try:
                async for message in src:
                    await dst.send(message)
            except:
                pass

        await asyncio.gather(
            relay(client_ws, server_ws),
            relay(server_ws, client_ws)
        )

async def main():
    print(f"🔁 프록시 서버 시작됨 (포트 {PORT})")
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()

asyncio.run(main())
