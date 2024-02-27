package com.chikie.controller;


import com.chikie.entity.News;
import com.chikie.service.NewsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin
@RestController
public class ResourceManageController {
    @Autowired
    private NewsService newsService;

    @GetMapping("/resmag")
    public List<News> getAllNews() {
        System.out.println("getAllNews....cnm");
        return newsService.getAllNews();
    } // 获取所有新闻数据

    @PutMapping("/resmag")
    public int updateNews(@RequestBody News news) {
        System.out.println("Put operation....");
        System.out.println(news);
        return newsService.updateNews(news);
    } // 更新新闻数据

    @DeleteMapping("/resmag/{id}")
    public int deleteNews(@PathVariable("id") String id) {
        System.out.println("Delete operation....");
        System.out.println(id);
        return newsService.deleteNews(id);
    } // 根据id删除数据
}
