<template>
  <div>

<v-app>
    <scroller style="top:auto;">

  <v-layout justify-center>
    <v-flex xs12>
      <v-card ref="form">
    <v-toolbar
      color="deep-purple accent-4"
      cards
      dark
      flat
    >
      <v-btn icon>
        <v-icon>arrow_back</v-icon>
      </v-btn>
      <v-card-title class="title font-weight-regular">创建新话题</v-card-title>
      <v-spacer></v-spacer>
    </v-toolbar>

        <v-card-text>
          <v-text-field
            ref="topicTitle"
            v-model="topicTitle"
            :rules="[() => !!topicTitle || 'This field is required']"
            :error-messages="errorMessages"
            label="标题"
            placeholder=""
            required
          ></v-text-field>

          <v-textarea
          box
          ref="topicDesc"
          name="topicDesc"
          label="简述"
          v-model="topicDesc"
          :rules="[() => !!topicDesc || 'This field is required']"
          :error-messages="errorMessages"
          required
          value=""
          ></v-textarea>

          <v-text-field
            ref="option1"
            v-model="option1"
            :rules="[() => !!option1 || 'This field is required']"
            :error-messages="errorMessages"
            label="选项一"
            placeholder=""
            required
          ></v-text-field>

          <v-text-field
            ref="option2"
            v-model="option2"
            :rules="[() => !!option2 || 'This field is required']"
            :error-messages="errorMessages"
            label="选项二"
            placeholder=""
            required
          ></v-text-field>

          <v-text-field
            ref="option3"
            v-model="option3"
            label="选项三"
            placeholder=""
            required
          ></v-text-field>

          <v-text-field
            ref="option4"
            v-model="option4"
            label="选项四"
            placeholder=""
            required
          ></v-text-field>

        <!--v-card>
        <v-layout>
        <v-flex xs12-->
        <group title="设置开始日期">
        <datetime 
          v-model="pubdate" 
          format="YYYY-MM-DD HH:mm" 
          :hour-list="['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']" 
          :minute-list="['00']" 
          @on-change="pubdateChange" 
          title="开始日期"> </datetime>
        </group>
        <group title="设置截止日期">
        <datetime 
          v-model="deadline" 
          format="YYYY-MM-DD HH:mm" 
          :hour-list="['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']" 
          :minute-list="['00']" 
          @on-change="deadlineChange" 
          title="截止日期"> </datetime>
        </group>
        <!--/v-flex>
        </v-layout>
        </v-card-->



        </v-card-text>

        <v-divider class="mt-5"></v-divider>
        <v-card-actions>
          <v-btn flat>取消</v-btn>
          <v-spacer></v-spacer>
          <v-slide-x-reverse-transition>
            <v-tooltip
              v-if="formHasErrors"
              left
            >
              <v-btn
                slot="activator"
                icon
                class="my-0"
                @click="resetForm"
              >
                <v-icon>refresh</v-icon>
              </v-btn>
              <span>Refresh form</span>
            </v-tooltip>
          </v-slide-x-reverse-transition>
          <v-btn color="primary" flat @click="submit">提交</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
  <br><br><br><br>

    </scroller>

</v-app>


  </div>
</template>

<script>
import { Datetime, Group } from 'vux'

import { mapState } from 'vuex'
import settings from '@/utils/config'
import Vue from 'vue'

export default {
  components: {
    Datetime,
    Group
  },

  data: () => ({
    countries: [],
    errorMessages: '',
    topicTitle: '',
    deadline: '',
    pubdate: '',
    topicDesc: '',
    option1: '',
    option2: '',
    option3: '',
    option4: '',
    formHasErrors: false
  }),

  computed: {
    form () {
      return {
        topicTitle: this.topicTitle,
        topicDesc: this.topicDesc,
        deadline: this.deadline,
        option1: this.option1,
        option2: this.option2
      }
    },
    ...mapState({
      logined: state => state.GlobalStore.logined,
      userid: state => state.GlobalStorea.userid
    })

  },
  watch: {
    topicTitle () {
      this.errorMessages = ''
    }
  },

  methods: {
    deadlineChange (value) {
      console.log('deadline change', value)
    },
    pubdateChange (value) {
      console.log('pubdate change', value)
    },

    addressCheck () {
      this.errorMessages = this.address && !this.topicTitle
        ? 'Hey! I\'m required'
        : ''

      return true
    },
    resetForm () {
      this.errorMessages = []
      this.formHasErrors = false

      Object.keys(this.form).forEach(f => {
        this.$refs[f].reset()
      })
    },
    submit () {
      // if (this.logined === false) {
      //   alert('请先登录')
      //   this.$router.push({ path: '/login' })
      //   return
      // }

      this.formHasErrors = false
      Object.keys(this.form).forEach(f => {
        if (!this.form[f]) this.formHasErrors = true
      })

      if (this.formHasErrors === true) {
        alert('请输入完整')
        return
      }

      let url = settings.CreateTopicURL + '?title=' + this.topicTitle + '&desc=' + this.topicDesc + '&deadline=' + this.deadline + '&pubdate=' + this.pubdate + '&option1=' + this.option1 + '&option2=' + this.option2
      if (this.option3.length > 0) {
        url = url + '&option3=' + this.option3
        if (this.option4.length > 0) {
          url = url + '&option4=' + this.option4
        }
      }
      if (this.option4.length > 0 && this.option3.length === 0) {
        alert('请依次填写option')
        return
      }
      console.log(url)
      Vue.jsonp(url).then(data => {
        console.log(data.data)
        if (data.retcode !== 0) {
          alert('创建失败！' + data.errmsg)
          return
        }
        this.$router.push({ path: '/topic' })
      })
      .catch(error => {
        console.log(error)
        alert('创建失败！')
      })
    }
  }
}
</script>

