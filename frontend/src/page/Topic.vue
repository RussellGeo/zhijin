<template>
  <div id="app">

  <my-header></my-header>
 
  <v-app>
    <v-btn
      color="pink"
      dark
      absolute
      middle
      right
      fab
      @click="createTopic"
    >
      <v-icon>add</v-icon>
    </v-btn>

  <scroller style="width:auto !important;left:auto;" class="my-scroller" :on-refresh="refresh" :on-infinite="infinite" ref="refScroller">

    <v-container grid-list-sm>

      <v-layout  column>

        <template v-for="(topic, index) in topics">

        <v-flex xs12 sm6 md3>
          <router-link :to="{path:'/topic_detail', query:{topicid:topic.topicId}}" class="new" :topicid='topic.topicId'>

            <v-card>
              <v-card-title>
                <div>
                  <div class="headline">{{topic.title}}</div>
                  <span>{{topic.desc}}</span> <br>
                  <span>{{topic.source}}</span> | <span>{{topic.pubDate}}</span>  
                </div>
              </v-card-title>
            </v-card>

          </router-link>
        </v-flex>

        </template>

      </v-layout>
    </v-container>

    <!--v-card>
      <v-container
        fluid
        grid-list-sm
      >
        <v-layout column align-center >
          
          <template v-for="(topic, index) in topics">

          <v-flex xs12 md6 >
            <router-link to="/topic_detail" class="new" :key='topic.topicId'>
            <v-card>
              <v-card-title>
                <div>
                  <div class="headline">{{topic.title}}</div>
                  <span>{{topic.desc}}</span> <br>
                  <span>{{topic.source}}</span> | <span>{{topic.pubDate}}</span>  
                </div>
              </v-card-title>
            </v-card>
            </router-link>
          </v-flex>

          </template>

        </v-layout>
      </v-container>
    </v-card-->

  </scroller>
  </v-app>


  <bottom-menu></bottom-menu>
</div>
</template>

<script>
import TabMenu from '@/components/TabMenu'
import Header from '@/components/Header'
import settings from '@/utils/config'
import Vue from 'vue'

export default {
  components: {
    'my-header': Header,
    'bottom-menu': TabMenu
  },
  data () {
    return {
      pos: 0,
      request_num: 5,
      requesting: false,
      topics: []
    }
  },
  created: function () {
    this.getTopics()
  },
  methods: {
    createTopic () {
      this.$router.push({ path: '/create_topic' })
    },
    getTopics () {
      if (this.requesting === true) {
        return
      }
      this.requesting = true
      let url = settings.GetTopicURL + '?pos=' + this.pos + '&num=' + this.request_num
      console.log(url)
      Vue.jsonp(url).then(data => {
        console.log(data.data)
        if (data.retcode !== 0) {
          this.requesting = false
          return
        }
        let topiclist = JSON.parse(data.data)
        for (let i in topiclist) {
          let topic = topiclist[i]
          let t = {topicId: topic.topicid, title: topic.title, desc: topic.desc, source: topic.source, pubDate: topic.pubdate, deadline: topic.deadline, option: JSON.parse(topic.options)}
          this.topics.push(t)
          this.pos = this.pos + 1
        }
        this.requesting = false
      })
      .catch(error => {
        console.log(error)
        alert('get topic list failed！')
        this.requesting = false
      })
    },
    refresh () {
      console.log('refresh function')
      this.$router.go(0)
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
      let self = this
      console.log('infinite function')
      console.log(this.$cookies.get('token'))
      setTimeout(() => {
        let l1 = self.topics.length
        self.getTopics()
        let l2 = self.topics.length
        if (l1 === l2) {
          self.$refs.refScroller.finishInfinite(true)
        } else {
          self.$refs.refScroller.finishInfinite()
        }
      }, 1500)
    }
  }
}
</script>

<style lang="less">
.my-scroller{
  top: auto !important;
}
</style>
