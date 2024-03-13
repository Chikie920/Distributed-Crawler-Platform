package com.chikie.service;

import com.chikie.entity.Setting;

public interface SettingService {
    Setting getSetting();
    int updateSetting(Setting setting);
}
