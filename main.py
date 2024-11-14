from selenium import webdriver
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from selenium import webdriver
from io import BytesIO
from PIL import Image


app = FastAPI()

class ScreenshotRequest(BaseModel):
    url: str


def get_selenium_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    return webdriver.Chrome(options=chrome_options)  


def take_full_page_screenshot(url: str) -> BytesIO:
    driver = get_selenium_driver()
    driver.get(url)
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, total_height)
    screenshot = driver.get_screenshot_as_png()
    driver.quit()
    img = Image.open(BytesIO(screenshot))
    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    
    return output

@app.post("/screenshot")
async def screenshot_endpoint(request: ScreenshotRequest):
    try:
        screenshot = take_full_page_screenshot(request.url)
        return StreamingResponse(screenshot, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to capture screenshot: {str(e)}")