package com.chikie.controller;

import com.chikie.entity.Task;
import com.chikie.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

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
    @GetMapping("/taskName")
    public List<String> getAllTaskName() {
        System.out.println("Get TaskName....");
        return taskService.getAllTaskName();
    }
    @PostMapping("/task")
    public int createTask(@RequestBody Task task) {
        System.out.println("Create Task....");
        return taskService.createTask(task);
    }
    @PutMapping("/task")
    public int updateTask(@RequestBody Task task) {
        System.out.println("Update Task....");
        return taskService.updateTask(task);
    }
    @PutMapping("/task/{taskName}")
    public int updateRunTimes(@PathVariable("taskName") String taskName) {
        System.out.println("Update Run Times....");
        return taskService.updateRunTimes(taskName);
    }
}
