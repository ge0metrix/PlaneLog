from codecs import StreamReader, StreamWriter
import asyncio
import time

class tarConn():
    host:str
    port:int
    reader:StreamReader
    writer:StreamWriter
    tail:str

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.nextReconnect = time.time()
        self.reconnectInterval = 5
        self.tail = ""
    
    async def connect(self):
        try:
            if self.writer:
                print(f'disconnecting {self.host}:{self.port}')
                self.writer.close()
                await self.writer.wait_closed()
                self.reader = None
                self.writer = None
            
            now = time.time()
            if now > self.nextReconnect:
                self.nextReconnect = now + self.reconnectInterval
                print(f'trying {self.host}:{self.port}')
                self.reader, self.writer = await asyncio.wait_for(asyncio.open_connection(self.host, self.port), self.reconnectInterval)
                print(f'connected {self.host}:{self.port}')

        except Exception as e:
            pass

    async def readlines(self) -> list[str]:
        if not self.writer or self.writer.is_closing():
            await self.connect()
            if not self.writer or self.writer.is_closing():
                return "closed"
        read = await self.reader.read(64*1024)
        #print(read.decode())
        lines = (self.tail + read.decode()).split('\n')
        self.tail = lines[-1]
        #print(f'read {len(lines) - 1} lines')
        return lines[:-1]