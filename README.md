# TikTok Video Downloader

This Python script allows you to automatically download videos from TikTok using Selenium WebDriver. The script first navigates to a TikTok profile page and scrolls through the page to collect all the video URLs. Then, it visits each URL through Snaptik.app and downloads the video.

## Prerequisites

- Python 3.6 or later
- Selenium WebDriver
- Firefox Browser
- geckodriver

## Usage

1. Make sure you have all the prerequisites installed.
2. Clone this repository or download the Python script.
3. Open the script and replace `'/Users/sihao/Downloads'` with the actual path to your downloads directory.
4. Replace `'https://www.tiktok.com/@enabunnyz'` with the URL of the TikTok profile you want to download videos from.
5. Run the script. 

## How It Works

The script works in two main steps:

1. **Collecting the URLs**: The script navigates to the TikTok profile page and scrolls through the page to collect all the video URLs. It uses the `window.scrollTo` JavaScript function to scroll and Selenium WebDriver's `find_elements` method to find the video link elements.

2. **Downloading the videos**: The script visits each collected URL through Snaptik.app and clicks the download button to download the video. It waits until the download is complete before moving on to the next video. If a video fails to download, its URL is added to a list of failed downloads.

At the end, the script prints the URLs of the videos that were successfully downloaded and the ones that failed to download.

## Known Issues and Limitations

- The artificial scrolling feature is bugged and is known to only have very limited scrolling abilities and therefore can't collect all the urls from a user.
- The script is painfully slow as it is single-threaded.
- It is a known error some videos may have 0kb file size.
- The script may fail to download a video if a timeout error occurs or if Snaptik.app fails to start the download. In such cases, the script will skip the current video and proceed to the next one.
- The script assumes that Firefox's default download directory is used. If your downloads directory is different, you need to update the `download_dir` variable in the script.

## Disclaimer

This script is provided for educational purposes only. Always make sure you are in compliance with the terms of service of the websites you interact with.
