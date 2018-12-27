from ui.ui_controller import UiController
from ampu import Ampu
from ampu import AmpuTaskManager

auto_uploader = Ampu()
ampu_task_manager = AmpuTaskManager(ampu_core=auto_uploader)
ui_controller = UiController()
ui_controller.set_core(ampu_task_manager)
ui_controller.start()