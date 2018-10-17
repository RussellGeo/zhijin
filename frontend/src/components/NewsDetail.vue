<template>
  <div>
    <x-header slot="header">
      知今
    </x-header>

    <!-- card>
      <div slot="header" style="width:100%;">
        <p>{{title}}</p>
      </div>
      <div slot="content">
        <p style="color:#999;font-size:12px;">{{source}} {{date}} | {{other}}</p>
        <p>{{content}}</p>
      </div>
    </card -->

    <article id="article">
      <div class="article-info">
        <h1 class="title">{{title}} </h1>
        <span class="source" style="font-size:15px;">{{source}} </span>
        <span class="date" style="font-size:12px;">{{date}} </span>
      </div>
      <br>
        
      <section class="article-content">
        <div class="content-html" v-html='content'> </div>
      </section>
    </article>

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
    set_article (news) {
      this.title = news.title
      this.content = news.content
      this.source = news.meta.source
      this.date = news.meta.date
      this.other = news.meta.other
    },
    get_news_detail (newsId) {
      axios({
        method: 'get',
        url: ip + '/get_news_detail?news_id=' + newsId
      })
      .then(function (response) {
        console.log(response)
        return response
      })
      .catch(function (error) {
        console.log(error)
      })
    },

    get_news_detail2 (newsId) {
      let self = this
      this.$jsonp(ip + '/get_news_detail?news_id=' + newsId).then(data => {
        console.log(data)
        self.set_article(data.data)
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
      title: '',
      content: '',
      source: '',
      date: '',
      other: ''
    }
  }
}
</script>

<style lang="less">
.title1 {
    color: #000;
    font-size: 20px;
    font-weight: bold;
    padding: 0.4rem 0;
    text-align: center;
}

#article {
  width: 100%;
  position: relative;
  padding-top: 20px;
  padding-right: 16px;
  padding-bottom: 12px;
  padding-left: 16px;
}
  .article_info {
    font-size: 12px;
    overflow: hidden;
    background: #fff;
    padding: 0 0.427rem 0.4rem;
    border-bottom: 1px solid #eee;
    background: #fff;
  }
    .title {
        color: #000;
        font-size: 20px;
        font-weight: bold;
        padding: 0.4rem 0;
        text-align: center;
    }
    .source {
        margin-right: 5px;
    }
  
  .article-content {
      position: relative;
      color: #333;
      font-size: 18px !important;
      line-height: 30px;
      padding: 0.4rem 0.427rem;
  }
      .content-html {
          overflow: hidden;
          text-indent: none !important;
          font-size: inherit;
          &.content_html-close{
              height: 1200px;
          }
          img {
              width: 100% !important;
              height: auto !important;
          }
          img[type="icon"]{
              width: initial!important;
          }
          *{
              text-indent: inherit !important;
              font-size: inherit !important;
              font-family: inherit !important;
              line-height: inherit !important;
              text-align: justify !important;
          }
          div,p{
              width: 100% !important;
              padding-bottom: 15px;
          }
      }
      .content-moreBtn {
          margin-top: 15px;
          padding: 5px 0;
          text-align: center;
          font-size: 14px;
          color: #00939c;
      }

</style>

