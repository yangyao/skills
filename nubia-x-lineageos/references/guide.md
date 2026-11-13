# Nubia X (NX616J) 刷 LineageOS 22.2 完整操作指南

记录于 2026-11-13。起点：一台已刷第三方 ROM（Android 9，mk_nx616j-userdebug）的 Nubia X；终点：官方 LineageOS 22.2（Android 15，2026-10 安全补丁）+ MindTheGapps。

## 0. 准备

- 电脑：`adb` + `fastboot`（macOS: `brew install android-platform-tools`）
- 数据线：必须是支持数据传输的线（充电线会导致 fastboot 完全不可见）
- 手机电量充到 50% 以上再开始刷机
- 下载（版本日期要一致，本例为 20261110）：
  - 官方 API 拿直链和校验值：`https://download.lineageos.org/api/v2/devices/nx616j/builds`
  - `recovery.img` / `dtbo.img` / `vbmeta.img` / `lineage-22.2-*-signed.zip`（各 ~64MB / 8MB / 4KB / 1.1GB）
  - GApps：MindTheGapps arm64（https://github.com/MindTheGapps/15.0.0-arm64/releases ）
- 所有文件 SHA256 与官方值核对后才可刷入

## 1. 连接

- USB adb：`adb devices` 应出现不带 IP 的条目；看不到就换线/换口
- 无线 adb：`adb connect <IP>:<端口>`（Android 11+ 端口随机，在开发者选项里看）
- fastboot 只能走 USB：`adb reboot bootloader` 后 `fastboot devices` 必须有输出

## 2. 解锁 bootloader（每次进 fastboot 都要做）

```
fastboot oem nubia_unlock NUBIA_NX616J
fastboot oem device-info   # 确认 Nubia fastboot unlocked: true
```

要点：

- 解锁会清空数据；开发者选项里的「OEM 解锁」开关只是前置许可，真实状态以 fastboot 为准
- **该 flag 在重启后会重置回 false**，所以解锁 → flash → 引导 recovery 必须一气呵成，中途不重启
- `Device unlocked: false` 是假象，以 `Nubia fastboot unlocked` 为准
- `fastboot boot <img>` 临时引导在此设备不支持

## 3. 刷 recovery 三件套

```
fastboot flash recovery recovery.img
fastboot flash dtbo dtbo.img
fastboot flash vbmeta vbmeta.img --disable-verity --disable-verification
```

只刷 recovery 不刷 dtbo/vbmeta 时，从旧固件（Android 9）启动的 LineageOS recovery 会开机即崩（表现为 Logo 一闪而过回到系统）。

## 4. 进入 recovery

- 实体键（音量上 + 电源）不可靠：松键即退出
- **推荐路径**：让旧系统开机，插 USB，然后：

```
adb reboot recovery
```

它会写 misc 分区，bootloader 自动引导 recovery，全程不用按键。

## 5. 清数据 + sideload 系统

1. recovery 里：**Factory reset → Format data / factory reset**（清空全部数据，必要步骤）
2. **Apply update → Apply from ADB**
3. 电脑：`adb sideload lineage-22.2-*.zip`
   - 成功标志：`Total xfer: 1.00x`
   - 进度停在 47%、报 `adb: failed to read command` 也算成功
4. 不要重启，继续下一步

## 6. sideload GApps（开机前最后机会）

1. 再点 **Apply update → Apply from ADB**
2. `adb sideload MindTheGapps-15.0.0-arm64-*.zip`
3. 提示 Signature verification failed → 选 **Yes**（预期行为）
4. 返回主菜单 → **Reboot system now**

首次开机 5–15 分钟属正常。WiFi 连接本身不需要代理；只有 Google 登录/Play 商店需要手机自己有代理。

## 8. 大文件下载经验（国内网络）

- 官方镜像直连：极慢且频繁 HTTP/2 断流
- 单线程 curl + socks5 代理：~150KB/s，可用但慢
- 推荐组合：curl 走代理 + `--http1.1` + 断点续传（`-C -`）+ 无限重试循环
- aria2 走 **HTTP 代理**端口（`--all-proxy=http://127.0.0.1:PORT -x16 -s16`）可多线程加速；aria2 不支持 socks5，会静默失败
- 可写看门狗脚本：每 10 分钟检查下载进程存活与流量增长，卡死自动杀掉重启续传

## 9. 以后升级

每月 nightly：下载新 zip → recovery → Apply from ADB → sideload。不需要重新解锁、清数据或重刷 recovery。

## 遗留状态

- bootloader 保持解锁状态，每次开机有解锁警告属正常
- 电池健康：设备闲置多年，首次刷机前电压仅 3.68V（~7%），建议观察续航
