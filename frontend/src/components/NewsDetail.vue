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

export default {
  components: {
    XHeader,
    Card
  },

  methods: {
    get_news_detail (newsId) {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8899/get_news_detail?news_id=' + newsId
      })
      .then(function (response) {
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
      })
    },

    get_news_detail2 (newsId) {
      this.$jsonp('http://127.0.0.1:8899/get_news_detail?news_id=' + newsId).then(data => {
        console.log(data)
      }).catch(err => {
        console.log(err)
      })
    }

  },

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


