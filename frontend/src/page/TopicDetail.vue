<template>
  <div> 
    <x-header slot="header">
      知今
    </x-header>

    <scroller style="top:auto;">
    <card>
      <div slot="header">
        <h1>{{news.title}}</h1>
      </div>
    </card>

    <div>
      <x-table :cell-bordered="false" :content-bordered="false" style="background-color:#fff;">
        <thead>
          <tr style="background-color: #F7F7F7">
            <th>选项</th>
            <th>份数</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{news.option[0].option}}</td>
            <td>{{news.option[0].value}}</td>
          </tr>
        </tbody>
      </x-table>
    </div>

    </scroller>
  </div>
</template>

<script>
import Header from '@/components/Header'
import { XHeader, Card, XTable } from 'vux'

export default {
  components: {
    'my-header': Header,
    XHeader,
    Card,
    XTable
  },
  data () {
    return {
      news: {
        channelId: 1,
        title: 'title',
        source: 'source',
        pubDate: 'pubData',
        option: [{option: 'op1', value: 11}, {option: 'op2', value: 12}]
      }
    }
  }
}
</script>


