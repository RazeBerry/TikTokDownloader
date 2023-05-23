# TikTok Video Downloader

This Python script allows you to automatically download videos from TikTok using Selenium WebDriver. The script first navigates to a TikTok profile page and scrolls through the page to collect all the video URLs. Then, it visits each URL through Snaptik.app and downloads the video. This script was tested on MacBook Pro with Apple Silicon and Python 3.11.2.

## Prerequisites

- Python 3.6 or later
- Selenium WebDriver
- Firefox Browser
- geckodriver


## Installation

1. Clone this repository:

    ```
    git clone https://github.com/RazeBerry/TikTokDownloader.git
    ```

2. Navigate to the cloned directory:

    ```
    cd TikTokDownloader
    ```

3. Install the required Python packages:

    ```
    pip install -r requirements.txt
    ```


## Usage

1. Open the `TikTokDownloader.py` script in a text editor.

2. Modify the following variables according to your needs:

    - `adblock_path`: Set this to the path of your downloaded Adblock Plus `.xpi` file. The `.xpi` file is included as part of the repository for your convenience.
    
    - `download_dir`: Set this to the path where you want the downloaded videos to be saved.

    - `tiktok_url`: Set this to the TikTok profile URL from which you want to download videos.

3. Run the script:

    ```
    python TikTokDownloader.py
    ```

The script will launch a Firefox window, navigate to the specified TikTok profile, and start downloading videos. Downloaded videos will be saved to the specified download directory.

## Notes

- The script will automatically dismiss any pop-up ads that appear during the download process.
- If a video download fails, the script will retry the download at the end of the process.
- If a video is still a photo rather than a video, the script will attempt to download it as a photo.
- This script allows multiple instances to be ran at the same time! Aka open multiple command prompts and they would be able to run simultaneously without issues prohibiting rate limits. 
- The script can possibly work with headless mode with Selenium but for debugging purposes I have left it on if you want to modify it such that it runs on headless mode change the relevant header section into: (do note that this is not tested to work as I had some difficulty getting both addon and headless mode to work simultaneously)
```
# Create a new instance of Firefox Options
options = Options()

# Add the argument "--headless" to the options
options.add_argument("--headless")

# Initialize the Firefox driver with the options
driver = webdriver.Firefox(options=options)
```

## How It Works

The script works in two main steps:

1. **Collecting the URLs**: The script navigates to the TikTok profile page and scrolls through the page to collect all the video URLs. It uses the `window.scrollTo` JavaScript function to scroll and Selenium WebDriver's `find_elements` method to find the video link elements.

2. **Downloading the videos**: The script visits each collected URL through Snaptik.app and clicks the download button to download the video. It waits until the download is complete before moving on to the next video. If a video fails to download, its URL is added to a list of failed downloads.

At the end, the script prints the URLs of the videos that were successfully downloaded and the ones that failed to download.

## Known Issues and Limitations

- The script is painfully slow as it is single-threaded among many other things and underoptimized. There are no motivations to optimize them as we may see ratelimits. 
- It is a known error some videos may have 0kb file size. I don't know the cause of it. 
- The script may fail to download a video if a timeout error occurs or if Snaptik.app fails to start the download. In such cases, the script will skip the current video and proceed to the next one.
- The sceipt will sometimes repeat downloading tiktok videos posted as images but it won't be stuck in a loop.
- The script assumes that Firefox's default download directory is used. If your downloads directory is different, you need to update the `download_dir` variable in the script.

## Disclaimer

This script is provided for educational purposes only. Always make sure you are in compliance with the terms of service of the websites you interact with.
