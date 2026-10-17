# DIP 數位影像作業

目前作業為 HW01。從以下入口可以快速找到報告、程式與講義。

- [目前技術報告 PDF（尚有待填項目）](HW01/hw1/build/content.pdf)
- [報告正文](HW01/hw1/report_sections/gamma_comparison.tex)
- [報告編譯與待完成項目](HW01/hw1/README_report.md)
- [作業要求整理](HW01/作業要求整理.md)

儲存庫包含實作程式、LaTeX 原始檔、測試圖片、實驗結果與目前報告。
原始講義、作業需求 PDF、課程影片、參考筆記及舊預覽留在本機，不隨 Git 上傳。
報告尚待填寫的真實分工、審查與過程紀錄列於 `HW01/hw1/README_report.md`。

## 資料夾用途

```text
數位影像作業/
├── README.md                     檔案入口與操作方式
├── .vscode/                      VS Code 編譯與預覽設定
├── requirements.txt              Python 執行所需套件
├── .gitignore                    Git 檔案排除規則
├── logs/                         工具紀錄（僅本機）
└── HW01/
    ├── 作業要求整理.md
    ├── assignment/               原始作業需求 PDF（僅本機）
    ├── lectures/                 六份講義 PDF（僅本機）
    └── hw1/
        ├── *.py                  現有 Python 程式
        ├── content.tex           LaTeX 主檔
        ├── README_report.md      報告編譯說明與待辦
        ├── report_sections/      報告正文與手寫證明圖片
        ├── images/               實驗輸入圖片
        ├── results/              程式輸出的圖片、CSV、文字資料
        ├── build/                目前 content.pdf；其他暫存檔僅本機
        ├── references/           以下筆記與參考圖僅本機
        │   ├── figures/          原始參考圖片
        │   └── 牙齒頭骨比較.txt    組員整理的比較筆記
        ├── media/                hw1.mp4 課程影片（僅本機）
        └── archive/preview/      舊的 content-preview.*（僅本機）
```

## 平常操作

下載儲存庫後，先在根目錄安裝 Python 執行所需套件：

```powershell
python -m pip install -r requirements.txt
```

實驗以 Python 3.13 與 CPU 版 PyTorch 執行。LaTeX 編譯另需 XeLaTeX 與 LaTeX Workshop，
中文使用 Windows 的微軟正黑體；其他系統的字型設定請參閱 `HW01/hw1/README_report.md`。

編輯 `HW01/hw1/report_sections/gamma_comparison.tex` 或 `HW01/hw1/content.tex`，
存檔後會自動編譯，也可按 `Ctrl+Alt+B`。
在命令選擇區執行 `LaTeX Workshop: View LaTeX PDF file`，會開啟 `HW01/hw1/build/content.pdf`。
若原先已開啟舊 PDF 分頁，先關閉舊分頁再重新執行預覽。

Python 程式以 `HW01/hw1` 為工作目錄，例如從專案根目錄執行：

```powershell
cd HW01/hw1
python medical_experiments.py
```

`__pycache__` 與 `.pyc` 是 Python 自動產生的快取，已在 VS Code 檔案總管隱藏。
繳交資料夾的 `codes/`、`content.pdf`、`process.pdf` 結構另依作業要求整理。
