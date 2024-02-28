package com.chikie.dao;

import com.chikie.entity.Setting;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import org.springframework.stereotype.Repository;

@Repository
public interface SettingDao {
    @Select("SELECT user_agent userAgent, proxy, ua_type uaType, proxy_open proxyOpen FROM setting")
    Setting getSetting();

    @Update("UPDATE setting SET user_agent = #{userAgent}, proxy = #{proxy}, ua_type = #{uaType}, proxy_open = #{proxyOpen}")
    int updateSetting(Setting setting);
}
