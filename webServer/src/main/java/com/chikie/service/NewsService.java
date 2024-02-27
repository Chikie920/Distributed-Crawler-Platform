package com.chikie.service;

import com.chikie.entity.News;

import java.util.List;

public interface NewsService {
    List<News> getAllNews();
    News getNewsById(String id);
    int updateNews(News news);
    int deleteNews(String id);
}
