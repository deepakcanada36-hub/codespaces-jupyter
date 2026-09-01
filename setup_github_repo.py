import os
import base64
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or input("Enter your GitHub Personal Access Token: ").strip()
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME") or input("Enter your GitHub Username: ").strip()
REPO_NAME = os.environ.get("REPO_NAME", "whatsapp-blaster-apk")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

MAIN_PY_CONTENT = """import os
import time
import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, cast


class WhatsAppBlasterApp(App):
    def build(self):
        self.excel_path = None
        self.media_path = None

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.status_label = Label(text="WhatsApp Bulk Sender", font_size=20)
        layout.add_widget(self.status_label)

        btn_excel = Button(text="1. Select Excel File (.xlsx)", size_hint_y=None, height=50)
        btn_excel.bind(on_release=self.open_excel_chooser)
        layout.add_widget(btn_excel)

        btn_media = Button(text="2. Select Media File (Image/Video - Optional)", size_hint_y=None, height=50)
        btn_media.bind(on_release=self.open_media_chooser)
        layout.add_widget(btn_media)

        self.msg_input = TextInput(hint_text="Type custom message here...", multiline=True)
        layout.add_widget(self.msg_input)

        btn_start = Button(text="3. Start Bulk Blast", size_hint_y=None, height=60, background_color=(0, 1, 0, 1))
        btn_start.bind(on_release=self.start_blast)
        layout.add_widget(btn_start)

        return layout

    def open_excel_chooser(self, instance):
        self.show_file_popup(self.set_excel_path)

    def open_media_chooser(self, instance):
        self.show_file_popup(self.set_media_path)

    def show_file_popup(self, callback):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView()
        content.add_widget(filechooser)

        btn_select = Button(text="Select", size_hint_y=None, height=40)
        content.add_widget(btn_select)

        popup = Popup(title="Select File", content=content, size_hint=(0.9, 0.9))

        def on_select(inst):
            if filechooser.selection:
                callback(filechooser.selection[0])
            popup.dismiss()

        btn_select.bind(on_release=on_select)
        popup.open()

    def set_excel_path(self, path):
        self.excel_path = path
        self.status_label.text = f"Excel Loaded: {os.path.basename(path)}"

    def set_media_path(self, path):
        self.media_path = path
        self.status_label.text = f"Media Loaded: {os.path.basename(path)}"

    def send_via_whatsapp_intent(self, phone_number, message, media_path=None):
        if platform != 'android':
            print(f"[Simulated Output] Sending to {phone_number}: {message}")
            return

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        String = autoclass('java.lang.String')

        currentActivity = PythonActivity.mActivity

        if media_path:
            intent = Intent(Intent.ACTION_SEND)
            intent.setPackage("com.whatsapp")

            ext = media_path.split('.')[-1].lower()
            mime_type = "image/*" if ext in ['jpg', 'jpeg', 'png'] else "video/*"
            intent.setType(mime_type)

            File = autoclass('java.io.File')
            file_obj = File(media_path)
            uri = Uri.fromFile(file_obj)

            intent.putExtra(Intent.EXTRA_STREAM, cast('android.os.Parcelable', uri))
            intent.putExtra(Intent.EXTRA_TEXT, String(message))
            intent.putExtra("jid", String(f"{phone_number}@s.whatsapp.net"))
        else:
            url = f"https://api.whatsapp.com/send?phone={phone_number}&text={Uri.encode(message)}"
            intent = Intent(Intent.ACTION_VIEW)
            intent.setData(Uri.parse(url))
            intent.setPackage("com.whatsapp")

        currentActivity.startActivity(intent)

    def start_blast(self, instance):
        if not self.excel_path:
            self.status_label.text = "Error: Select Excel file first!"
            return

        try:
            df = pd.read_excel(self.excel_path)
            numbers = df['Phone'].astype(str).tolist()
            text_msg = self.msg_input.text

            for num in numbers:
                clean_num = "".join(filter(str.isdigit, num))
                self.status_label.text = f"Processing: {clean_num}"
                self.send_via_whatsapp_intent(clean_num, text_msg, self.media_path)
                time.sleep(5)

            self.status_label.text = "Bulk Process Completed!"

        except Exception as e:
            self.status_label.text = f"Failed: {str(e)}"


if __name__ == '__main__':
    WhatsAppBlasterApp().run()
"""

BUILDOZER_SPEC_CONTENT = """[app]
title = WhatsApp Blaster
package.name = whatsappblaster
package.domain = org.automation
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy,pandas,openpyxl,pyjnius

orientation = portrait
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
"""

WORKFLOW_CONTENT = """name: Build Android APK

on:
  push:
    branches: [ \"main\", \"master\" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Build APK with Buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        id: buildozer
        with:
          repository_root: .
          workdir: .
          buildozer_version: stable

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: WhatsAppBlaster-APK
          path: ${{ steps.buildozer.outputs.filename }}
"""


def create_or_update_github_file(path, content, commit_message):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{path}"
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    response = requests.get(url, headers=headers)
    sha = None
    if response.status_code == 200:
        sha = response.json().get("sha")

    payload = {
        "message": commit_message,
        "content": encoded_content,
    }
    if sha:
        payload["sha"] = sha

    response = requests.put(url, json=payload, headers=headers)
    if response.status_code in [200, 201]:
        print(f"Successfully pushed: {path}")
    else:
        print(f"Failed to push {path}: {response.text}")


def ensure_repo_exists():
    create_repo_url = "https://api.github.com/user/repos"
    repo_data = {
        "name": REPO_NAME,
        "private": False,
        "auto_init": True,
    }
    response = requests.post(create_repo_url, json=repo_data, headers=headers)
    if response.status_code in [200, 201]:
        print(f"Repository '{REPO_NAME}' created successfully.")
    elif response.status_code == 422:
        print(f"Repository '{REPO_NAME}' already exists; continuing.")
    else:
        print(f"Repository setup failed: {response.json().get('message', 'Unknown error')}")
        raise RuntimeError("GitHub repository creation failed")


if __name__ == "__main__":
    if not GITHUB_TOKEN or not GITHUB_USERNAME:
        raise ValueError("GITHUB_TOKEN and GITHUB_USERNAME must be provided.")

    ensure_repo_exists()
    create_or_update_github_file("main.py", MAIN_PY_CONTENT, "Add main application file")
    create_or_update_github_file("buildozer.spec", BUILDOZER_SPEC_CONTENT, "Add buildozer configuration")
    create_or_update_github_file(".github/workflows/build.yml", WORKFLOW_CONTENT, "Add GitHub Actions workflow")

    print("\n--- Process Triggered ---")
    print(f"Access your build at: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}/actions")
