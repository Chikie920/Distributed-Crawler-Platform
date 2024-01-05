<template>
    <mdui-top-app-bar style="position: relative;background-color:antiquewhite;">
        <mdui-icon-menu class="menu_icon"></mdui-icon-menu>
        <mdui-top-app-bar-title class="top_title">Title</mdui-top-app-bar-title>
        <div style="flex-grow: 1"></div>
    </mdui-top-app-bar>
</template>

<script setup>
import 'mdui/components/top-app-bar.js'
import 'mdui/components/top-app-bar-title.js'
import '@mdui/icons/menu.js'
</script>

<style scoped>
.menu_icon {
    margin: auto;
}

.top_title {
    margin-left: 2vw;
}

</style>
