# App 接入與存檔

## IPA

確認 target 支援手機。iPad-only 的 UIDeviceFamily 不能只改包就算 iPhone 適配；有源碼時改小螢幕版面、family、方向和觸控尺寸。編譯真機 **Release**，檢查離線資源與版本；不優先用含額外 Debug dylib 的包。

ZIP 只放 `Payload/App.app`，排除 AppleDouble `._*` 和 `__MACOSX`。此次曾因 AppleDouble 導致 `0xe8008001`；此錯誤也可能有其他原因，不要直接撤銷憑證。

用 `scripts/prepare_ipa.py` 清包或保留指定擴充。腳本不簽名，也不保證刪擴充後功能完整。保留清單必須來自當次版本的依賴核對。

## 備份

先停正式 App 寫入，備份最新 Library 和實際使用的 Documents／App Groups；放在倉庫外並建立 hash。不要為搬普通資料匯出全部 Keychain 或容器簽名憑證。

```sh
xcrun devicectl device copy from --device "$DEVICE_ID" \
  --domain-type appDataContainer --domain-identifier "$SOURCE_BUNDLE_ID" \
  --source Library --destination "$PRIVATE_BACKUP/Library" --timeout 60
```

讀 App 源碼確認進度、積分、Web game 狀態、偏好等位置。NAS 同步回積分不代表本機題組、作答和進度也回來。

## guest 映射與遷移

匯入後先請使用者不啟動。若已啟動，先備份新資料，檢查是否有新進度或待處理同步，再選合併或還原，不能盲目覆蓋。

此次 3.8.0 已驗證：

```text
Documents/Applications/<actual-app-folder>.app/LCAppInfo.plist
  LCDataUUID
  LCContainers（多容器時選對項目）
Documents/Data/Application/<LCDataUUID>/Library/
```

新版、Shared App 或外部容器可能不同，先列檔讀映射；不要使用舊手機 UUID。讀所需 guest LCAppInfo 即可，不讀無關主程式憑證／登入資料。

1. 使用者從多工畫面完全關閉 LiveContainer。
2. 只搬已確認的 App 子目錄，不整包覆蓋 LiveContainer 自己的 Library。
3. 原生 ID 可能帶 team suffix；偏好 plist 名稱改為 guest 實際 ID。不要複製另一台裝置的 client identity。
4. 寫入後讀回必要檔案核對 hash／內容；啟動、重開驗證保存和同步。
5. 舊版只有在遷移驗證且授權後才刪。各手機分開確認，不拿一台成功當全家完成。

配對 cookie 可能在 Keychain，需重新配對。搬電視位址不代表搬到憑證；讓新裝置產生自己的 client ID。只有使用者要配對／控制時才對電視發請求，勿擅自顯示 PIN、切輸入或停用除錯。

日後更新 guest：先備份，在 LiveContainer 匯入同 Bundle ID 新 IPA，核對資料保留。不要用 AltStore 把 guest 又裝成原生 App、浪費簽名名額。
