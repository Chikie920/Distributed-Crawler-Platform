package com.chikie.service.impl;

import com.chikie.dao.NewsDao;
import com.chikie.entity.News;
import com.chikie.service.NewsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NewsServiceImpl implements NewsService {
    @Autowired
    private NewsDao newsDao;
    @Override
    public List<News> getAllNews() {
        return newsDao.getAllNews();
    }

    @Override
    public News getNewsById(String id) {
        return newsDao.getNewsById(id);
    }

    @Override
    public int updateNews(News news) {
        return newsDao.updateNews(news.getId(), news.getTitle(), news.getDate(), news.getContent());
    }

    @Override
    public int deleteNews(String id) {
        return newsDao.deleteNews(id);
    }
}
