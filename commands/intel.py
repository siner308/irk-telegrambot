import time
import datetime
from random import choice
from uuid import uuid4

from utils.handle_string import extract_command
from utils.maps import get_location
from utils.giphy import get_giphy_image_url
from settings import MAX_LOAD_TIME


def get_intel_screenshot(robot, bot, update):
    '''인텔 스크린샷 찍어드려요'''
    start_time = int(time.time())
    print(update.message.text)
    tokens = extract_command(update.message.text)
    print(tokens)
    now = datetime.datetime.now()

    # send help information
    if not len(tokens):
        text = '*/intel* 명령어 입력 후, 원하는 위치의 주소를 아는대로 적어주시면 됩니다.\n' \
               'ex) `/intel 올림픽공원`'
        update.message.reply_markdown(text)
        return

    if not robot.chrome.check_lock():
        lock_id = uuid4()
        if not (robot.chrome.lock(lock_id=lock_id)):
            text = '`%s에 사용을 시작한 유저가 있습니다. 잠시만 기다려주세요`' % robot.chrome.locked_at
            update.message.reply_markdown(text='%s' % text)
            return
    else:
        text = '`%s에 사용을 시작한 유저가 있습니다. 잠시만 기다려주세요`' % robot.chrome.locked_at
        update.message.reply_markdown(text='%s' % text)
        return

    # get response
    robot.logger.info('[%s] Getting Geolocation...' % (time.time() - start_time))
    keyword = ' '.join(tokens)
    data = get_location(keyword)
    if not len(data['results']):
        text = '`구글에 주소 데이터가 없습니다.`'
        update.message.reply_markdown(text='%s' % text)
        robot.chrome.unlock()
        return

    # get address
    try:
        robot.logger.info('[%s] Finding Address...' % (time.time() - start_time))
        address = data['results'][0]['formatted_address']
        message = '%s\n' \
                  '`%s`' % (address, str(now))
    except Exception as e:
        robot.logger.info(e)
        robot.logger.info(data)
        text = '`주소를 불러오는데 실패했습니다.`\n' \
               '>%s' % keyword
        update.message.reply_markdown(text='%s' % text)
        robot.chrome.unlock()
        return

    # parsing address
    try:
        robot.logger.info('[%s] Parsing Address...' % (time.time() - start_time))
        lat = round(float(data['results'][0]['geometry']['location']['lat']), 6)
        lng = round(float(data['results'][0]['geometry']['location']['lng']), 6)
        edge_west = data['results'][0]['geometry']['viewport']['southwest']['lng']
        edge_east = data['results'][0]['geometry']['viewport']['northeast']['lng']
        width = edge_east - edge_west

    except Exception as e:
        robot.logger.info(e)
        robot.logger.info(data)
        text = '`좌표를 불러오는데 실패했습니다.`\n' \
               '>%s' % address
        update.message.reply_markdown(text='%s' % text)
        robot.chrome.unlock()
        return

    # Settings Zoom Level
    robot.logger.info('[%s] Setting Zoom Level...' % (time.time() - start_time))
    all_portal_zoom = 0.08
    if width < all_portal_zoom:
        z = 15
    else:
        z = 13
        extra_z = 0
        while width > all_portal_zoom * (2 ** (2 + extra_z)):
            extra_z += 1
        z -= extra_z

    # Notify Giphy
    robot.logger.info('[%s] Notify Giphy...' % (time.time() - start_time))
    try:
        text = '`준비가 되는 동안 귀여운 거 보시죠`'
        giphy_queryset = ['puppy', 'dog', 'cat', 'kitten', 'rabbit', 'kangaroo']
        giphy_image_url = get_giphy_image_url(choice(giphy_queryset))
    except Exception as e:
        robot.logger.info(e)
        text = '귀여운걸 불러오는데 실패했어요... ㅠㅠ'
        giant_penguin_image_url = 'http://woman.chosun.com/editor/cheditor_new/attach/2019/AFW9NUB869E9LSXPF1Z4_1.jpg'
        giphy_image_url = giant_penguin_image_url

    update.message.reply_markdown(text='%s\n%s' % (text, giphy_image_url))

    # Getting Intel Map
    robot.logger.info('[%s] Getting Intel Map...' % (time.time() - start_time))
    url = 'https://intel.ingress.com/intel?ll=%s,%s&z=%s' % (lat, lng, z)
    robot.logger.info(url)
    robot.chrome.driver.get(url)
    time.sleep(1)

    robot.logger.info('[%s] %s (lat: %s, lng: %s, z: %s)' % ((time.time() - start_time), keyword, lat, lng, z))
    if robot.chrome.driver.title != 'Ingress Intel Map':
        text = '지도를 불러오는 데 실패했어요 ㅠㅠ'
        update.message.reply_markdown(text='%s' % text)
        robot.chrome.unlock()
        return
    while True:
        current_time = int(time.time())
        spent_time = current_time - start_time
        robot.logger.info(spent_time)

        # Timeout
        if spent_time > MAX_LOAD_TIME:
            message = '너무 오래걸리는 지역이라서 이정도만 보여드릴게요!\n' \
                      '%s' % message
            break

        # Get Loading Percent
        try:
            loading_msg = robot.chrome.driver.find_element_by_id('loading_msg')
        except Exception as e:
            robot.logger.info(e)
            robot.logger.info(robot.chrome.driver.page_source)
            text = '지도를 불러오긴 했는데... 로딩하는 도중에 실패했어요 ㅠㅠ'
            update.message.reply_markdown(text='%s' % text)
            robot.chrome.unlock()
            return

        # Load Complete
        if loading_msg.get_attribute("style") == 'display: none;':
            break
        time.sleep(1)

    # Saving Screenshot
    robot.logger.info('[%s] Saving Screenshot...' % (time.time() - start_time))
    filename = now.strftime('%Y%m%d%H%M%S')
    try:
        file_url = robot.chrome.save_screenshot(filename)
        text = '%s\n%s' % (message, file_url)
    except Exception as e:
        text = '스크린샷 저장에 실패했어요... ㅠㅠ'
        update.message.reply_markdown(text='%s' % text)
        robot.logger.info(e)

    robot.chrome.unlock()
    update.message.reply_markdown(text=text)