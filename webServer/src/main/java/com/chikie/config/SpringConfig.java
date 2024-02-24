package com.chikie.config;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.PropertySource;

@Configuration // Spring配置类注解
@PropertySource("classpath:jdbc.properties") // 加载数据库配置文件到spring容器中，可全局使用
@ComponentScan({"com.chikie.service", "com.chikie.dao"}) // 扫设置描包用于自动装配
@Import({JdbcConfig.class, MyBatisConfig.class}) // 导入配置
public class SpringConfig {
}
