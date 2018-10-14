<template>
  <div>
    <scroller :on-refresh="refresh" :on-infinite="infinite" ref="refScroller">
      <panel :list="newsList" :type="panel_type" @on-img-error="onImgError"></panel>
      <panel :list="tailNewsList" :type="panel_type" @on-img-error="onImgError"></panel>
    </scroller>
  </div>
</template>

<script>
import { Panel } from 'vux'
import { mapState, mapActions } from 'vuex'

var inited = false

export default {
  components: {
    Panel
  },
  methods: {
    onImgError (item, $event) {
      console.log(item, $event)
    },

    ...mapActions([
      'get_news_api'
    ]),

    refresh () {
      console.log(this.$refs.refScroller)
      console.log('refresh function')
      let self = this
      setTimeout(() => {
        self.get_news_api('http://127.0.0.1:8899/get_news/', true)
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
        self.get_news_api('http://127.0.0.1:8899/get_news/', false)
        self.$refs.refScroller.finishInfinite()
        console.log('infinite function2')
      }, 1500)
    }

  },

  computed: {
    ...mapState({
      newsList: state => state.NewsStore.newsList,
      tailNewsList: state => state.NewsStore.tailNewsList
    })
  },

  created: function () {
    this.get_news_api('http://127.0.0.1:8899/get_news/', true)
    inited = true
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
  }
}
</script>


