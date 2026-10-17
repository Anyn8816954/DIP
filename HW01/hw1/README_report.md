# LaTeX 技術報告

目前 Q1、Q2 以手寫證明圖片呈現，並完成 Gamma 前後比較（指定鐵塔圖及三個額外案例）、指定 `dark.jpg` 的直方圖等化實驗、醫學影像六個運算函式的程式與核心說明、補零與指定卷積測試、依組員整理的 `references/牙齒頭骨比較.txt` 加入的醫學影像比較，以及四組 CNN 模型比較。尚待補齊的報告項目列於本文末尾。

## 檔案位置

- `content.tex`：主檔，設定中文、版面、程式碼及圖片樣式。
- `report_sections/gamma_comparison.tex`：Q1／Q2 證明、Gamma、直方圖等化、牙齒／頭骨比較及 CNN 五個章節的正文。
- `report_sections/Q1Q2.jpg`：第一節使用的 Q1／Q2 手寫證明圖片，沒有另外轉寫證明文字與公式。
- `results/`：直接引用現有 Gamma、直方圖等化、`medical/mouth`、`medical/skull` 與 `cnn` 中的結果圖片。
- `build/`：目前的 `content.pdf`、SyncTeX 與 LaTeX 編譯暫存檔；最新報告請開啟 `build/content.pdf`。
- `references/`：組員比較筆記與 `figures/` 中的參考圖片，僅保留在本機。
- `media/`：課程影片 `hw1.mp4`，僅保留在本機。
- `archive/preview/`：先前的 `content-preview.*`，作為本機舊版存檔。

圖片路徑以 `hw1` 為工作目錄。請勿只移動 `.tex` 而未攜帶相關資料夾。

## 編譯

使用 **XeLaTeX**。文件使用 `ctexart`，中文改採 Windows 內建的 Microsoft JhengHei（微軟正黑體），以避免 Fandol 字型缺少部分繁體字。
若改用其他作業系統，須將主檔三個 `\setCJK...font` 指令中的字型名稱改為該環境已安裝且支援繁體中文的字型。

### 在 VS Code 編譯

專案根目錄 `數位影像作業/.vscode/settings.json` 已設定 `XeLaTeX (2 passes)`。
請以 VS Code 開啟整個「數位影像作業」資料夾，才能載入這份設定。
此配方直接執行 XeLaTeX 兩次，不經過 `latexmk`，因此這份報告的編譯流程不需要 Perl。

1. 若尚未安裝 TeX 發行版，可從 [MiKTeX 官網](https://miktex.org/download) 安裝。選擇只為目前使用者安裝；若希望編譯時自動補齊套件，將缺少套件的安裝方式設為 `Always`。完成後開啟 MiKTeX Console 檢查並安裝更新。
2. 在 VS Code 按 `Ctrl+Shift+X`，搜尋並安裝 **LaTeX Workshop**，擴充套件 ID 為 `James-Yu.latex-workshop`。
3. 完全關閉並重新開啟 VS Code，讓它讀取安裝後的 PATH。在新終端機執行 `xelatex --version`，確認能顯示版本。
4. 開啟 `content.tex` 或 `gamma_comparison.tex`，按 `Ctrl+Alt+B`。設定會從主檔所在的 `hw1` 資料夾編譯兩次，輸出 `build/content.pdf`。
5. 按 `Ctrl+Shift+P`，執行 `LaTeX Workshop: View LaTeX PDF file`，在 VS Code 內預覽。

目前設定為存檔後自動編譯；也可以按 `Ctrl+Alt+B` 手動更新 PDF。
`gamma_comparison.tex` 第一行已有指向主檔的 root 註解，因此編輯該分檔時也能找到 `content.tex`。
編譯工具使用主檔的預設輸出名稱，擴充套件的 `latex-workshop.latex.jobname` 留空，
並透過 `-output-directory=%OUTDIR%` 與 `latex-workshop.latex.outDir` 統一將 PDF、SyncTeX 與暫存檔放入 `build/`。
`gamma_comparison.tex` 是由主檔載入的章節，從這兩個 `.tex` 編譯或開啟預覽時，皆對應同一份 `build/content.pdf`。
若仍看到舊內容，先關閉舊 PDF 預覽分頁，回到 `.tex`，從命令選擇區重新執行 `LaTeX Workshop: View LaTeX PDF file`。
第一次編譯可能需要下載中文與排版套件。若遇到錯誤，可在「檢視 → 輸出」切換至 LaTeX Workshop 或 LaTeX Compiler，查看錯誤紀錄。

設定依據：[LaTeX Workshop 編譯文件](https://github.com/James-Yu/LaTeX-Workshop/wiki/Compile)、[MiKTeX Windows 安裝文件](https://miktex.org/howto/install-miktex)。

### 在終端機編譯

若電腦已有含所需套件的 TeX 發行版，在 PowerShell 執行：

```powershell
cd "C:\Users\user\Desktop\數位影像作業\HW01\hw1"
New-Item -ItemType Directory -Path build -Force | Out-Null
xelatex -synctex=1 -interaction=nonstopmode -halt-on-error -output-directory=build content.tex
xelatex -synctex=1 -interaction=nonstopmode -halt-on-error -output-directory=build content.tex
```

第二次編譯用於更新圖表與公式的交互參照；輸出為 `build/content.pdf`。
如果終端機找不到 `xelatex`，請重新開啟 VS Code 以讀取安裝後的 PATH，或使用 MiKTeX 安裝目錄中的 `xelatex.exe` 完整路徑。
舊的 `content-preview.*` 已集中到 `archive/preview/`，後續不再更新。
整理前位於 `hw1` 根目錄的 `content.pdf` 也已移入 `build/`；請關閉舊 PDF 分頁，重新執行預覽指令以開啟 `build/content.pdf`。
若編譯時無法覆寫 PDF，先關閉占用該 PDF 的外部閱讀器，再重新編譯。

若在 Overleaf 編譯，先將中文設定改為平台可用的繁體中文字型，再將 `content.tex`、`report_sections` 資料夾及以下圖片按原路徑上傳，主檔設為 `content.tex`、Compiler 設為 XeLaTeX：

```text
content.tex
report_sections/
  gamma_comparison.tex
  Q1Q2.jpg
results/
  brian-pennington-gray.png
  gamma-enhancement.png
  gamma-dark-gray.png
  gamma-dark-enhanced.png
  gamma_bright-gray.png
  gamma_bright-enhanced.png
  gamma_normal-gray.png
  gamma_normal-enhanced.png
  dark-gray.png
  equalized.png
  histogram-input.png
  histogram-mapping.png
  histogram-output.png
  medical/
    convolution-test.png
    mouth/
      padded.png
      padding-detail.png
      0-gray.png
      1-laplacian.png
      2-gradient.png
      4-sharpened.png
      5-mask.png
      6-denoised_sharpened.png
    skull/
      padded.png
      padding-detail.png
      0-gray.png
      1-laplacian.png
      2-gradient.png
      4-sharpened.png
      5-mask.png
      6-denoised_sharpened.png
```

CNN 章節另需 `results/cnn/` 中四個案例的 `*-input.png` 與 `*-comparison.png`，共八張圖片。
章節數值依目前的 `*-summary.txt` 與 `photo-128-outputs.csv` 整理；修改測試後應同步更新報告。

醫學影像第 4.3 節包含指定卷積測試圖、精確分數與 CSV 八位小數輸出，
並引用牙齒、頭骨各自的補零全圖及左上角放大圖。
補零素材為每側一個零值像素；已核對四側全為零、內部像素與原圖相同，且高寬各增加兩個像素。

## 後續編輯

1. 在 `content.tex` 的 `\author{...}` 填入組員姓名與學號。
2. 依實際分工填寫 Gamma 章節末尾的實作者、審查者與審查意見。
3. 若修改 Python 參數並重跑，請同步更新正文參數、圖說與統計數字。
4. 加入其他部分時，在主檔使用 `\input{report_sections/新的檔名}`。

統計數值是對現有完整尺寸灰階 PNG 計算；平均灰階為所有像素的算術平均。
純白／純黑比例分別計算像素值等於 255／0 的比例。
建立時已逐像素核對四組輸出與 `uint8(clip(255 * (I / 255) ** gamma, 0, 255))` 一致。

繳交時取 `build/content.pdf` 作為技術報告，依作業規定與 `process.pdf`、`codes` 放入繳交資料夾；
`.tex`、此說明檔及編譯暫存檔不放入最終壓縮檔。

## 尚待補齊的報告項目

以下是目前報告檔案中尚未見到的內容，並非表示組員尚未在其他地方完成：

- Q1、Q2 已以手寫證明圖片呈現；成員姓名與實際審查紀錄仍須依真實分工補填。
- 理論總整理及單一整合心智圖。
- 實作前的問題紀錄，以及諮詢 AI／老師前後的個人結論。
- `process.pdf` 所需的需求／分工／進度表、會議紀錄、工時、心得與貢獻比例。
- 各章節的真實姓名與審查意見。
- 最終 `hw1.zip` 的 `codes/`、`content.pdf`、`process.pdf` 結構及內容檢查。

可解釋 CNN 屬加分項目，目前的隨機權重實驗尚未涵蓋此項。
