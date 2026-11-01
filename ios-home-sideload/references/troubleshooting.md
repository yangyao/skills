# 故障定位

## USB 成功、Wi-Fi 找不到裝置

CoreDevice 能連 Wi-Fi 不代表 AltServer 的 legacy usbmux 清單正常。先證實：

```sh
idevice_id -n -l
idevicepair -n -u "$DEVICE_ID" validate
```

缺工具再評估 Homebrew libimobiledevice，不預設都要重裝。檢查手機解鎖、同網段、Finder Wi-Fi 顯示設定已套用。無線清單看到目標且 validate 成功，再讓使用者 Refresh All。

若 Bonjour／手機 62078 可達、Finder 正確、CoreDevice 可達，但 legacy 無線清單沒有目標，可能是 Mac 裝置服務快取。可先正常重啟 AltServer。

此次實際修復：經授權，使用者在 Mac Terminal 執行 `sudo /usr/bin/killall -TERM usbmuxd`；服務自動重啟，無線清單和 validate 恢復，再重啟 AltServer，拔線 Refresh All 通過。會使 iOS 裝置連線短暫重連，**不是每次續簽的例行步驟**。密碼由使用者自行輸入。

不繞 SIP，不停系統保護。沒有新證據不要重複要求重啟手機、切 Wi-Fi、重置配對或信任。

## 憑證與 App ID

「既有 signing certificate 不可用，已建立新憑證」與「AltServer 找不到裝置」不同。若已換憑證，先修連線再完成 Refresh Now／All，必要時重匯 LiveContainer 憑證。

簽名前盤點其他受影響手機、iPad、App；不擅自撤銷開發憑證。不要在 AltStore 與 Sideloadly 來回簽名碰運氣，或讀取 private auth session 來繞 UI。

ID 不足看 View App IDs 的實際 expiry，刪 App 不立即釋放。先核對主 ID 能否沿用，再等待或讓使用者選帳號；不默認付費或借證書。臨時裁切擴充要記錄缺失，餘額夠再同主 ID 覆蓋補回，資料不需重建。

## 入口與保存

- Safari 開啟確認：點的是 Web Clip／網頁入口，不是官方 Launch App。
- 找不到 Launch App：核對實際擴充、簽名後 ID、捷徑 descriptor。同版本號不代表含相同擴充。
- 要結束其他 guest：單容器仍有其他 App 執行，不是刪資料。多容器／多工另評估，不作預設加裝。
- JIT-less 錯誤：先看容器簽名、憑證匯入和診斷，勿先刪資料。
- 預設 glyph：直啟成功不代表自動配置 PNG，仍需一次手動選圖示。
