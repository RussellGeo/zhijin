<template>
  <div>
    <!--x-header class="header" slot="header" :left-options="{showBack: false}"> zhijin </x-header-->
    <my-header> </my-header>
    <scroller class="my-scroller" :on-refresh="refresh" :on-infinite="infinite" ref="refScroller">
      <panel :list="newsList" :type="panel_type" @on-click-item="onClickItem" @on-img-error="onImgError"></panel>
      <panel :list="tailNewsList" :type="panel_type" @on-img-error="onImgError"></panel>
    </scroller>
  </div>
</template>

<script>
// import { XHeader, Panel } from 'vux'
import { Panel } from 'vux'
import { mapState, mapActions, mapMutations } from 'vuex'
import Header from '@/components/Header'

var inited = false

export default {
  components: {
    // XHeader,
    'my-header': Header,
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
      console.log(this.$refs.refScroller)
      console.log('refresh function')
      let self = this
      setTimeout(() => {
        // self.get_news_api('/get_news/', true)
        self.get_news_api({url: '/get_news/', isTop: true})
        self.$refs.refScroller.finishPullToRefresh()
      }, 1500)
    },

    infinite () {
      if (!inited) {
        this.$refs.refScroller.finishInfinite()
        return
      }
      let self = this
      console.log('infinite function')
      setTimeout(() => {
        // self.get_news_api('/get_news/', false)
        self.get_news_api({url: '/get_news/', isTop: false})
        self.$refs.refScroller.finishInfinite()
        console.log('infinite function2')
      }, 1500)
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
    inited = true
    this.set_newscreated()
    console.log('News.vue created')
    this.get_news_api({url: '/get_news/', isTop: true})
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

