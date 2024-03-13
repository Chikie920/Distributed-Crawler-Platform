package com.chikie.controller;


import com.chikie.entity.News;
import com.chikie.service.NewsService;
import org.apache.ibatis.annotations.Select;
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

    @GetMapping("/resmag/{taskName}")
    public List<News> getNewsByTaskName(@PathVariable("taskName") String taskName) {
        System.out.println("GetNewsByTaskName....");
        return newsService.getNewsByTaskName(taskName);
    }

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

    @GetMapping("/resmag/id")
    public List<String> getAllId() {
        System.out.println("Get All id....");
        return newsService.getAllId();
    }

    @GetMapping("/resmag/counts/{time}")
    public int getNewsCountsByTime(@PathVariable("time") String time) {
        System.out.println("Get NewsCountsByTime....");
        return newsService.getNewsCountsByTime(time);
    }

    @GetMapping("/resmag/contents")
    public List<String> getAllContent() {
        System.out.println("Get All Content....");
        return newsService.getAllContent();
    }
}
