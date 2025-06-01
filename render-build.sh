#!/usr/bin/env bash
set -e

# Install Chromium and ChromeDriver for Selenium headless
apt-get update
apt-get install -y chromium chromium-driver

# Create symlinks so selenium can find Chrome
ln -s /usr/bin/chromium /usr/bin/google-chrome
ln -s /usr/lib/chromium/chromedriver /usr/bin/chromedriver
