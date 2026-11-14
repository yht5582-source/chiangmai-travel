# 清邁慢旅｜2026 旅行手帳

2026/11/15–11/22清邁八日互動行程，手機與桌機皆可使用。根目錄index.html為完整網頁，不需套件或API金鑰。

## 功能

- 依Asia/Bangkok日期自動換日，每30秒及返回頁面時檢查。旅程前顯示首日、結束後顯示末日。
- 可手動選日；按「跟隨今天」恢復自動模式。
- Google Maps內嵌地點標記、步行/搭車導航、每日分段路線。
- 經使用者允許後取得定位，顯示座標、精度與到景點的約略直線距離。
- 所有地點搜尋與行程完成勾選。

## 定位與距離

定位需在HTTPS網站開啟並允許位置權限；內嵌預覽可能不支援。位置只在記憶體中使用，停止即清除，不回傳網站。Google Maps相關按鈕會將所需座標傳給Google；勾選紀錄僅存在目前瀏覽器。

距離由裝置位置和景點概略座標計算，為直線估算，非道路里程、步行時間或入口精準距離。請以Google Maps具名地點、分店和實際導航為準。

## 行程與資料

住宿安排：11/15–11/18 THEE Vijit Lanna；11/18–11/22 Arun Khiri。航班和住宿依旅客憑證為準；按摩、餐廳與接送均尚未預約。

天氣提示整理於2026/11/14，非即時氣象。週三11/18以換飯店、咖啡及按摩為主，目前無法確定會有暴雨。

參考：[泰國氣象局](https://www.tmd.go.th/en/weather/region/northern)、[真心市集](https://jingjaicentralchiangmai.com/public/market)、[Fah Lanna](https://fahlanna.com/location/)、[Akha Ama](https://www.akhaamacoffee.com/)、[One Nimman](https://www.onenimman.com/en/event/)。

## GitHub Pages

Settings → Pages → Deploy from a branch → main → / (root) → Save。

.nojekyll讓Pages直接提供靜態內容；Google地圖與導航需要網路。

## 驗證

已測試JavaScript語法、泰國午夜換日、旅程日期邊界、距離公式、模擬定位成功/拒絕/停止、8天路線連結；以瀏覽器檢查日期切換、地點搜尋與Google地圖。實體手機GPS需由使用者在裝置上允許後確認。
