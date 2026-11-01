# 故障定位

## AltStore 下載逾時

`AltStore could not be downloaded. The request timed out.` 指向 Mac 下載官方安裝檔失敗，與配對錯誤、裝置找不到、App ID 不足不同。不要因此重裝全部工具、切換簽名器或撤銷憑證。

已驗證的替代流程：

1. Mac 取得官方來源清單 `https://cdn.altstore.io/file/altstore/apps.json`（AltServer 的來源入口也可能是 `https://apps.altstore.io`）。篩選正式版 `com.rileytestut.AltStore`，按目標 OS 選相容版本，讀取該版 `downloadURL`、`size`、`sha256`；不從第三方 IPA 站下載，不將此例的版本或 hash 永久寫死。
2. 用工具下載官方 IPA 到倉庫外。HTTP 200 的來源清單不代表大檔能在 AltServer 內建時限內完成；慢速時用 `curl -C -` 斷點續傳，先確認伺服器支援 Range。保持同一個版本與 URL，若來源改版或無法續傳，另開新檔，不把不同檔案拼接。
3. 若使用者已設定本機代理，可在不改全域設定的情況下使用已確認的代理位址；不硬編碼連接埠、不擅自開關其 VPN。避免多條重複下載互相爭帶寬，完成後停止自己啟動的重複工作。
4. **比對官方大小和 SHA-256、驗證 ZIP、主 Bundle ID 和版本後**，才標示可安裝。未完成的 partial 檔不能讓使用者選取；已驗證檔放在容易找到的下載目錄，取清楚檔名。
5. 關閉錯誤視窗，Mac **按住 Option 點 AltServer → Sideload .ipa… → 正確裝置**，選本地 IPA，同帳號登入。此入口已在第二台手機和平板成功安裝 AltStore；不必重設配對或改用另一個簽名器。
6. 安裝後用裝置 App inventory 核對 AltStore 的實際 ID／版本；之後沿用該官方檔案設定其他裝置，只有相容性／版本需求改變才重抓。不要把安裝包、實際帳號或校驗紀錄放進公開 skill。

若原生 UI 只有選單列入口且控制工具無法取得，請使用者完成具體的選單選擇；不要反覆呼叫同一個會逾時的 UI handle。

## USB 成功、Wi-Fi 找不到裝置

CoreDevice 能連 Wi-Fi 不代表 AltServer 的 legacy usbmux 清單正常。先證實：

```sh
idevice_id -n -l
idevicepair -n -u "$DEVICE_ID" validate
```

缺工具再評估 Homebrew libimobiledevice，不預設都要重裝。檢查手機解鎖、同網段、Finder Wi-Fi 顯示設定已套用。若未啟用，勾選再 Apply；USB 下讀回 `EnableWifiConnections=true`，確認清單出現 `(Network)` 並無線 validate 成功，才請使用者拔線 Refresh All。**清單中只有 `(USB)` 不算無線可用。**

平板實際案例：使用者已完成 App 設定，但 Finder 的 Show this iPad when on Wi-Fi 仍是未勾。勾選並套用後，讀回 true、Network 與 validate 恢復，拔線刷新成功；不需要重啟 usbmuxd。因此先核對選項，不要直接套用手機曾經需要的系統服務重啟。

若 Bonjour／手機 62078 可達、Finder 正確、CoreDevice 可達，但 legacy 無線清單沒有目標，可能是 Mac 裝置服務快取。可先正常重啟 AltServer。

此次實際修復：經授權，使用者在 Mac Terminal 執行 `sudo /usr/bin/killall -TERM usbmuxd`；服務自動重啟，無線清單和 validate 恢復，再重啟 AltServer，拔線 Refresh All 通過。會使 iOS 裝置連線短暫重連，**不是每次續簽的例行步驟**。密碼由使用者自行輸入。

不繞 SIP，不停系統保護。沒有新證據不要重複要求重啟手機、切 Wi-Fi、重置配對或信任。

## 憑證與 App ID

「既有 signing certificate 不可用，已建立新憑證」與「AltServer 找不到裝置」不同。若已換憑證，先修連線再完成 Refresh Now／All，必要時重匯 LiveContainer 憑證。

簽名前盤點其他受影響手機、iPad、App；不擅自撤銷開發憑證。不要在 AltStore 與 Sideloadly 來回簽名碰運氣，或讀取 private auth session 來繞 UI。

ID 不足看 View App IDs 的實際 expiry，刪 App 不立即釋放。先核對主 ID 能否沿用，再等待或讓使用者選帳號；不默認付費或借證書。臨時裁切擴充要記錄缺失，餘額夠再同主 ID 覆蓋補回，資料不需重建。

**0 App IDs remaining 不等於不能設定另一台裝置。** 同帳號、相同主 App 和擴充 Bundle ID 可重用已註冊 ID；此次平板在餘額 0 時成功沿用同一套 AltStore／LiveContainer／擴充。不為了新手機改 Bundle ID，否則可能轉成需新註冊。這不保證任意新 App／新擴充都可裝，也不排除其他裝置數量或簽名限制。參考 [AltStore 的重用邏輯](https://github.com/altstoreio/AltStore/blob/main/AltStore/Operations/FetchProvisioningProfilesOperation.swift)。

## 入口與保存

- Safari 開啟確認：點的是 Web Clip／網頁入口，不是官方 Launch App。
- 找不到 Launch App：核對實際擴充、簽名後 ID、捷徑 descriptor。同版本號不代表含相同擴充。
- 要結束其他 guest：單容器仍有其他 App 執行，不是刪資料。多容器／多工另評估，不作預設加裝。
- JIT-less 錯誤：先看容器簽名、憑證匯入和診斷，勿先刪資料。
- 預設 glyph：直啟成功不代表自動配置 PNG，仍需一次手動選圖示。
- guest 首次直啟閃退、LCAppInfo 尚無資料容器：先在 LiveContainer 清單正常開啟一次，再讀映射產生捷徑。此次遙控器在首次清單啟動後恢復，但未取得崩潰報告，不能把初始化順序視為所有閃退的確定原因；若清單啟動也失敗，改查該 App 的崩潰資料。
