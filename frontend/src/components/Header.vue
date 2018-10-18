<template>
  <x-header class="myheader" slot="header" :left-options="{showBack: false}">
    知今
  </x-header>
</template>

<script>
import { XHeader } from 'vux'
export default {
  components: {
    XHeader
  }
}
</script>

<style lang="less">
.myheader{
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  z-index: 999;
}


</style>
