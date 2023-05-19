from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

import time
import os
import shutil

# Initialize the Firefox driver
driver = webdriver.Firefox()

# Keep track of the original window handle (this is the "name" of the original tab)
original_window = driver.current_window_handle

# keep track of the last number of URLs
last_num_urls = 0

# navigate to the profile page
profile_url = 'https://www.tiktok.com/@???'
driver.get(profile_url)

time.sleep(3)

# extract the username from the profile URL
username = profile_url.split('@')[-1]

# list to store the video URLs
video_urls = []

# get the total height of the page
total_height = int(driver.execute_script("return document.body.scrollHeight"))
print(total_height)
no_new_urls_count = 0

i = 1

# Path to your downloaded adblock plus extension
adblock_file_path = 'ADBLOCK PATH PUT IT HERE'

# Install the Adblock Plus extension
driver.install_addon(adblock_file_path, temporary=True)


# Switch back to the original window
driver.switch_to.window(original_window)


while i < total_height:
    print(f'Starting loop with position {i} out of {total_height}')  # print statement at the start of the loop

    driver.execute_script("window.scrollTo(0, {});".format(i))
    time.sleep(1)  # increase sleep time to allow more time for page to load

    # find all video link elements
    video_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/video/"]')

    # extract the URLs from the elements
    new_video_urls = [e.get_attribute('href') for e in video_elements]

    # add the new URLs to the list
    new_urls = [url for url in new_video_urls if url not in video_urls]
    video_urls.extend(new_urls)

    if new_urls:
        print(f'Found {len(new_urls)} new URLs')  # print the number of new URLs found
        no_new_urls_count = 0
    else:
        print('No new URLs found')
        no_new_urls_count += 1

    # update the total height at every iteration
    total_height = int(driver.execute_script("return document.body.scrollHeight"))

    if no_new_urls_count > 12:
        print(f'No new URLs found in the last 12 scrolls, stopping.')
        break

    print(f'Ending loop with position {i} out of {total_height}')  # print statement at the end of the loop

    i += 200

# the directory where Firefox downloads files by default
download_dir = 'INSERT DOWNLOAD PATH'

# create a new directory for the user
user_dir = os.path.join(download_dir, username)
os.makedirs(user_dir, exist_ok=True)

# lists to store the successful and failed downloads
successful_downloads = []
failed_downloads = []

for url in video_urls:
    # navigate to the page
    driver.get('https://snaptik.app/')
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, 'url')))

    # find the input element
    input_element = driver.find_element(By.NAME, 'url')

    # type in the TikTok URL
    input_element.send_keys(url)
    
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.button-go.is-link')))

    # find the submit button and click it
    submit_button = driver.find_element(By.CSS_SELECTOR, 'button.button-go.is-link')
    submit_button.click()

    try:
        # wait for the new page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.button.download-file.is-secondary.mt-3')))
        
        # check if the ad is present and dismiss it
        try:
            ad_dismiss_button = driver.find_element(By.CSS_SELECTOR, 'button.ad-dismiss')
            ad_dismiss_button.click()
        except:
            pass  # ad was not present, proceed as normal

        # find the download link
        download_link = driver.find_element(By.CSS_SELECTOR, 'a.button.download-file.is-secondary.mt-3')

        # click the download link
        download_link.click()

        # wait for the download to complete
        while True:
            time.sleep(1)  # wait 1 second before checking again
            download_files = [f for f in os.listdir(download_dir) if f.endswith('.crdownload')]
            if not download_files:
                break  # no more .crdownload files, download must be complete

        # move the downloaded file to the user's directory
        downloaded_files = [f for f in os.listdir(download_dir) if f.endswith('.mp4')]
        if downloaded_files:
            # get the newest downloaded file
            newest_file = max(downloaded_files, key=lambda x: os.path.getmtime(os.path.join(download_dir, x)))
            file_size = os.path.getsize(os.path.join(download_dir, newest_file))
            if file_size == 0:
                print(f'Download failed (0KB file) for {url}.')
                failed_downloads.append(url)
            else:
                # move the file to the user's directory
                shutil.move(os.path.join(download_dir, newest_file), os.path.join(user_dir, newest_file))
                print(f'Successfully downloaded {url}.')
                successful_downloads.append(url)
                # only remove if it was previously considered a failed download
                if url in failed_downloads:
                    failed_downloads.remove(url)
        else:
            print(f'Download failed (no file) for {url}.')
            failed_downloads.append(url)
    except TimeoutException:
        print(f'TimeoutException occurred for {url}. Trying to download as photo...')

        # Find all the photo download links
        photo_elements = driver.find_elements(By.CSS_SELECTOR, 'a.button.w100[data-event="download_albumPhoto_photo"]')
        for photo_element in photo_elements:
            # Click each photo download link
            photo_element.click()
                    # Check if the popup is present and dismiss it
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Close"]')))
                close_button = driver.find_element(By.XPATH, '//span[text()="Close"]')
                close_button.click()
            except TimeoutException:
                pass  # popup was not present, proceed as normal

            # Click each photo download link
            photo_element.click()
            
            # wait for the download to complete
            while True:
                time.sleep(0.2)  # wait  second before checking again
                download_files = [f for f in os.listdir(download_dir) if f.endswith('.crdownload')]
                if not download_files:
                    break  # no more .crdownload files, download must be complete

            # move the downloaded file to the user's directory
            downloaded_files = [f for f in os.listdir(download_dir) if f[:-4].isdigit() and f.endswith(('.jpg', '.jpeg', '.png'))]
            if downloaded_files:
                # get the newest downloaded file
                newest_file = max(downloaded_files, key=lambda x: os.path.getmtime(os.path.join(download_dir, x)))
                # move the file to the user's directory
                shutil.move(os.path.join(download_dir, newest_file), os.path.join(user_dir, newest_file))
                print(f'Successfully downloaded photo {url}.')
                successful_downloads.append(url)
                # only remove if it was previously considered a failed download
                if url in failed_downloads:
                    failed_downloads.remove(url)
            else:
                print(f'Download failed (no photo) for {url}.') 

# After the first run of the download operation, delete all 0KB mp4 files
for filename in os.listdir(download_dir):
    file_path = os.path.join(download_dir, filename)
    if filename.endswith('.mp4') and os.path.getsize(file_path) == 0:
        os.remove(file_path)
        print(f'Deleted 0KB file: {filename}')

# print the successful and failed downloads
print('Successfully downloaded these videos:')
for url in successful_downloads:
    print(url)

print('Failed to download these videos:')
for url in failed_downloads:
    print(url)

print('Attempting to redownload failed videos...')
for url in failed_downloads:
    try:
        # navigate to the page
        driver.get('https://snaptik.app/')
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, 'url')))

        # find the input element
        input_element = driver.find_element(By.NAME, 'url')

        # type in the TikTok URL
        input_element.send_keys(url)
        
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.button-go.is-link')))

        # find the submit button and click it
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button.button-go.is-link')
        submit_button.click()

        # wait for the new page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.button.download-file.is-secondary.mt-3')))
        
        # check if the ad is present and dismiss it
        try:
            ad_dismiss_button = driver.find_element(By.CSS_SELECTOR, 'button.ad-dismiss')
            ad_dismiss_button.click()
        except:
            pass  # ad was not present, proceed as normal

        # find the download link
        download_link = driver.find_element(By.CSS_SELECTOR, 'a.button.download-file.is-secondary.mt-3')

        # click the download link
        download_link.click()

        # wait for the download to complete
        while True:
            time.sleep(1)  # wait 1 second before checking again
            download_files = [f for f in os.listdir(download_dir) if f.endswith('.crdownload')]
            if not download_files:
                break  # no more .crdownload files, download must be complete

        # move the downloaded file to the user's directory
        downloaded_files = [f for f in os.listdir(download_dir) if f.endswith('.mp4')]
        if downloaded_files:
            # get the newest downloaded file
            newest_file = max(downloaded_files, key=lambda x: os.path.getmtime(os.path.join(download_dir, x)))
            file_size = os.path.getsize(os.path.join(download_dir, newest_file))
            if file_size == 0:
                print(f'Redownload failed (0KB file) for {url}.')
                failed_downloads.remove(url)
            else:
                print(f'Successfully redownloaded {url}.')
                shutil.move(os.path.join(download_dir, newest_file), os.path.join(user_dir, newest_file))
                successful_downloads.append(url)
                failed_downloads.remove(url)
        else:
            print(f'Redownload failed (no file) for {url}.')
            failed_downloads.remove(url)
    except TimeoutException:
        print(f'TimeoutException occurred for {url} during re-download attempt. Skipping this video.')

if not failed_downloads:
    # close the browser session
    driver.quit()

def remove_empty_files(directory):
    # iterate over all files in the directory
    for filename in os.listdir(directory):
        # construct the full file path
        file_path = os.path.join(directory, filename)
        # check if it is a file (not a directory) and its size is 0
        if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
            # remove the file
            os.remove(file_path)
        
remove_empty_files(download_dir)
