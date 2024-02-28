package com.chikie.entity;

public class Task {
    private String taskName;
    private String createTime;
    private String runTimes;
    private String dataCounts;

    public Task() {
    }

    public Task(String taskName, String createTime, String runTimes, String dataCounts) {
        this.taskName = taskName;
        this.createTime = createTime;
        this.runTimes = runTimes;
        this.dataCounts = dataCounts;
    }

    public String getTaskName() {
        return taskName;
    }

    public void setTaskName(String taskName) {
        this.taskName = taskName;
    }

    public String getCreateTime() {
        return createTime;
    }

    public void setCreateTime(String createTime) {
        this.createTime = createTime;
    }

    public String getRunTimes() {
        return runTimes;
    }

    public void setRunTimes(String runTimes) {
        this.runTimes = runTimes;
    }

    public String getDataCounts() {
        return dataCounts;
    }

    public void setDataCounts(String dataCounts) {
        this.dataCounts = dataCounts;
    }

    @Override
    public String toString() {
        return "Task{" +
                "taskName='" + taskName + '\'' +
                ", createTime='" + createTime + '\'' +
                ", runTimes='" + runTimes + '\'' +
                ", dataCounts='" + dataCounts + '\'' +
                '}';
    }
}
