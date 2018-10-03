# -*- encoding=utf8 -*-
__author__ = "sa"

from airtest.core.api import *

auto_setup(__file__)

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(force_restart=False)
# start your script here

clear_app("com.taobao.idlefish")
sleep(1.0)

start_app("com.taobao.idlefish")
sleep(10.0)

if poco("com.taobao.idlefish:id/pic"):
    poco("com.taobao.idlefish:id/action_bar_right").click()

sleep(10)
snapshot(msg="页面显示正常")

clear_app("com.taobao.idlefish")
