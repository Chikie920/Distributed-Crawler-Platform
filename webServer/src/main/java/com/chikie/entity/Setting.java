package com.chikie.entity;

public class Setting {
    private String userAgent;
    private String proxy;
    private int uaType;
    private int proxyOpen;

    public Setting() {
    }

    public Setting(String userAgent, String proxy, int uaType, int proxyOpen) {
        this.userAgent = userAgent;
        this.proxy = proxy;
        this.uaType = uaType;
        this.proxyOpen = proxyOpen;
    }

    public String getUserAgent() {
        return userAgent;
    }

    public void setUserAgent(String userAgent) {
        this.userAgent = userAgent;
    }

    public String getProxy() {
        return proxy;
    }

    public void setProxy(String proxy) {
        this.proxy = proxy;
    }

    public int getUaType() {
        return uaType;
    }

    public void setUaType(int uaType) {
        this.uaType = uaType;
    }

    public int getProxyOpen() {
        return proxyOpen;
    }

    public void setProxyOpen(int proxyOpen) {
        this.proxyOpen = proxyOpen;
    }

    @Override
    public String toString() {
        return "Setting{" +
                "userAgent='" + userAgent + '\'' +
                ", proxy='" + proxy + '\'' +
                ", uaType=" + uaType +
                ", proxyOpen=" + proxyOpen +
                '}';
    }
}
