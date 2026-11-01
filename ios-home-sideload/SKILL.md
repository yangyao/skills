---
name: ios-home-sideload
description: Set up or maintain self-developed iPhone/iPad apps using AltStore Classic, a Mac running AltServer, LiveContainer, preserved app data, and native Launch App shortcuts. Use for a replacement phone, adding an IPA, fixing home Wi-Fi refresh, or preparing Home Screen launchers.
---

# 家庭 iOS App 安裝、續簽與直啟

使用者選擇：免費 Apple 帳號、自己的 Mac + 家庭 Wi-Fi、不使用手機 VPN；接受手機手動刷新與第一次電腦配對。這是第三方軟體配合自己的 Apple 開發簽名，不是購買第三方簽名服務。若使用者提出不同偏好，以新指示為準。

## 選擇路徑

- **換手機／第一次設定**：讀 [setup.md](references/setup.md)。AltStore Classic + AltServer + LiveContainer；優先保留官方啟動擴充。
- **加 App／搬資料**：讀 [apps-and-data.md](references/apps-and-data.md)。先備份，區分原生 App 與 guest 的資料；積分同步不代表全部進度已搬好。
- **桌面入口**：讀 [shortcuts.md](references/shortcuts.md)。使用官方 `Launch App` AppIntent，避免 Safari URL 或 Web Clip 入口。先產生一個測試，成功再批量。
- **Wi-Fi 刷新／簽名錯誤**：讀 [troubleshooting.md](references/troubleshooting.md)。先證實 legacy usbmux 無線發現正常，再讓使用者重試。

## 工作原則

1. 先盤點目標裝置、實際 Bundle ID、App ID 餘額、續簽工具與存檔。不要把舊手機的 UDID、容器 UUID 或簽名後 ID 當成新手機的值。
2. 同主 Bundle ID **覆蓋更新**，不要先刪 LiveContainer。先備份 guest 資料和映射；刪容器可能一併刪掉全部 guest 存檔。
3. 不自行撤銷憑證、刪 App、清 Keychain、重置配對或停掉其他續簽服務。只有既有授權涵蓋該影響才做。避免多個工具交替替換簽名憑證。
4. Apple 密碼、2FA、解鎖碼和管理員密碼由使用者在工具／系統畫面輸入，不收集到對話。不得把私鑰、配對記錄或登入資料變成公開資源。
5. Agent 完成準備、備份、編譯、傳檔與核對；手機信任、權限和最後安裝確認由使用者做。每次只交接具體必要步驟，不重做已成功項目。
6. SDK build ≠ 手機執行；USB 成功 ≠ Wi-Fi 成功；新增圖示 ≠ 官方直啟。精確描述已驗證與待驗證狀態，不承諾不存在的一鍵功能。

## 真實限制

- 免費簽名有效期、每台啟用 App 數、帳號 App ID 註冊額度是不同限制。擴充也可能占 ID；不是每週只能點十次刷新。看 AltStore `View App IDs`，不猜週一重置或目前餘額。
- guest 不各自向 Apple 註冊 App ID；容器與擴充仍需簽名。依當次官方版本核對相依擴充，不要先刪光再承諾所有功能可用。
- `Launch App` 可省去 Safari，但單容器切換 guest 仍可能提示結束目前 App。多容器／多工不是此次預設需求。
- **無已驗證的全自動原圖示桌面安裝流程**。官方捷徑仍需使用者選圖示並確認加入主畫面。Web Clip 設定檔可批量放圖示，卻引入瀏覽器跳轉，不作預設推薦。
- 續簽需 Apple 服務及可到達的 AltServer；App 的離線保存／跨裝置同步取決於 App 本身。

## 完成標準

目標 guest 完成首次清單啟動、存檔核對正常、Finder Wi-Fi 設定讀回已啟用、拔 USB 後 Refresh All 成功、刷新後資料保留，桌面捷徑實測使用官方 Launch App，並提供清楚名稱與原圖下載。未驗證部分明確列出，不用另一台裝置的成功代替目標驗證。AltStore 下載逾時先走官方 IPA 本地安裝分支，不重跑全部設定。

## 公開邊界

只保存通用流程、原始碼和公開參考。實際設備清單、設定 JSON、存檔、IPA、圖示、家庭服務 token、簽名與配對資料放在倉庫外。不要為家庭工具加入未要求的 CI、GitHub Actions 或發佈流程。
