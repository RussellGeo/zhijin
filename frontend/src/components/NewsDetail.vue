<template>
  <div>
    <x-header slot="header">
      知今
    </x-header>

    <card>
    <div slot="header">
      <p>{{title}}</p>
    </div>
    <div slot="content">
      <p>{{content}}</p>
    </div>
    </card>
  </div>
</template>

<script>
import { XHeader, Card } from 'vux'
import axios from 'axios'

var ip = 'http://106.12.124.186:8899'

export default {
  components: {
    XHeader,
    Card
  },

  watch: {
    $route (val) {
      if (val.query.news_id) {
        let newsId = val.query.news_id
        console.log('watch news_id:' + newsId)
        this.get_news_detail2(newsId)
      }
    }
  },

  methods: {
    get_news_detail (newsId) {
      axios({
        method: 'get',
        url: ip + '/get_news_detail?news_id=' + newsId
      })
      .then(function (response) {
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
      })
    },

    get_news_detail2 (newsId) {
      this.$jsonp(ip + '/get_news_detail?news_id=' + newsId).then(data => {
        console.log(data)
      }).catch(err => {
        console.log(err)
      })
    }

  }, // end methods

  created: function () {
    let newsId = this.$route.query.news_id
    console.log('news_id:' + newsId)
    this.get_news_detail2(newsId)
  },

  data () {
    return {
      title: 'title 111',
      content: 'content ss'
    }
  }
}
</script>


