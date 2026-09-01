[app]
title = WhatsApp Blaster
package.name = whatsappblaster
package.domain = org.automation
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = tests, bin, .buildozer

version = 0.1
requirements = python3,kivy,pyjnius,requests

orientation = portrait
fullscreen = 0

# Entry point for Android
android.entrypoint = org.kivy.android.PythonActivity
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,INTERNET
android.accept_sdk_license = True
android.enable_androidx = True
android.copy_libs = 1

# Icons and branding
android.icon = %(source.dir)s/data/icon.png
android.presplash_filename = %(source.dir)s/data/presplash.png

# Build optimization
android.gradle_options = org.gradle.jvmargs=-Xmx2048m
p4a.release_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin
