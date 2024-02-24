package com.chikie.config;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;

@Configuration
@ComponentScan({"com.chikie.controller", "com.chikie.config"})
@EnableWebMvc
public class SpringMvcConfig {
}
