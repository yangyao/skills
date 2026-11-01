# 第一次設定或換手機

## 正確產品與既有狀態

用官方 Mac AltServer、手機 AltStore **Classic**、官方 LiveContainer。Classic 由 AltServer 安裝，**不要讓使用者去 App Store 搜尋**，也不要混成區域限定的 PAL。確認目前系統與版本相容性。

先盤點既有安裝、裝置配對和登入。已有 AltServer 就沿用，不為新 guest 重做整套流程。若有 Sideloadly 等自動續簽，先確認憑證衝突與影響，依授權調整服務；不讀私鑰／token 儲存。

## 初次操作

1. 目標手機 USB 接 Mac、解鎖、信任。Finder「一般」啟用連 Wi-Fi 時顯示裝置並套用；不要按還原或不必要的媒體同步。
2. AltServer 選單列選正確手機安裝 AltStore。對照 UDID／型號，不靠名字猜。Apple 登入和2FA 由使用者輸入。
3. 手機依需求開開發者模式、信任開發者及本機網路權限，開 AltStore 登入同帳號。
4. 看 My Apps → View App IDs 的實際餘額，計入主容器與所需擴充。刪 App 不會立即歸還 ID。
5. AltStore `＋` 匯入 LiveContainer，保留啟動擴充。此次驗證的 3.8.0，Launch App 需要 `LaunchAppExtension` + `ShareExtension`；較新文件的命名可能不同，依包內 metadata／源碼確認。額度不足時再評估裁切，明說失去的功能。
6. LiveContainer Settings 匯入 AltStore 憑證，JIT-Less Diagnose/Test 通過；密碼只在裝置填。後續真的換憑證時才視需要重匯。
7. 用無敏感資料的測試 IPA 檢查 guest 執行、計數保存及重開，再搬正式 App。

只缺擴充時，使用同主 Bundle ID 在 AltStore 覆蓋更新、Keep App Extensions；不卸載 LiveContainer。不同主 ID 是另一個 App，不是覆蓋。

## 傳檔與刷新

```sh
xcrun devicectl device info apps --device "$DEVICE_ID" --timeout 15
xcrun devicectl device copy to --device "$DEVICE_ID" \
  --domain-type appDataContainer --domain-identifier "$LC_BUNDLE_ID" \
  --source "$IPA_PATH" --destination Documents/NewApp.ipa --timeout 30
```

guest 在 LiveContainer Apps `＋ → 我的 iPhone → LiveContainer` 匯入；容器本身才用 AltStore `＋`。此次 LiveContainer Documents 可在 Files 看見，AltStore Documents 不可見，勿反覆用失敗的傳檔路徑。

手機不能訪問 GitHub 時，Mac 先下載，從只含公開下載檔的獨立目錄開臨時區網 HTTP 服務。不要服務專案根目錄或含家庭設定的 IPA 目錄。確認 HTTP200，開手機 Safari，結束後停服務。

依使用者需要設定 AltServer 登入啟動，沿用已有設定。LaunchAgent 可用實際路徑的 `open -g -j -a /Applications/AltServer.app` + RunAtLoad，不必 KeepAlive 重複啟動。

先 USB Refresh All，再拔 USB、同 Wi-Fi、手機解鎖，確認無線發現後實測 Refresh All。有效期更新且 guest 資料保留才通過。Mac 要開機、登入並執行 AltServer；續簽時可連 Apple。

## 官方來源

- https://faq.altstore.io/altstore-classic/how-to-install-altstore-macos
- https://faq.altstore.io/altstore-classic/app-ids
- https://github.com/LiveContainer/LiveContainer/releases
- https://livecontainer.github.io/docs/guides/add-to-home-screen
