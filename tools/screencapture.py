import os
import asyncio
import base64
from pyppeteer import launch

class ScreenCapture():

    def capture(self, url):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self._capture(url))
        return result

    async def _capture(self, url):
        browser = await launch()
        page = await browser.newPage()
        await page.setViewport({'width':800, 'height':1200})
        await page.goto(url)
        await page.screenshot({'path': 'out.png'})
        await browser.close()
        with open('out.png', 'rb') as contents:
            b64 = base64.b64encode(contents.read())
        os.remove('out.png')
        return b64
