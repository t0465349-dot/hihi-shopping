import os
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 📈 1. 基礎路徑直接對齊終點
SCAN_HTML_PATH = r"D:\GitHub\hihi-shopping\scan.html"
IMAGES_DIR = r"D:\GitHub\hihi-shopping\images"
TARGET_DIR = r"D:\GitHub\hihi-shopping"
TARGET_FILE_PATH = os.path.join(TARGET_DIR, "img_data.js")

# 🛑 關鍵心法：先斬後奏！如果目標資料夾已有舊的索引檔，先刪掉它
# 這樣 Edge 下載新檔時，才會直接命名為 img_data.js，不會變成 img_data (1).js
if os.path.exists(TARGET_FILE_PATH):
    print("🗑️ 偵測到舊的索引檔，正在執行預先刪除...")
    os.remove(TARGET_FILE_PATH)

print("🚀 正在啟動 Edge 瀏覽器並將下載路徑直接鎖定專案目錄...")

# ⚙️ 2. 設定 Edge 瀏覽器參數（下載點直接設為終點資料夾）
edge_options = Options()
edge_prefs = {
    "download.default_directory": TARGET_DIR,          # 💡 直接下放到 D:\GitHub\hihi-shopping
    "download.prompt_for_download": False,            # 不跳出另存新檔視窗
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False,                    # 關閉網頁安全防護
    "safebrowsing.disable_download_protection": True  # 徹底關閉「可能危害您的裝置」下載阻攔
}
edge_options.add_experimental_option("prefs", edge_prefs)
edge_options.add_argument("--safebrowsing-disable-download-protection")

# 啟動瀏覽器
driver = webdriver.Edge(options=edge_options)
driver.maximize_window()

try:
    # 🌐 3. 打開本地的 scan.html
    print(f"📂 正在開啟網頁：{SCAN_HTML_PATH}")
    driver.get(f"file:///{SCAN_HTML_PATH}")
    
    # ⏳ 4. 等待網頁按鈕載入完成
    wait = WebDriverWait(driver, 15)
    
    # 自動選定 images 資料夾並整批上傳
    print("📸 正在自動選定 images 資料夾並整批上傳...")
    folder_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
    folder_input.send_keys(IMAGES_DIR)
    
    # 等待掃描完成，直到「下載 img_data.js」的藍色按鈕現身
    print("⏳ 正在等待系統掃描圖片並產生索引...（請稍候）")
    download_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., '下載 img_data.js')]")))
    
    # 💾 5. 點擊下載（直接落入 D:\GitHub\hihi-shopping）
    print("💾 掃描成功！正在直接下載至專案目錄...")
    download_btn.click()
    
    # ⏳ 6. 監控下載狀態
    downloaded = False
    for _ in range(30):  # 最多等待 30 秒
        if os.path.exists(TARGET_FILE_PATH) and os.path.getsize(TARGET_FILE_PATH) > 0:
            downloaded = True
            break
        time.sleep(1)
        
    if downloaded:
        print("🏆 【自動化結帳成功】！新索引檔已直接覆蓋進 D 槽專案目錄，大功告成！")
    else:
        print("❌ 下載好像出了點問題，沒能在專案目錄看到新檔案。")
        
finally:
    # 關閉瀏覽器
    driver.quit()