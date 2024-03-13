package com.chikie.config;

import com.alibaba.druid.pool.DruidDataSource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;

import javax.sql.DataSource;

public class JdbcConfig {
    @Value("${jdbc.url}")
    private String url;
    @Value("${jdbc.name}")
    private String name;
    @Value("${jdbc.password}")
    private String password;

    @Bean // 让spring管理第三方bean
    public DataSource getDataSource() {
        DruidDataSource druidDataSource = new DruidDataSource(); // 创建德鲁伊连接池
        druidDataSource.setUrl(url);
        druidDataSource.setUsername(name);
        druidDataSource.setPassword(password);
        return druidDataSource;
    }
}
