# 🚀 CypherMesh Prep

**CypherMesh Prep** is an automated, lightweight desktop tool built with Python and OpenCV. It is specifically designed to prepare side-by-side orthographic renders for Image-to-3D AI generators (such as Meshy.ai).

AI 3D generators often struggle with floor lines, gradient backgrounds, and harsh black outlines, which results in messy 3D topology. This tool automatically cleans up the image and splits it into perfect Front and Back views with transparent backgrounds, ready for generation.

## ✨ Features

- **✂️ Automatic Splitting:** Detects and splits side-by-side images into separate left/right (Back/Front) views.
- **🧹 Smart Background Removal:** Uses Otsu's thresholding to adapt to gradient backgrounds and isolate the main object automatically.
- **🚫 Floor-Line Deletion:** Applies morphological operations to erase thin horizon/floor lines that AI models often mistake for physical geometry.
- **🎨 Outline Smoothing:** Uses a Bilateral Filter to smooth out harsh inner black lines and shadows while preserving sharp outer edges.
- **🖥️ Simple GUI:** A clean, minimal, and user-friendly Tkinter interface.

## 🛠️ Requirements

Make sure you have Python installed. You can install the required dependencies using:

```bash
pip install -r requirements.txt
```

🚀 How to Use
Run the script:

Bash
python cyphermesh.py
The splash screen will load, followed by the main GUI.

Click "Učitaj sliku i obradi" (Load and process image).

Select your side-by-side render (e.g., .png or .jpg).

The tool will automatically generate two new files in the same directory:

meshy_ready_front.png

meshy_ready_back.png

Upload these perfectly masked images directly to Meshy.ai or your preferred Image-to-3D platform!

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

📜 License
This project is open-source and available under the MIT License.
