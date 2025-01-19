from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Khởi động trình duyệt
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Mở trang web
driver.get('https://xoso.com.vn/quay-thu-xsmb.html')

# Chờ một chút để trang tải
time.sleep(3)  # Chờ 3 giây

# Tìm kiếm kết quả quay thử
results = driver.find_elements(By.CLASS_NAME, 'result')  # Thay đổi class theo cấu trúc thực tế

# In kết quả
for result in results:
    numbers = result.find_elements(By.CLASS_NAME, 'number')
    date = result.find_element(By.CLASS_NAME, 'date')
    print(f"Ngày: {date.text.strip()}")
    for number in numbers:
        print(f"Kết quả: {number.text.strip()}")

# Đóng trình duyệt
driver.quit()
