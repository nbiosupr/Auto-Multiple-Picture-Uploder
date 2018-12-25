from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions as selenium_exception

import time
import os.path

driver_path = "D:\\실습\\auto_multi_picture_uploader\\externalDriver\\chromedriver_win32\\chromedriver.exe"


def get_all_file(folder_path):
    file_list = []
    for root, dirs, files in os.walk(os.path.abspath(folder_path)):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


class AmpuError(Exception):
    pass


class IlligalArgumentError(ValueError):
    pass


class LoginFailedError(AmpuError):
    pass


class NoTaskError(AmpuError):
    pass


class ConvertSize:
    b = 1
    kb = 1024
    mb = 1024 * 1024

    def __init__(self):
        pass

    def __call__(self, size, from_s, to_s):
        if from_s == ConvertSize.b:
            if to_s == ConvertSize.kb:
                return size / ConvertSize.kb
            elif to_s == ConvertSize.mb:
                return size / ConvertSize.mb
        elif from_s == ConvertSize.kb:
            if to_s == ConvertSize.b:
                return size * ConvertSize.b
            elif to_s == ConvertSize.mb:
                return size / ConvertSize.b
        elif from_s == ConvertSize.mb:
            if to_s == ConvertSize.b:
                return size * ConvertSize.mb
            elif to_s == ConvertSize.kb:
                return size * ConvertSize.kb

        raise IlligalArgumentError('[e : @convert size] 잘못된 파라미터 입니다.')


class Task:
    def __init__(self,
                 task_title=None,
                 cafe_path=None,
                 menu_name=None,
                 post_title=None,
                 comment=None,
                 images_path=None,
                 number_to_divide=None):
        self.task_title = task_title
        self.cafe_path = cafe_path
        self.menu_name = menu_name
        self.post_title = post_title
        self.comment = comment
        self.images_path = images_path
        self.number_to_divide = number_to_divide


class AmpuTaskManager:
    def __init__(self, ampu_core):
        self.__task_list = list()
        self.__ampu_core = Ampu()

    def naver_login(self):
        self.__ampu_core.login()

    def add_task(self, my_task):
        self.__task_list.append(my_task)

    def execute(self):
        if len(self.__task_list) == 0:
            raise NoTaskError

        ampu_core = self.__ampu_core

        for task in self.__task_list:
            cafe_path = task.cafe_path
            menu_name = task.menu_name
            subject = task.post_title
            image_folder_path = task.images_path
            divided_number = task.number_to_divide

            images = get_all_file(image_folder_path)

            ampu_core.go_to_cafe(task.cafe_path)

            if divided_number == 1 :
                my_post = Post()
                my_post.set_menu_name(menu_name)
                my_post.set_title(subject)
                my_post.set_images(images)
                ampu_core.write(my_post)
            else:
                images_list = ampu_core.divide_images_by_number(images, divided_number)
                idx = 1
                for temp_images in images_list:
                    my_post = Post()
                    my_post.set_menu_name(menu_name)
                    my_post.set_title(subject + ' - ' + str(idx))
                    my_post.set_images(temp_images)
                    ampu_core.write(my_post)
                    idx += 1


class Post:
    def __init__(self):
        self.menu_name = None
        self.title = None
        self.image_list = None

    def set_menu_name(self, menu_name):
        self.menu_name = menu_name

    def set_images(self, images):
        self.image_list = images

    def set_title(self, title):
        self.title = title


class Ampu:
    NAVER_IMAGES_SIZE_LIMIT = ConvertSize()(50,
                                            ConvertSize.mb,
                                            ConvertSize.b)
    LOGIN_URL = "https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com"
    VERY_LONG_TIME = 300
    LONG_TIME = 20
    SHORT_TIME = 3

    def __init__(self):

        self.__driver = None

        self.__task_list = list()

        self.__is_login = False

        self.is_cli_test = False

    @classmethod
    def make_multi_file_path(cls, images):
        # images는 str array 입니다.

        multi_file_path = ''

        for image_path in images:
            multi_file_path += image_path + ' \n '

        multi_file_path = multi_file_path[:-3]

        return multi_file_path

    def __initialize_driver(self):
        self.__driver = webdriver.Chrome(driver_path)
        self.__driver.implicitly_wait(3)

    def __upload_images(self, multi_file_path):
        VERY_LONG_TIME = Ampu.VERY_LONG_TIME
        LONG_TIME = Ampu.LONG_TIME
        driver = self.__driver

        #######################################

        # 프레임 스위치
        try:
            driver.switch_to.frame("cafe_main")
        except selenium_exception.NoSuchFrameException:
            pass

        driver.find_element_by_id('iImage').click();

        parent_window = driver.window_handles[0]
        child_window = driver.window_handles[1]

        driver.switch_to.window(child_window)
        button_close_notice = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'npe_alert_btn_close'))
        )
        button_close_notice.click()

        # 파일업로드
        file_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'pc_image_file'))
        )

        file_input.send_keys(multi_file_path)

        # 이미지 사이즈 변경
        time.sleep(0.3)
        WebDriverWait(driver, VERY_LONG_TIME).until_not(
            EC.element_to_be_clickable((By.CLASS_NAME, "npe_alert_btn_cancel"))
        )
        driver.execute_script("document.getElementsByClassName('npu_size_item')[8].click()")

        # 업로드 버튼 클릭
        upload_button = WebDriverWait(driver, LONG_TIME).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'npu_btn_submit'))
        )
        upload_button.click()
        WebDriverWait(driver, VERY_LONG_TIME).until(
            EC.number_of_windows_to_be(1)
        )
        driver.switch_to.window(parent_window)

    def __write_post(self, my_post):
        # my_post 는 post 클래스의 인스턴스 입니다.

        VERY_LONG_TIME = Ampu.VERY_LONG_TIME
        LONG_TIME = Ampu.LONG_TIME
        SHORT_TIME = Ampu.SHORT_TIME

        driver = self.__driver
        menu_name = my_post.menu_name

        subject_text = my_post.title
        images = my_post.image_list

        # 글작성클릭
        try:
            driver.switch_to.default_content()
        except selenium_exception.NoSuchFrameException:
            pass

        try:
            post_write_button = WebDriverWait(driver, LONG_TIME).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'cafe-write-btn'))
            )
        except selenium_exception.TimeoutException:
            raise LoginFailedError('[e:@Ampu.__write_post] 로그인 요망')

        post_write_button.click()

        # 메뉴 선택
        driver.switch_to.frame('cafe_main')
        menu_box = Select(driver.find_element_by_name('menuid'))
        menu_box.select_by_visible_text(menu_name)

        # 제목 입력
        driver.find_element_by_id('subject').click()
        driver.find_element_by_id('subject').send_keys(subject_text)
    
        # 이미지 업로드
        divided_images_list = Ampu.divide_images_list_by_size(images)
        for divided_images in divided_images_list:
            multi_file_path = Ampu.make_multi_file_path(divided_images)
            self.__upload_images(multi_file_path)

        # 게시글 등록
        WebDriverWait(driver, LONG_TIME).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "cafe_main"))
        )
        driver.execute_script('oCafeWrite.preCafeWriteContents()')

        # 게시글 등록이 완료될 때 까지 대기
        WebDriverWait(driver, LONG_TIME).until_not(
            EC.presence_of_element_located((By.ID, 'cafePreviewBtn'))
        )

    ##########################
    # public class method #
    ##########################

    @classmethod
    def divide_images_list_by_size(cls, images):
        # 이미지 경로 리스트를 파라미터로 받습니다.
        # 이미지 경로 리스트를 용량 제한에 맞춰 나눠 리스트에 담아 리턴합니다.

        divided_images_list = []
        size_limit = Ampu.NAVER_IMAGES_SIZE_LIMIT

        total_size = 0

        divided_images = list()
        for image_path in images:
            image_size = os.path.getsize(image_path)
            temp_total_size = total_size + image_size
            if temp_total_size < size_limit:
                total_size += image_size
                divided_images.append(image_path)
                pass
            else:
                divided_images_list.append(divided_images)
                # 초기화
                total_size = 0
                divided_images= list()
                # 새 리스트에 저장
                total_size += image_size
                divided_images.append(image_path)

        if divided_images:
            divided_images_list.append(divided_images)

        return divided_images_list

    @classmethod
    def divide_images_by_number(cls, images, number_of_div):
        if number_of_div < 1:
            raise IlligalArgumentError('[e : @ampu.__divide_images_by_number] 잘못된 파라미터입니다. 1 이상의 값을 전달해 주세요')

        divided_images_list = []
        number_of_images = len(images)
        number_of_each_list = int(number_of_images / number_of_div)
        start_index = 0
        end_index = number_of_each_list

        while end_index <= number_of_images:
            divided_images_list.append(images[start_index:end_index])
            start_index = end_index
            end_index = end_index + number_of_each_list

        if end_index < number_of_images:
            divided_images_list.append(images[start_index:])

        return divided_images_list

    ##########################
    # public instance method #
    ##########################
    def go_to_cafe(self, cafe_path):
        if not self.__is_login:
            raise LoginFailedError
        driver = self.__driver
        driver.get(cafe_path)

    def login(self, is_abroad = False, phone = None):
        self.__initialize_driver()

        driver = self.__driver
        driver.get(Ampu.LOGIN_URL)

        try:
            if is_abroad:
                phone_number_box = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.ID, 'phone_value'))
                )
                phone_number_box.send_keys(phone)
                phone_number_box.submit()

        except selenium_exception.TimeoutException:
            print('[e] 로그인에 실패하였습니다.')
            exit()

        try:
            WebDriverWait(driver, Ampu.LONG_TIME).until(
                EC.presence_of_element_located((By.ID, 'minime'))
            )
        except selenium_exception.TimeoutException:
            raise LoginFailedError

        self.__is_login = True
        
    def logoff(self):
        pass
        # todo 드라이버 닫아버리기

    def add_task(self, my_task):
        self.__task_list.append(my_task)

    def write(self, my_post):
        # 예외처리
        if not self.__is_login:
            raise LoginFailedError
        try:
            self.__write_post(my_post)
        except Exception as e:
            print(e)
            return False

        return True


def test_case_all():
    cafe_url = 'https://cafe.naver.com/autouploadtest'
    menu_name = '자유게시판'
    title = '업로더를 테스트합니다.'
    image_path = 'C:\\Users\\nbios\\Pictures\\test'
    div_num = 3

    auto_uploader = Ampu()
    ampu_task_manager = AmpuTaskManager(ampu_core=auto_uploader)

    my_task = Task(task_title='test1',
                   cafe_path=cafe_url,
                   menu_name=menu_name,
                   post_title=title,
                   images_path=image_path,
                   number_to_divide=div_num)
    ampu_task_manager.add_task(my_task)

    ampu_task_manager.naver_login()
    ampu_task_manager.execute()


def test_case_convert():
    num_mb = 50
    convert_size = ConvertSize()
    converted_num = convert_size(num_mb, ConvertSize.mb, ConvertSize.b)
    print(converted_num)


def test_case_login():
    auto_uploader = Ampu()
    auto_uploader.login(is_abroad=False)
    input()


def test_case_getfiles():
    image_path = 'C:\\Users\\nbios\\Pictures\\test'
    images = get_all_file(image_path)

    divided_images_list = []
    size_limit = 50 * 1024 * 1024

    total_size = 0

    divided_images = list()
    for image_path in images:
        image_size = os.path.getsize(image_path)
        temp_total_size = total_size + image_size
        if temp_total_size < size_limit:
            total_size += image_size
            divided_images.append(image_path)
            pass
        else:
            divided_images_list.append(divided_images)
            # 초기화
            total_size = 0
            divided_images = list()
            # 새 리스트에 저장
            total_size += image_size
            divided_images.append(image_path)

    if divided_images:
        divided_images_list.append(divided_images)

    for e in divided_images_list:
        image_multi = Ampu.make_multi_file_path(e)
        print('-------------------')
        print(image_multi)

    #print(image_multi)

test_case_all()