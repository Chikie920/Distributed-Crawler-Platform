package com.chikie.service.impl;

import com.chikie.dao.SettingDao;
import com.chikie.entity.Setting;
import com.chikie.service.SettingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class SetingServiceImpl implements SettingService {
    @Autowired
    private SettingDao settingDao;
    @Override
    public Setting getSetting() {
        return settingDao.getSetting();
    }
    @Override
    public int updateSetting(Setting setting) {
        return settingDao.updateSetting(setting);
    }
}
