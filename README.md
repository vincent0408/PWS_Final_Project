# PWS_Final_Project

PWS 109-2期末專案
|檔案名稱|用途 |
| ------ | ------ |
| processing_total.ipynb| 與全班相關的資料分析|
| processing_personal.ipynb| 與個人相關的資料分析|
| processing_visualization.ipynb| 分析並視覺化資料處理結果|
| processing_total.py | 將processing_total.ipynb轉成Python模組供data_total_XXX.py使用 |
| processing_personal.py | 將processing_personal.ipynb轉成Python模組供data_personal_XXX.py使用 |
| crawler.py| 爬下ccClub Judge中 PWS Homework 1~6的資料|
| data_total_XXX.py | 將資料分析中，全班共同相關的資料，寫入資料庫 |
| data_personal_XXX.py | 將資料分析中，使用者專屬相關的資料，寫入資料庫  |
| db_XXX.py | 其他與爬蟲資料無關的資料庫，如密碼、爬蟲資料呈現、使用者作業得分等等 |
| json/serviceAccountKey_XXX.json | 多個Firebase Realtime Database的驗證金鑰，照理來說為資安不能上傳，但考慮到此專案學習性質仍然上傳，若有安全疑慮將會撤下|
| mail_sender.py | 寄信機器人 |
