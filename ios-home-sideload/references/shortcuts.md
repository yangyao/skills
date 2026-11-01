# 原生直啟捷徑

成功路徑：保留官方啟動擴充 → 捷徑使用 **Launch App AppIntent** → guest Launch URL → 手機匯入並測試 → 使用者加入主畫面。

`打開 URL` 或 `.mobileconfig` Web Clip 不是同一方案。Web Clip 可批量放原圖示，但經 Safari 確認；不能當成同等體驗的預設推薦。

## 產生檔案

每個 App 先從 LiveContainer 清單成功啟動，再取得該裝置的實際 app folder、LCDataUUID、簽名 team、已安裝啟動擴充 Bundle ID。**缺 LCDataUUID 就先完成初始化，不省略 UUID 產生一份看似可用的捷徑。** 此次遙控器曾在首次直啟失敗，從清單開啟後恢復。此次 AltStore 把主 ID 變成 `<original>.<team>`，擴充變成 `<parent>.<team>.<extension>`；不要把此規則當成所有安裝器的保證。

從當次官方 IPA 的 `LaunchAppExtension.appex/Metadata.appintents/extract.actionsdata` 核對 Intent 和參數。此次 3.8.0：Intent `LaunchAppExtension`、參數 `launchURL`；官方來源程式需要 ShareExtension。新版本依實際 metadata 更新。

設定 JSON 放倉庫外：

```json
{
  "extension_bundle_id": "com.example.container.TEAMID.LaunchAppExtension",
  "team_id": "TEAMID",
  "intent_identifier": "LaunchAppExtension",
  "parameter_name": "launchURL",
  "scheme": "livecontainer",
  "apps": [
    {"slug": "my-app", "name": "我的 App", "bundle_folder": "com.example.myapp.app", "container_id": "REPLACE-WITH-ACTUAL-UUID", "icon_path": "/private/path/我的 App.png"}
  ]
}
```

```sh
python3 scripts/make_shortcuts.py --config /private/path/launchers.json \
  --output-dir /private/path/public-downloads --sign
```

`--sign` 呼叫 Mac `shortcuts sign --mode anyone`，這是 Apple 捷徑檔分享簽署，不是替容器簽名，不需要 agent 取得 Apple 密碼。未加此選項只產生原始 plist 用於檢查；現代 iOS 分享匯入用已簽版本。

`name` 使用 App 實際顯示名稱，捷徑與下載檔名一致，別用 learning／remote 等難對應的檔名或額外前綴。`icon_path` 可選，指向倉庫外已取得的原始 PNG；**正式交付時提供原圖**，下載頁同卡片顯示 App 名稱、圖示預覽、捷徑下載及圖片下載，避免讓使用者另外尋找圖片。

腳本生成 index.html；只服務捷徑、圖示等非敏感檔案。先讓手機匯入一個測試，出現官方 Launch App 動作且能執行，再批量匯入其餘。關掉 HTTP 服務後，已匯入的捷徑仍可用。

## 圖示不能自動帶入

捷徑內部 glyph 與自訂 Home Screen PNG 是兩件事，**官方 Launch App 不會自動配置主畫面原圖示**。先說清楚此限制，不讓使用者走完才發現仍要手動。

可在 LiveContainer 長按 guest → Add to Home Screen → Save App Icon；agent 也可複製已生成的 `Documents/Applications/<folder>/LCAppIconLight.png` 到方便選取的位置（先確認該版本檔案存在）。

手機捷徑分享 → 加入主畫面 → 點圖示 → 選檔案／照片 → 加入，仍需使用者確認一次。未驗證第三方自動工具只能標為待評估。

舊 Web Clip 可移除對應桌面設定檔，不會刪 guest。先辨認正確 profile，不碰其他 VPN／管理項目。原生直啟仍可能因單容器執行另一 guest 而提示結束，不承諾所有提示消失。

## 來源

- https://livecontainer.github.io/docs/guides/add-to-home-screen
- https://github.com/LiveContainer/LiveContainer/issues/207
- https://support.apple.com/guide/shortcuts/apd735880972/ios
- https://livecontainer.github.io/docs/guides/multiple-livecontainers
