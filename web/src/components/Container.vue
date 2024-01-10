<template>
    <mdui-layout-main class="example-layout-main" full-height style="background-color: #fafdfd;">
        <RouterView></RouterView>
    </mdui-layout-main>
</template>

<script setup>
    import { RouterView } from 'vue-router';
</script>

<style scoped>
.divider {
    margin-left: 0px;
    float: left;
}
</style>
