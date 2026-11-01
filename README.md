# skills

給 agent 使用的個人工作流程。內容以實際使用經驗整理，避免換裝置、加 App 時重複踩坑。

| Skill | 用途 |
| --- | --- |
| [ios-home-sideload](ios-home-sideload/SKILL.md) | Mac AltServer + AltStore Classic + LiveContainer：換手機、加自製 App、保留存檔、Wi-Fi 續簽與官方直啟捷徑 |

## 使用

把本倉庫交給 agent，請它先讀對應 `SKILL.md`，或把 skill 資料夾安裝到 agent 的 skills 目錄。

Codex 範例：

```sh
git clone https://github.com/yangyao/skills.git
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/ios-home-sideload" ~/.codex/skills/ios-home-sideload
```

若本機已存在同名 skill，先比較內容，不直接覆蓋。新工作階段可以使用：

> 使用 $ios-home-sideload，將我的自製 App 接入另一台 iPhone，保留存檔、設定無線刷新和直啟捷徑。

技能只攜帶流程，不攜帶任何人的 Apple 帳號、裝置識別碼、憑證、配對記錄、App 存檔或 IPA。Agent 必須在每次任務取得當下裝置資料。沒有 GitHub Actions 或自動發佈。

## 已知取捨

官方 Launch App 捷徑已實測能避免 Safari 入口，但原 App 圖示與「加入主畫面」仍有手機手動確認步驟。不要把「可產生捷徑檔」誤稱為全自動安裝桌面原圖示。
