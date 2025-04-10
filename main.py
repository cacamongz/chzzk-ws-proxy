import asyncio
import websockets

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
    print("🔁 프록시 서버 시작됨 (포트 443)")
    async with websockets.serve(handler, "0.0.0.0", 443):
        await asyncio.Future()  # 무한 대기

asyncio.run(main())
