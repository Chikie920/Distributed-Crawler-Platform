<template>
    <!-- <mdui-radio-group value="0" style="display: block;">
        <mdui-radio value="0">使用模板创建</mdui-radio>
        <mdui-radio value="1">自定义创建</mdui-radio>
    </mdui-radio-group> -->
    <h2>创建方式</h2>
    <mdui-select @change="create_type_change" variant="outlined" :value="select_type"
        style="width: 15%; display: block; margin-top: 1rem;">
        <mdui-menu-item value="1">#使用模板创建任务</mdui-menu-item>
        <mdui-menu-item value="2">#自定义创建任务</mdui-menu-item>
    </mdui-select>
    <div v-show="select_type == '1'">
        <h2 style="margin-top: 1rem;">主机选择</h2>
        <mdui-select variant="outlined" :value="0" style="width: 20%; display: block; margin-top: 1rem;">
            <mdui-menu-item v-for="host, index in available_host_list" :key="index" :value="index">
                #{{ host.ip + ":" + host.port }}
            </mdui-menu-item>
        </mdui-select>
        <h2 style="margin-top: 2rem;">模板选择</h2>
        <mdui-select variant="outlined" :value="0" style="width: 15%; margin-top: 1rem; display: block;">
            <mdui-menu-item v-for="job, index in job_list" :key="index" :value="index">
                #{{ job }}
            </mdui-menu-item>
        </mdui-select>
    </div>

    <div v-show="select_type == '2'">
        <h2 style="margin-top: 1rem;">相关参数</h2>
        <mdui-text-field style="width: 20%; margin-top: 1rem; display: block;" label="任务名称"></mdui-text-field>
        <mdui-text-field style="width: 40%; margin-top: 1rem; display: block;" label="目标网址"></mdui-text-field>

        <h2 style="margin-top: 1rem;">主机选择</h2>
        <mdui-select variant="outlined" :value="0" style="width: 20%; display: block; margin-top: 1rem;"
            v-for="host, index in available_host_list" :key="index">
            <mdui-menu-item :value="index">#{{ host.ip + ":" + host.port }}</mdui-menu-item>
        </mdui-select>

    </div>

    <mdui-button variant="outlined" style="margin-top: 1rem;">提交</mdui-button>
</template>

<script setup>
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mdui/components/radio-group.js';
import 'mdui/components/radio.js';
import 'mdui/components/text-field.js';
import 'mdui/components/select.js';
import 'mdui/components/select.js';
import 'mdui/components/menu-item.js';
import 'mdui/components/button.js';
import { ref, onMounted } from 'vue';
import emitter from '../tools/emitter.js';

let select_type = ref("1"); // 选择创建方式
let available_host_list = ref([]); // 在线主机列表
let job_list = ref(['百度新闻', '网易新闻', '新浪新闻', '凤凰新闻', '澎湃新闻', '搜狐新闻']); // 存放爬虫模板

function create_type_change() {
    if (select_type.value == "1") {
        select_type.value = "2";
    } else {
        select_type.value = "1";
    }
}

emitter.on('getOnlineHost', (res) => {
    // console.log(value);
    // available_host_list.value = toRaw(value)[0];
    // console.log(JSON.parse(JSON.stringify(res)))
    available_host_list.value = JSON.parse(JSON.stringify(res));
    // console.log(available_host_list.value);
});

onMounted(() => {
});

</script>

<style scoped>
mdui-text-field::part(container) {
    background-color: #E0E0E0;
}
</style>