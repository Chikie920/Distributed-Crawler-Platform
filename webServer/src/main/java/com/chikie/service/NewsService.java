package com.chikie.service;

import com.chikie.entity.News;

import java.util.List;

public interface NewsService {
    List<News> getAllNews(); // 获取所有新闻信息
    News getNewsById(String id); // 根据id获取新闻信息
    List<News> getNewsByTaskName(String taskName); // 根据任务名获取新闻信息
    int updateNews(News news); // 更新新闻信息
    int deleteNews(String id); // 根据id删除新闻
}
