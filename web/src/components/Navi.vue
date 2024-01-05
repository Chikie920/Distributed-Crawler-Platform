<template>
    <mdui-navigation-drawer open="true" class="example-drawer" full-height="true" ref="drawer" style="position: relative; background-color: pink;">
        <mdui-button @click="closeDrawer">关闭侧边抽屉栏</mdui-button>
    </mdui-navigation-drawer>
    <!-- <mdui-button @click="openDrawer">打开侧边抽屉栏</mdui-button> -->
</template>

<script setup>
    import 'mdui/components/navigation-drawer.js'
    import { ref } from 'vue'


    let drawer = ref()
    function openDrawer() {
        drawer.value.open = true
    }

    function closeDrawer() {
        drawer.value.open = false
    }

</script>

<style scoped></style>
