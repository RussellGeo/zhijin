<template>
  <div>
    <!--x-header class="header" slot="header" :left-options="{showBack: false}"> zhijin </x-header-->
    <my-header> </my-header>
    <scroller style="width:auto !important;left:auto;" class="my-scroller" :on-refresh="refresh" :on-infinite="infinite" ref="refScroller">
      <!--panel :list="newsList" :type="panel_type" @on-click-item="onClickItem" @on-img-error="onImgError"></panel-->

      <!--panel :list="tailNewsList" :type="panel_type" @on-click-item="onClickItem" @on-img-error="onImgError"></panel-->

      <v-list two-line>
        <template v-for="(item, index) in tailNewsList">
          <v-list-tile
            :key="item.title"
            avatar
            ripple
            @click="onClickItem(item)"
          >

            <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                <v-list-tile-sub-title class="text--primary">{{ item.desc}}</v-list-tile-sub-title>
                <v-list-tile-sub-title>{{ item.meta.source}} | {{ item.meta.date }}</v-list-tile-sub-title>
              </v-list-tile-content>

            </v-list-tile>
            <v-divider
              v-if="index + 1 < tailNewsList.length"
              :key="index"
            ></v-divider>

        </template>
      </v-list>

    </scroller>

    <bottom-menu></bottom-menu>
  </div>
</template>

<script>
// import { XHeader, Panel } from 'vux'
import { Panel } from 'vux'
import { mapState, mapActions, mapMutations } from 'vuex'
import Header from '@/components/Header'
import TabMenu from '@/components/TabMenu'

// var inited = false
var updating = false

export default {
  components: {
    // XHeader,
    'my-header': Header,
    'bottom-menu': TabMenu,
    Panel
  },
  methods: {
    onImgError (item, $event) {
      console.log(item, $event)
    },

    onClickItem (item) {
      if (item.url === '/') {
        window.open(item.src)
      }
    },

    ...mapActions([
      'get_news_api',
      'j_get_news_api'
    ]),

    ...mapMutations([
      'set_newscreated'
    ]),

    refresh () {
      console.log('refresh function')
      this.$refs.refScroller.finishPullToRefresh()

      // console.log(this.$refs.refScroller)
      // let self = this
      // setTimeout(() => {
      //   // self.get_news_api('/get_news/', true)
      //   self.get_news_api({url: '/get_news/', isTop: true})
      //   self.$refs.refScroller.finishPullToRefresh()
      // }, 1500)
    },

    infinite () {
      console.log('enter infinite')
      // console.log(inited)
      // if (inited === false) {
      //   this.$refs.refScroller.finishInfinite()
      //   return
      // }
      if (updating === true) {
        this.$refs.refScroller.finishInfinite()
        return
      }
      updating = true
      let self = this
      console.log('infinite function')
      console.log(this.$cookies.get('token'))
      setTimeout(() => {
        // self.get_news_api('/get_news/', false)
        let l = self.tailNewsList.length
        console.log(l)
        self.j_get_news_api({url: '/get_news/', isTop: false})
        let l2 = self.tailNewsList.length
        console.log(l2)
        if (l === l2) {
          console.log('no more data')
          self.$refs.refScroller.finishInfinite(true)
        } else {
          self.$refs.refScroller.finishInfinite()
        }
        updating = false
        console.log('infinite function2')
      }, 1500)
      console.log('infinite function3')
    }

  },

  computed: {
    ...mapState({
      newsCreated: state => state.NewsStore.newsCreated,
      newsList: state => state.NewsStore.newsList,
      tailNewsList: state => state.NewsStore.tailNewsList
    })
  },

  created: function () {
    console.log(this.newsCreated)
    if (this.newsCreated === true) {
      console.log('already created')
      return
    }
    this.set_newscreated()
    console.log('News.vue created')
    // setTimeout(() => {
    //   this.j_get_news_api({url: '/get_news/', isTop: false})
    //   inited = true
    // }, 1500)
  },

  data () {
    return {
      panel_type: '4',
      list: [{
        src: 'http://somedomain.somdomain/x.jpg',
        fallbackSrc: 'http://placeholder.qiniudn.com/60x60/3cc51f/ffffff',
        title: '标题一',
        desc: '由各种物质组成的巨型球状天体，叫做星球。星球有一定的形状，有自己的运行轨道。',
        url: '/'
      }, {
        src: 'http://placeholder.qiniudn.com/60x60/3cc51f/ffffff',
        title: '标题二',
        desc: '由各种物质组成的巨型球状天体，叫做星球。星球有一定的形状，有自己的运行轨道。',
        url: {
          path: '/',
          replace: false
        },
        meta: {
          source: '来源信息',
          date: '时间',
          other: '其他信息'
        }
      }]
    }
  },

  beforeRouteEnter (to, from, next) {
    if (!sessionStorage.askPositon || from.path === '/') {
      console.log('before enter from path' + from.path)
      sessionStorage.askPositon = ''
      next()
    } else {
      next(vm => {
        if (vm && vm.$refs.refScroller) {
          setTimeout(function () {
            vm.$refs.refScroller.scrollTo(0, sessionStorage.askPositon, false)
          }, 3)
        }
      })
    }
  },
  beforeRouteLeave (to, from, next) {
    sessionStorage.askPositon = this.$refs.refScroller && this.$refs.refScroller.getPosition() && this.$refs.refScroller.getPosition().top
    next()
  }

}
</script>

<style lang="less">

.my-scroller{
  top: auto !important;
}

.myheader{
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  z-index: 999;
}

</style>

