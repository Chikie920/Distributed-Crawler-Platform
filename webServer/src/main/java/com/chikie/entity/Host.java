package com.chikie.entity;

public class Host {
    private String id;
    private String ip;
    private String port;

    public Host() {
    }

    public Host(String id, String ip, String port) {
        this.id = id;
        this.ip = ip;
        this.port = port;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public String getPort() {
        return port;
    }

    public void setPort(String port) {
        this.port = port;
    }

    @Override
    public String toString() {
        return "Host{" +
                "id=" + id +
                ", ip='" + ip + '\'' +
                ", port='" + port + '\'' +
                '}';
    }
}
