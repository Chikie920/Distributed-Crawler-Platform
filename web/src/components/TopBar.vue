<template>
    <mdui-top-app-bar class="topBar">
        <mdui-icon-menu ref="menu_icon"  class="menu_icon" @click="emitter.emit('operateDrawer')"></mdui-icon-menu>
        <mdui-top-app-bar-title class="top_title">Distributed Crawler Platform</mdui-top-app-bar-title>
        <div style="flex-grow: 1"></div>
    </mdui-top-app-bar>
</template>

<script setup>
import 'mdui/components/top-app-bar.js'
import 'mdui/components/top-app-bar-title.js'
import '@mdui/icons/menu.js'
import emitter from '@/tools/emitter.js'
</script>

<style scoped>
.topBar {
    position: relative;
    background-color: #fafdfd;
}

.menu_icon {
    font-size: 1.8rem;
    margin: auto;
    margin-left: 0.4rem;
    font-weight: 600;
}

.top_title {
    margin-left: 2vw;
    user-select: none;
    font-size: 1.2rem;
    font-weight: 600;
}
</style>
