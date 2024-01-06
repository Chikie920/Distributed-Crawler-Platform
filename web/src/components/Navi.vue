<template>
    <mdui-navigation-drawer open="true" class="example-drawer navi" full-height ref="drawer">
        <mdui-list class="list_container" v-for="item,idx in operateList" :key="idx">
            <mdui-list-item rounded class="list_item">
                <p class="list_item_p">
                    {{ item }}
                </p>
                <mdui-icon-monitor v-if="idx==0"></mdui-icon-monitor>
                <mdui-icon-post-add v-if="idx==1"></mdui-icon-post-add>
                <mdui-icon-data-saver-off v-if="idx==2"></mdui-icon-data-saver-off>
                <mdui-icon-analytics v-if="idx==3"></mdui-icon-analytics>
                <mdui-icon-settings v-if="idx==4"></mdui-icon-settings>
            </mdui-list-item>
        </mdui-list>
    </mdui-navigation-drawer>
</template>

<script setup>
import 'mdui/components/navigation-drawer.js'
import 'mdui/components/list.js'
import 'mdui/components/list-item.js'
import 'mdui/components/list-subheader.js'
import '@mdui/icons/monitor.js'
import '@mdui/icons/post-add.js'
import '@mdui/icons/data-saver-off.js'
import '@mdui/icons/analytics.js'
import '@mdui/icons/settings.js'
import emitter from '@/tools/emitter.js'
import { ref, onUnmounted } from 'vue'


let drawer = ref() // 引用元素

function operateDrawer() { // 操作抽屉
    let open = drawer.value.open // 获取抽屉状态
    if (open) {
        drawer.value.open = false
    } else {
        drawer.value.open = true
    }
}

emitter.on('operateDrawer', operateDrawer) // 绑定事件

onUnmounted(() => { // 在页面撤销时销毁绑定事件
    emitter.off('operateDrawer')
})

let operateList = ['状态监视', '任务创建', '资源管理', '数据分析', '设置']

</script>

<style scoped>
.navi {
    width: 12%;
    position: relative;
    background-color: #fafdfd;
}

.list_container {
    background-color: #fafdfd;
}

mdui-navigation-drawer::part(panel) {
    background-color: #fafdfd;
}

.list_item {
    height: 7vh;
    text-align: center;
    display:flex;/*Flex布局*/
    /* display: -webkit-flex;
    align-items:center; */
}

.list_item_p {
    font-weight: 600;
    float: right;
    margin: auto;
    margin-left: 1rem;
}

</style>
