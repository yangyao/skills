---
name: nubia-x-lineageos
description: 从第三方 Android 9 ROM 把 Nubia X (NX616J) 刷到官方 LineageOS 22.2 (Android 15)，包括解鎖、recovery、sideload、GApps。适用于刷机中途 recovery 闪退、bootloader 解鎖 flag 重置、adb/fashboot 不可见等故障。
---

# Nubia X (NX616J) 刷官方 LineageOS 22.2

實際走通的全流程筆記（2026-11 在一台刷過第三方 Android 9 ROM 的 NX616J 上完成）。最終狀態：LineageOS 22.2 + MindTheGapps + SFA 代理。

## 關鍵前提

1. 官方支援確認：https://wiki.lineageos.org/devices/nx616j/install 是唯一權威流程；本 skill 只補充實戰坑。
2. 電腦需要 `adb` + `fastboot`；fastboot 只能走 USB，網路 ADB 不行。
3. 刷機會清空全部資料；先確認電量 >50%（fastboot 下充電極慢，先回系統充）。
4. 下載三類檔案：同一天的 `recovery.img` / `dtbo.img` / `vbmeta.img` + 系統 zip（download.lineageos.org/api/v2/devices/nx616j/builds 可拿直鏈和 SHA256）。

## 實戰坑（按發生順序）

### 1. 電腦看不到手機

- USB 線可能是純充電線：`adb devices` 只有無線條目、`fastboot devices` 空。換線是第一解法。
- Wi-Fi ADB 重啟後會掉，端口不一定是 5555（Android 11+ 隨機端口，手機開發者選項裡能看到）。

### 2. 解鎖 flag 會被重置（最大坑）

- Nubia 解鎖命令：`fastboot oem nubia_unlock NUBIA_NX616J`。
- **`Nubia fastboot unlocked` flag 在每次重啟/關機後會變回 false**，即使 `fastboot reboot` 前剛解鎖過。
- 因此正確順序是：進 fastboot → 解鎖 → **立刻** flash → 不經系統直接引導 recovery。每次回 fastboot 都要重新解鎖一次。
- `fastboot boot recovery.img`（臨時引導）在此設備不被支援。
- 標準 `Device unlocked: false` 顯示是假的，以 `Nubia fastboot unlocked` 為準。

### 3. recovery 一閃而退

- 只刷 recovery、不刷 dtbo/vbmeta 時，從 Android 9 舊固件起來的 LineageOS recovery 會啟動即崩。
- 解法：同時刷三件套，vbmeta 帶禁驗證參數：
  ```
  fastboot flash recovery recovery.img
  fastboot flash dtbo dtbo.img
  fastboot flash vbmeta vbmeta.img --disable-verity --disable-verification
  ```
- 實體鍵（音量上+電源）進 recovery 不可靠：鬆鍵會退出。**可靠路徑：啟動舊系統後執行 `adb reboot recovery`**（它寫 misc 分區，bootloader 會自動引導 recovery，全程無需按鍵）。

### 4. sideload 與 GApps

- 順序：recovery 裡 Format data → Apply from ADB → `adb sideload lineage.zip`（出現 `Total xfer: 1.00x` 即成功；47% 停住或 `failed to read command` 也是成功）。
- GApps 用 MindTheGapps arm64（https://github.com/MindTheGapps/15.0.0-arm64/releases ），必須在第一次開機前 sideload。
- GApps sideload 時提示 Signature verification failed → 選 **Yes** 繼續，這是預期的。

### 5. 大檔下載（國內網路）

- LineageOS 官方鏡像直連極慢且頻繁斷（HTTP/2 PROTOCOL_ERROR），單線程 curl + socks5 代理也只有 ~150KB/s。
- 有效組合：**aria2 不支援 socks5 代理**（會靜默失敗）；用 curl 走代理（`-x socks5h://127.0.0.1:port --http1.1 -C -`）配無限重試循環，或 aria2 走 **HTTP 代理**（`--all-proxy=http://127.0.0.1:port -x16`，若代理端口同時接受 CONNECT）。
- 一切以 SHA256 對官方值為準，校驗不過絕不刷入。
