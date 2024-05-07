<template>
    <h2>User-Agent 设置</h2>
    <mdui-radio-group :value="uaType" style="margin-top: 1rem;">
        <mdui-radio @click="changeUaStatus" :value="0">随机 UA</mdui-radio>
        <mdui-radio @click="changeUaStatus" :value="1">自定义 UA</mdui-radio>
    </mdui-radio-group>
    <div style="width: 50%;min-height: 10%;">
        <mdui-text-field :disabled="uaType==0?true:false" ref="uaTextField" rows="3" label="Input Your User-Agent" v-model="ua"></mdui-text-field>
    </div>


    <h2 style="margin-top: 10vh;">网络代理设置</h2>
    <div style="display: flex;text-align: center;margin-top: 1rem;">
        <h5 style="margin: auto 0;">使用代理</h5>
        <mdui-switch :checked="proxyOpen==0?false:true" @change="changeProxyStatus" style="margin-left: 1rem;"></mdui-switch>
    </div>
    <div style="width: 50%;min-height: 10%;">
        <mdui-text-field :disabled="proxyOpen==0?true:false" ref="proxyTextField" rows="3" label="输入代理网络地址" v-model="proxy"></mdui-text-field>
        <mdui-button @click="submitUA" ref="uaButton" variant="elevated"
            style="margin-top: 1rem; float: right;">提交</mdui-button>
    </div>

    <!-- 消息提示 -->
    <mdui-snackbar ref="snackbar_success" placement="top" auto-close-delay="1000"
        class="example-close-delay">操作成功!</mdui-snackbar>
    <mdui-snackbar ref="snackbar_fail" placement="top" auto-close-delay="1000"
        class="example-close-delay">操作失败!</mdui-snackbar>
</template>

<script setup>

import { ref, onMounted } from 'vue';
import 'mdui/components/radio-group.js';
import 'mdui/components/radio.js';
import 'mdui/components/text-field.js';
import 'mdui/components/switch.js';
import 'mdui/components/button.js';
import 'mdui/components/snackbar.js';
import axios from 'axios';

let uaTextField = ref(); // ua代理控件
let uaButton = ref(); // ua代理控件
let proxyTextField = ref(); // proxy代理控件
let setting = ref(); // 存储设置数据
let ua = ref(""); // ua内容
let proxy = ref(""); //proxy内容
let snackbar_success = ref() // 操作结果提示消息条-操作成功
let snackbar_fail = ref() // 操作结果提示消息条-操作失败
let uaType = ref(0); // ua类别
let proxyOpen = ref(0); // 是否开启proxy

function changeUaStatus() {
    if (uaType.value == 0) {
        uaType.value = 1;
    }
    else {
        uaType.value = 0;
    }
} // 更改ua相关控件状态

function changeProxyStatus() {
    if (proxyOpen.value == 0) {
        proxyOpen.value = 1;
    }
    else {
        proxyOpen.value = 0;
    }
} // 更改proxy相关控件状态

function submitUA() {
    let Data = {
        "userAgent": ua.value,
        "proxy": proxy.value,
        "uaType": uaType.value,
        "proxyOpen": proxyOpen.value
    }
    axios.put('http://localhost:8080/setting', Data, {
        headers: { 'Content-Type': 'application/json' }
    }).then(function (response) {
        // 请求成功
        // console.log("*****save*****");
        // console.log(response.data);
        if (response.data == 1) {
            snackbar_success.value.open = true;
        } else {
            snackbar_fail.value.open = true;
        }
    })
        .catch(function (error) {
            // 请求失败
            console.log(error);
        }); // 获取新闻数据
} // 上传UA

onMounted(() => {
    axios.get('http://localhost:8080/setting')
        .then(function (response) {
            // 请求成功
            setting.value = response.data;
            // console.log(setting.value.length);
            ua.value = setting.value.userAgent;
            proxy.value = setting.value.proxy;
            uaType.value = setting.value.uaType;
            proxyOpen.value = setting.value.proxyOpen;
            // console.log(setting.value)
        })
        .catch(function (error) {
            // 请求失败
            console.log(error);
        }); // 获取设置信息
})


</script>

<style scoped></style>