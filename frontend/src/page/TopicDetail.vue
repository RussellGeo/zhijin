<template>
  <div> 
    <x-header slot="header">
      知今
    </x-header>

    <scroller style="top:auto;">

    <v-app>
      <v-layout>
        <v-flex xs12 sm6 offset-sm3>
          <v-card>
            <v-img
              class="white--text"
              height="200px"
              src="https://cdn.vuetifyjs.com/images/cards/docks.jpg">
              <v-container fill-height fluid>
                <v-layout fill-height>
                  <v-flex xs12 align-end flexbox>
                    <span class="headline">{{topic.title}}</span>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-img>
            <v-card-title>
              <div>
                <span>{{topic.desc}}</span>
              </div>
            </v-card-title>
            <v-card-text>
              <v-container fluid>
                <template v-for="(op, index) in topic.options">

                <v-layout row align-content-center>
                  <v-flex xs12 md12>
                    <v-card tile flat>
                      <v-card-text>
                        <h3>{{index + 1}}. {{op.option}}</h3>
                      </v-card-text>
                    </v-card>
                  </v-flex>
                </v-layout>

                <v-layout row justify-space-between>
                  <v-flex xs4 md4>
                    <v-card tile flat>
                      <v-card-text>
                        <span>{{op.value}}%</span>
                      </v-card-text>
                    </v-card>
                  </v-flex>
                  <v-flex xs4 order-md1 order-xs3>
                    <v-btn color="red lighten-1" @click="support(op.index)">支持</v-btn>
                  </v-flex>
                </v-layout>
                <v-divider></v-divider>

                </template>

              </v-container>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-app>

    </scroller>
    <br><br><br>
    <br><br><br>

  </div>
</template>

<script>
import Header from '@/components/Header'
import { XHeader, Card, XTable } from 'vux'
import settings from '@/utils/config'
import Vue from 'vue'

export default {
  components: {
    'my-header': Header,
    XHeader,
    Card,
    XTable
  },
  data () {
    return {
      topic: {
        topicId: 0,
        title: '',
        desc: '',
        source: '',
        pubDate: '',
        options: []
      }
    }
  },
  created: function () {
    let topicid = this.$route.query.topicid
    console.log('topicid:' + topicid)
    this.get_topic_detail(topicid)
  },

  methods: {
    get_topic_detail (topicid) {
      let url = settings.GetTopicDetailURL + '?topicid=' + topicid
      console.log(url)
      Vue.jsonp(url).then(data => {
        console.log(data.data)
        let t = JSON.parse(data.data)
        this.topic.topicId = t.topicid
        this.topic.title = t.title
        this.topic.desc = t.desc
        this.topic.source = t.source
        this.topic.pubDate = t.pubdate
        this.topic.deadline = t.deadline
        this.topic.options = JSON.parse(t.options)
      })
      .catch(error => {
        console.log(error)
        alert('get topic detail failed')
      })
    },
    support (index) {
      console.log(index)
      let url = settings.TopicVoteURL + '?topicid=' + this.topic.topicId + '&op_index=' + index
      console.log(url)
      Vue.jsonp(url).then(data => {
        console.log(data.data)
        if (data.retcode !== 0) {
          console.log('vote failed')
          return
        }
        this.$router.go(0)
      })
      .catch(error => {
        console.log(error)
        alert('get topic detail failed')
      })
    }
  }

}
</script>


