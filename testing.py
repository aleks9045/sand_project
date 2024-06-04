import pyautogui


def testing():
    pyautogui.sleep(2)

    start_pos = 500, 300
    pyautogui.scroll(2000)
    pyautogui.sleep(0.1)
    for i in range(20):
        pyautogui.moveTo(start_pos)
        pyautogui.drag(500, 0, 3)


if __name__ == "__main__":
    testing()
