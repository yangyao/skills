# Nubia X 重获新生：刷官方 LineageOS 22.2

一台刷着第三方 Android 9 ROM、安全补丁停在 2021 年的 Nubia X (NX616J)，完整刷到官方 LineageOS 22.2（Android 15，2026-10 安全补丁）。全程通过 adb/fastboot 远程操控，一条命令一条命令走的实弹记录。

## 能解决什么

- 从第三方 ROM / 老固件刷官方 LineageOS（官方 wiki 只覆盖标准流程，这里补全了实际会踩的坑）
- 刷机中途 recovery 闪退、解锁 flag 重置、fastboot 看不到设备等故障的定位与修复
- 国内核网络下下载 1GB+ 刷机包的稳定下载方案

## 适合谁

- 手上有 Nubia X 或同类老设备（高通 sdm845 时代），想升到能维护的官方 ROM
- Agent 需要远程通过 adb/fastboot 替使用者执行刷机流程

## 入口

- 给 Agent：[SKILL.md](SKILL.md)
- 给人看的完整操作记录：[references/guide.md](references/guide.md)
