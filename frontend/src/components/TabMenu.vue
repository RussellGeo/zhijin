<template>
      <tabbar>
        <tabbar-item>
          <img src="@/assets/icon_nav_article.png" alt="" slot="icon">
          <span slot="label">Home</span>
        </tabbar-item>
        <tabbar-item>
          <img src="@/assets/icon_nav_cell.png" alt="" slot="icon">
          <span slot="label">Rec</span>
        </tabbar-item>
      </tabbar>
</template>

<script>
import { Tabbar, TabbarItem } from 'vux'
export default {
  components: {
    Tabbar,
    TabbarItem
  }
}
</script>


