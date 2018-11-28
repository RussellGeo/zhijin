<template>
  <div class="select">
    <my-header> </my-header>
    <section class="news">
          <router-link to="/topic_detail" class="new" :key='news.channelId'>
            <div class="intro">
              <h4>{{news.title}}</h4>
              <p><span>{{news.source}}</span> | <span>{{news.pubDate}}</span></p>
            </div>
          </router-link>

          <a href="javascript: void(0)" class="new" :key='news.channelId'>
            <div class="intro">
              <h4>{{news.title}}</h4>
              <p><span>{{news.option1.option}}</span><span class="op_value">{{news.option1.value}}</span></p>
              <p><span>{{news.source}}</span> | <span>{{news.pubDate}}</span></p>
            </div>
          </a>

    </section>
  </div>
</template>

<script>
import Header from '@/components/Header'

export default {
  components: {
    'my-header': Header
  },
  data () {
    return {
      news: {
        channelId: 1,
        title: 'title',
        source: 'source',
        pubDate: 'pubData',
        option1: {option: 'op1', value: 11},
        option2: {option: 'op2', value: 89}
      }
    }
  }
}
</script>

<style lang="less">
.select{
  background: #fff;
  .swiper-wrapper{
    height: 200px;
    .swiper-slide img{
      width: 100%;
      height: 200px;
    }
  }
  .news{
    min-height: 500px;
    padding: 0 10px;
    .new{
      height: 100px;
      color: #262627;
      border-bottom: 1px solid #eee;
      display: flex;
      justify-content: flex-start;
      align-items: center;
      width: 100%;
      img{
        height: 80px;
        width: 100px;
      }
      .intro{
        width: 80%;
        height: 80px;
        display: flex;
        padding-left: 10px;
        flex-direction: column;
        justify-content: space-between;
        h4{
          font-size: 20px;
          line-height: 1.2;
          font-weight: bold;
          overflow: hidden;
          display: -webkit-box;
          word-break: break-all;
          -webkit-line-clamp: 2;
          text-overflow: ellipsis;
          -webkit-box-orient: vertical;
        }
        p{
          font-size: 13px;
          color: #666;
        }
        .op_value{
          float:right;
        }
      }
    }
    .loadMore{
      height: 50px;
      width: 100%;
      color: #545454;
      background: #eee;
      text-align: center;
      line-height: 50px;
      font-size: 13px;
      border: none;
      border-radius: 0;
      outline: none;
      margin-bottom: 10px;
    }
    .fail{
      display: flex;
      min-height: 300px;
      align-items: center;
      justify-content: center;
    }
  }
}

</style>
