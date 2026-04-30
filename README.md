# 🎵 YouTube to MP3 Pro (Desktop Edition)

A professional-grade, full-stack desktop application that converts YouTube videos to high-quality MP3s. This project features a Python/Flask backend bundled into a standalone Windows Executable (`.exe`) with integrated FFmpeg processing.

## 📸 Interface
![Web App UI](assets/mp3_site_localrun.PNG)

## 🚀 Key Features
*   **Standalone Portable EXE:** No Python installation required for the end-user.
*   **Auto-Lifecycle Management:** Integrated **Heartbeat Logic** that automatically terminates the background server when the browser tab is closed to save system resources.
*   **Desktop Integration:** Automatically creates a `MyDownloads` folder on the user's Desktop for easy access to files.
*   **High-Performance Engine:** Powered by `yt-dlp` for robust extraction and `FFmpeg` for 192kbps audio conversion.

---

## 🛠️ The Architecture
This project uses a **Decoupled Desktop Architecture**. Instead of a standard GUI library, it utilizes a Flask web-server as the backend and a modern HTML/CSS/JS frontend, providing a superior UI/UX and mobile-first responsiveness.

### Technical Highlights:
*   **Resource Pathing:** Uses custom `resource_path` logic to handle temporary file extraction and internal pathing within the PyInstaller `_MEIPASS` environment.
*   **Multi-Threading:** Runs a background **Watchdog Thread** as a daemon to monitor browser pings and manage the process lifecycle.
*   **Binary Bundling:** Successfully bundles `ffmpeg.exe`, `index.html`, and `static` assets into a single-file distribution.

---

## 🔍 The "Cloud vs. Residential" Challenge
While originally designed for cloud deployment, this project evolved to tackle the 2026 YouTube security updates (PO Tokens/Bot Detection).
*   **The Problem:** Cloud platforms (Render/AWS) face heavy Data Center IP blocking.
*   **The Solution:** Transitioning to a Desktop App utilizes **Residential IPs**, ensuring 100% functionality and bypassing automated bot detection.

---

## 📂 Project Structure
*   `main.py`: Core Flask engine & lifecycle Watchdog logic.
*   `index.html`: Responsive Dashboard UI.
*   `static/`: Custom CSS and frontend assets.
*   `ffmpeg.exe`: The core conversion engine (bundled into the EXE).
*   `main.spec`: Configuration for the PyInstaller build process.

---

## 📦 How to Build (For Developers)
If you want to compile the EXE yourself from the source:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/AleronVaz/yt_mp3_downloader.git](https://github.com/AleronVaz/yt_mp3_downloader.git)
    cd yt_mp3_downloader
    ```
2.  **Install Dependencies:**
    ```bash
    pip install flask yt-dlp
    ```
3.  **Run the PyInstaller Command:**
    ```bash
    pyinstaller --noconsole --onefile --clean --icon=app_icon.ico --add-data "index.html;." --add-data "static;static" --add-binary "ffmpeg.exe;." main.py
    ```

---

## 📱 Legacy Support: Mobile (Termux)
The project remains compatible as a local server on Android via **Termux**:
1.  **Install Termux** (F-Droid version).
2.  **Setup Environment:**
    ```bash
    pkg update && pkg upgrade -y
    pkg install python git ffmpeg -y
    ```
3.  **Clone and Run:**
    ```bash
    git clone [https://github.com/AleronVaz/yt_mp3_downloader.git](https://github.com/AleronVaz/yt_mp3_downloader.git)
    cd yt_mp3_downloader
    python main.py
    ```