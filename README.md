# 🎵 YouTube to MP3 Downloader

A full-stack project featuring a Python backend for audio extraction and a modern, responsive web interface.

## 📸 Gallery

#### Web Interface
![Web App UI](assets/mp3_site_localrun.png)

#### Terminal Performance (Local)
![Local Success](assets/mp3_terminal.png)

#### The "Cloud Wall" (Render Logs)
![Render Error](assets/mp3_render_error.png)

> [!IMPORTANT]
> **Status: Functionally Complete / Deployment Restricted**
> This application is fully operational in local development environments. However, due to YouTube's enhanced security updates in early 2026 (PO Tokens/Bot Detection), live deployment on cloud platforms like Render is currently restricted by Data Center IP blocking.

## 🚀 Project Overview
This repository contains a dual-interface system:
1. **CLI Tool:** A Python script for local command-line downloads (Fully Functional).
2. **Web Interface:** A clean, mobile-responsive frontend (HTML/CSS) designed for cloud deployment.

## 🌐 Live Site
- **Status:** Backend logic is restricted on Render due to automated bot-detection.
- **Development Note:** The site remains hosted to demonstrate UI/UX design and API architecture.

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3 (Mobile-First Design), JavaScript.
- **Backend:** Python 3.x, Flask.
- **Core Engine:** `yt-dlp` / `pytubefix` & `FFmpeg`.

## 🔍 The "Cloud vs. Bot Detection" Challenge
During the deployment phase, the project served as a deep dive into modern web security.
- **The Issue:** YouTube's **Proof of Origin (PO) Token** system requires interactive browser handshakes that "headless" cloud servers (Render/AWS) cannot easily provide.
- **The Investigation:** I experimented with multiple libraries and branching strategies (see `pytube-library-change` branch) to bypass these restrictions, documenting the shift from simple scraping to advanced authentication requirements.

## 📂 Structure
- `index.html`: The main dashboard for the converter.
- `style.css`: Custom Red & White theme with mobile responsiveness.
- `main.py`: The core Flask/Python script handling the conversion logic.
- `requirements.txt`: List of dependencies for cloud and local environments.

## 📦 Local Installation
Since local machines use **Residential IPs**, the project works as intended when run on your own hardware:

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/AleronVaz/yt_mp3_downloader.git](https://github.com/AleronVaz/yt_mp3_downloader.git)
   cd yt_mp3_downloader
   ```