import asyncio
import os
import time

WORKINGDIR = os.path.dirname(os.path.realpath(__file__))

events = {}
ports = {}
processes = {}
pid = 0 

def consume(data):
    parts = data.partition(b' ')
    return parts[0].decode(), parts[2]

async def handle_request(reader, writer):
    global pid
    read = await reader.read(1024)
    method, arg = consume(read)

    if method.upper() == 'START':
        pid += 1
        paths = arg.decode().split(" ")
        events[pid] = asyncio.Event()
        cmd = f'python {os.path.join(WORKINGDIR, *paths)} {pid}'
        process = await asyncio.create_subprocess_shell(cmd)
        await events[pid].wait()
        processes[ports[pid]] = process
        writer.write(f"{ports[pid]}".encode())
        await writer.drain()
    elif method.upper() == 'STOP':
        pid_ = int(arg)
        processes[pid_].terminate()
        await processes[pid_].wait()
        writer.write(b' ')
        await writer.drain()
    elif method.upper() == 'PORT':
        split = arg.split(b" ")
        pid_ = int(split[0])
        port_ = int(split[1])
        ports[pid_] = port_
        writer.write(b' ')
        await writer.drain()
        events[pid_].set()

async def main():
    server = await asyncio.start_server(handle_request, '0.0.0.0', 42922)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main(), debug=False)
