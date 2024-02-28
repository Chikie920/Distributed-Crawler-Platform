package com.chikie.controller;

import com.chikie.entity.Task;
import com.chikie.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@CrossOrigin
@RestController
public class TaskController {
    @Autowired
    private TaskService taskService;
    @GetMapping("/task")
    public List<Task> getAllTasks(){
        System.out.println("Get all tasks....");
        return taskService.getAllTasks();
    } // 获取所有任务信息
}
