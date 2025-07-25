# WiFiMapper

WiFiMapper is a professional WiFi analysis tool designed to scan, visualize, and optimize wireless networks. It provides features such as network scanning, heatmap generation, channel optimization, interference detection, and network simulation, all within a user-friendly PyQt6-based graphical interface.

## Table of Contents

- Overview
- Features
- Prerequisites
- Installation
- Usage
- Developer Notes
- License

## Overview

WiFiMapper is built to assist network administrators and enthusiasts in analyzing WiFi networks. It supports multiple frequency bands (2.4 GHz, 5 GHz, 6 GHz), provides real-time network scanning, and visualizes signal strength through heatmaps. The tool also includes simulation capabilities to estimate network performance based on access point models and environmental factors.

## Features

- **Network Scanning**: Scan available WiFi networks with details like SSID, BSSID, RSSI, channel, and security type.
- **Heatmap Generation**: Visualize signal strength over a loaded floor plan in 2D or 3D.
- **Channel Optimization**: Suggests the least congested channel for better performance.
- **Interference Detection**: Identifies potential WiFi and non-WiFi interference sources.
- **Network Simulation**: Simulates network performance based on access point models, wall materials, and device counts.
- **Multilingual Support**: Interface available in English, Persian, and Chinese.
- **Theme Customization**: Supports multiple themes (Windows 11, Dark, Light, Red, Blue).
- **Export Options**: Generate reports in PDF, CSV, or KMZ formats.
- **Offline Mode**: Allows usage without active WiFi scanning.

## Prerequisites

- Python 3.8 or higher
- PyQt6
- pyqtgraph
- numpy
- pandas
- Pillow
- reportlab
- qdarkstyle
- pywifi (optional, for WiFi scanning; requires comtypes on Windows)
- simplekml (optional, for KMZ export)

## Installation

1. Ensure Python 3.8+ is installed on your system.
2. Install the required dependencies using pip:

   ```bash
   pip install PyQt6 pyqtgraph numpy pandas Pillow reportlab qdarkstyle
   ```
3. (Optional) For WiFi scanning, install pywifi:

   ```bash
   pip install pywifi
   ```

   On Windows, also install comtypes:

   ```bash
   pip install comtypes
   ```
4. (Optional) For KMZ export, install simplekml:

   ```bash
   pip install simplekml
   ```
5. Place the `WiFiMapper.jpg` logo file in the project directory for favicon and logo display.

## Usage

1. Run the application:

   ```bash
   python wifi_mapper.py
   ```
2. Use the control panel to:
   - Load a floor plan (PNG, JPG, JPEG, PDF, or DWG).
   - Start a network scan (select frequency band and scan mode).
   - Generate a heatmap based on scan data.
   - Optimize channels or detect interference/dead zones.
   - Run network simulations with customizable parameters.
3. Switch themes or languages in the Settings tab.
4. Save projects or export reports via the File menu.

## Developer Notes

- Developed by Hamid Yarali.
- Ensure the `WiFiMapper.jpg` file is in the project directory for proper logo and favicon display.
- Translation files (\*.qm) for Persian and Chinese should be available in the project directory.
- The application supports offline mode for environments without WiFi capabilities.
- For better favicon rendering, consider converting `WiFiMapper.jpg` to `.ico` format.
- The heatmap generation uses a simplified path loss model; enhance it for more accurate results if needed.

## License

This project is licensed under the MIT License.

---

# WiFiMapper (فارسی)

WiFiMapper یک ابزار حرفه‌ای برای تحلیل شبکه‌های وای‌فای است که برای اسکن، تجسم و بهینه‌سازی شبکه‌های بی‌سیم طراحی شده است. این ابزار قابلیت‌هایی مانند اسکن شبکه، تولید نقشه حرارتی، بهینه‌سازی کانال، تشخیص تداخل و شبیه‌سازی شبکه را در یک رابط گرافیکی کاربرپسند مبتنی بر PyQt6 ارائه می‌دهد.

## فهرست مطالب

- بررسی اجمالی
- ویژگی‌ها
- پیش‌نیازها
- نصب
- استفاده
- یادداشت‌های توسعه‌دهنده
- مجوز

## بررسی اجمالی

WiFiMapper برای کمک به مدیران شبکه و علاقه‌مندان به تحلیل شبکه‌های وای‌فای طراحی شده است. این ابزار از باندهای فرکانسی مختلف (2.4 گیگاهرتز، 5 گیگاهرتز، 6 گیگاهرتز) پشتیبانی می‌کند، اسکن شبکه را در زمان واقعی انجام می‌دهد و قدرت سیگنال را از طریق نقشه‌های حرارتی تجسم می‌کند. همچنین قابلیت شبیه‌سازی عملکرد شبکه بر اساس مدل‌های نقطه دسترسی و عوامل محیطی را دارد.

## ویژگی‌ها

- **اسکن شبکه**: اسکن شبکه‌های وای‌فای موجود با جزئیاتی مانند SSID، BSSID، RSSI، کانال و نوع امنیت.
- **تولید نقشه حرارتی**: تجسم قدرت سیگنال روی یک پلان کف بارگذاری‌شده در حالت دوبعدی یا سه‌بعدی.
- **بهینه‌سازی کانال**: پیشنهاد کانال با کمترین ازدحام برای عملکرد بهتر.
- **تشخیص تداخل**: شناسایی منابع احتمالی تداخل وای‌فای و غیروای‌فای.
- **شبیه‌سازی شبکه**: شبیه‌سازی عملکرد شبکه بر اساس مدل‌های نقطه دسترسی، جنس دیوارها و تعداد دستگاه‌ها.
- **پشتیبانی چندزبانه**: رابط کاربری به زبان‌های انگلیسی، فارسی و چینی.
- **شخصی‌سازی تم**: پشتیبانی از تم‌های مختلف (ویندوز 11، تیره، روشن، قرمز، آبی).
- **گزینه‌های خروجی**: تولید گزارش در فرمت‌های PDF، CSV یا KMZ.
- **حالت آفلاین**: امکان استفاده بدون اسکن فعال وای‌فای.

## پیش‌نیازها

- پایتون 3.8 یا بالاتر
- PyQt6
- pyqtgraph
- numpy
- pandas
- Pillow
- reportlab
- qdarkstyle
- pywifi (اختیاری، برای اسکن وای‌فای؛ در ویندوز نیاز به comtypes دارد)
- simplekml (اختیاری، برای خروجی KMZ)

## نصب

1. اطمینان حاصل کنید که پایتون 3.8 یا بالاتر روی سیستم نصب است.
2. وابستگی‌های مورد نیاز را با استفاده از pip نصب کنید:

   ```bash
   pip install PyQt6 pyqtgraph numpy pandas Pillow reportlab qdarkstyle
   ```
3. (اختیاری) برای اسکن وای‌فای، pywifi را نصب کنید:

   ```bash
   pip install pywifi
   ```

   در ویندوز، comtypes را نیز نصب کنید:

   ```bash
   pip install comtypes
   ```
4. (اختیاری) برای خروجی KMZ، simplekml را نصب کنید:

   ```bash
   pip install simplekml
   ```
5. فایل لوگو `WiFiMapper.jpg` را در دایرکتوری پروژه قرار دهید تا آیکون و لوگو نمایش داده شود.

## استفاده

1. برنامه را اجرا کنید:

   ```bash
   python wifi_mapper.py
   ```
2. از پنل کنترلی برای موارد زیر استفاده کنید:
   - بارگذاری پلان کف (PNG، JPG، JPEG، PDF یا DWG).
   - شروع اسکن شبکه (انتخاب باند فرکانسی و حالت اسکن).
   - تولید نقشه حرارتی بر اساس داده‌های اسکن.
   - بهینه‌سازی کانال‌ها یا تشخیص تداخل/مناطق مرده.
   - اجرای شبیه‌سازی شبکه با پارامترهای قابل تنظیم.
3. تغییر تم یا زبان از تب تنظیمات.
4. ذخیره پروژه‌ها یا خروجی گزارش‌ها از منوی فایل.

## یادداشت‌های توسعه‌دهنده

- توسعه‌یافته توسط حمید یارعلی.
- اطمینان حاصل کنید که فایل `WiFiMapper.jpg` در دایرکتوری پروژه برای نمایش صحیح لوگو و آیکون موجود است.
- فایل‌های ترجمه (\*.qm) برای فارسی و چینی باید در دایرکتوری پروژه موجود باشند.
- برنامه از حالت آفلاین برای محیط‌هایی بدون قابلیت وای‌فای پشتیبانی می‌کند.
- برای رندر بهتر آیکون، می‌توانید فایل `WiFiMapper.jpg` را به فرمت `.ico` تبدیل کنید.
- تولید نقشه حرارتی از یک مدل ساده کاهش مسیر استفاده می‌کند؛ در صورت نیاز، آن را برای نتایج دقیق‌تر بهبود دهید.

## مجوز

این پروژه تحت مجوز MIT منتشر شده است.

---

# WiFiMapper (中文)

WiFiMapper 是一款专业的 WiFi 分析工具，旨在扫描、可视化和优化无线网络。它提供网络扫描、热图生成、信道优化、干扰检测和网络模拟等功能，所有这些都集成在一个基于 PyQt6 的用户友好图形界面中。

## 目录

- 概述
- 功能
- 前提条件
- 安装
- 使用
- 开发者说明
- 许可证

## 概述

WiFiMapper 专为网络管理员和爱好者设计，用于分析 WiFi 网络。它支持多种频段（2.4 GHz、5 GHz、6 GHz），提供实时网络扫描，并通过热图可视化信号强度。该工具还包括基于接入点模型和环境因素的网络性能模拟功能。

## 功能

- **网络扫描**：扫描可用 WiFi 网络，获取 SSID、BSSID、RSSI、信道和安全类型等详细信息。
- **热图生成**：在加载的平面图上以 2D 或 3D 形式可视化信号强度。
- **信道优化**：建议最不拥挤的信道以提高性能。
- **干扰检测**：识别潜在的 WiFi 和非 WiFi 干扰源。
- **网络模拟**：根据接入点模型、墙体材料和设备数量模拟网络性能。
- **多语言支持**：界面支持英语、波斯语和中文。
- **主题自定义**：支持多种主题（Windows 11、深色、浅色、红色、蓝色）。
- **导出选项**：生成 PDF、CSV 或 KMZ 格式的报告。
- **离线模式**：允许在没有活跃 WiFi 扫描的情况下使用。

## 前提条件

- Python 3.8 或更高版本
- PyQt6
- pyqtgraph
- numpy
- pandas
- Pillow
- reportlab
- qdarkstyle
- pywifi（可选，用于 WiFi 扫描；在 Windows 上需要 comtypes）
- simplekml（可选，用于 KMZ 导出）

## 安装

1. 确保系统中安装了 Python 3.8 或更高版本。
2. 使用 pip 安装所需依赖项：

   ```bash
   pip install PyQt6 pyqtgraph numpy pandas Pillow reportlab qdarkstyle
   ```
3. （可选）若需 WiFi 扫描，安装 pywifi：

   ```bash
   pip install pywifi
   ```

   在 Windows 上，还需安装 comtypes：

   ```bash
   pip install comtypes
   ```
4. （可选）若需 KMZ 导出，安装 simplekml：

   ```bash
   pip install simplekml
   ```
5. 将 `WiFiMapper.jpg` 标志文件放置在项目目录中，以便显示图标和标志。

## 使用

1. 运行应用程序：

   ```bash
   python wifi_mapper.py
   ```
2. 使用控制面板进行以下操作：
   - 加载平面图（PNG、JPG、JPEG、PDF 或 DWG）。
   - 开始网络扫描（选择频段和扫描模式）。
   - 根据扫描数据生成热图。
   - 优化信道或检测干扰/死区。
   - 使用可自定义参数运行网络模拟。
3. 在设置选项卡中切换主题或语言。
4. 通过文件菜单保存项目或导出报告。

## 开发者说明

- 由 Hamid Yarali 开发。
- 确保 `WiFiMapper.jpg` 文件位于项目目录中，以便正确显示标志和图标。
- 波斯语和中文的翻译文件 (\*.qm) 应位于项目目录中。
- 应用程序支持离线模式，适用于没有 WiFi 功能的环境。
- 为获得更好的图标渲染效果，可考虑将 `WiFiMapper.jpg` 转换为 `.ico` 格式。
- 热图生成使用简化的路径损耗模型；如需更精确的结果，可对其进行增强。

## 许可证

本项目采用 MIT 许可证发布。